from bisect import bisect_left
from couchdb import Server
from datetime import datetime


class Metric(dict):
    def __init__(self, timestamp, role, host, metrics={}):
        self.timestamp = timestamp
        self.role = role
        self.host = host
        self.metrics = metrics
        super(Metric, self).__init__(metrics)


class CraftsCollection(dict):
    def __init__(self, db):
        self._db = db

        super(CraftsCollection, self).__init__()

    def __iter__(self):
        keylist = sorted(self.keys())
        for key in keylist:
            yield self[key]

    def find_nearest(self, dt):
        pos = bisect_left(sorted(self.keys()), dt)

        return self[self.keys()[pos]]

    def get(self, view, **kwargs):
        result = self._db.view(view, **kwargs)
        self.update(dict([(datetime.strptime(doc.id, '%Y-%m-%dT%H:%M:%S.%f'),
                    doc.value) for doc in result]))


class PredictionCollection(CraftsCollection):
    def get(self, role, metric, start=datetime.min, end=datetime.max):
        return super(PredictionCollection, self)\
            .get('crafts/predict',
                 startkey=[role, metric, start.isoformat()],
                 endkey=[role, metric, end.isoformat()])


class SummaryCollection(CraftsCollection):
    def get(self, role, start=datetime.min, end=datetime.max):
        return super(SummaryCollection, self)\
            .get('crafts/summary',
                 startkey=[role, start.isoformat()],
                 endkey=[role, end.isoformat()])


class RoleCollection(CraftsCollection):
    def get(self, role, start=datetime.min, end=datetime.max):
        return super(RoleCollection, self)\
            .get('crafts/roles',
                 startkey=[role, start.isoformat()],
                 endkey=[role, end.isoformat()])


class MetricCollection(CraftsCollection):
    def get(self, start=datetime.min, end=datetime.max):
        return super(MetricCollection, self)\
            .get('crafts/metrics',
                 startkey=start.isoformat(),
                 endkey=end.isoformat())

    def save(self):
        self._db.update(self.values())

    def add(self, m):
        if m.timestamp not in self:
            self[m.timestamp] = {
                '_id': m.timestamp.isoformat(),
                'type': 'sample',
                'roles': {}}

        doc = self[m.timestamp]['roles']

        if m.role not in doc:
            doc[m.role] = {'stats': {}}

        doc[m.role][m.host] = m.metrics

        for name, metric in m.metrics.items():
            if name not in doc[m.role]['stats']:
                doc[m.role]['stats'][name] = {
                    'count': 0,
                    'sum': 0,
                    'min': metric,
                    'max': 0,
                    'avg': 0,
                    'var': 0}

            stats = doc[m.role]['stats'][name]
            stats['count'] += 1
            stats['sum'] += metric
            stats['min'] = min(stats['min'], metric)
            stats['max'] = max(stats['max'], metric)

            newavg = stats['sum'] / stats['count']
            if stats['count'] > 1:
                stats['var'] = ((stats['count'] - 2) / (stats['count'] - 1)) *\
                    stats['var'] +\
                    (1 / stats['count']) *\
                    (newavg - stats['avg']) ** 2
            else:
                stats['var'] = 0

            stats['avg'] = newavg
