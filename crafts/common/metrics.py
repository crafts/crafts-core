from bisect import bisect_left
from couchdb import Server
from datetime import datetime


class Metric(dict):
    def __init__(self, timestamp, host="ALL", metrics={}):
        self.timestamp = timestamp
        self.host = host
        self.metrics = metrics
        super(Metric, self).__init__(metrics)


class CraftsCollection(dict):
    def __init__(self, db, role):
        self._db = db
        self.role = role

        super(CraftsCollection, self).__init__()

    def find_nearest(self, dt):
        pos = bisect_left(sorted(self.keys()), dt)

        return self[self.keys()[pos]]

    def get(self, view, start=datetime.min, end=datetime.max):
        result = self._db.view(view,
                               startkey=[self.role, start.isoformat()],
                               endkey=[self.role, end.isoformat()])

        self.update(dict([(datetime.strptime(
            doc.key[1], '%Y-%m-%dT%H:%M:%S'),
            doc.value) for doc in result]))


class AggregateCollection(CraftsCollection):
    def get(self, start=datetime.min, end=datetime.max):
        super(AggregateCollection, self).get('crafts/aggregates',
                                             start, end)


class PredictionCollection(CraftsCollection):
    def get(self, start=datetime.min, end=datetime.max):
        super(PredictionCollection, self).get('crafts/predictions',
                                             start, end)

    def save(self):
        docs = []
        for time, predictions in self.items():
            doc = {
                '_id': '{}/{}/prediction'.format(self.role, time.isoformat()),
                'role': self.role,
                'timestamp': time.isoformat(),
                'type': 'prediction',
                'predictions': predictions
            }
            docs.append(doc)

        self._db.update(docs)

    def add(self, p):
        if p.timestamp not in self:
            self[p.timestamp] = {}

        self[p.timestamp].update(p.metrics)


class MetricCollection(CraftsCollection):
    def get(self, start=datetime.min, end=datetime.max):
        super(AggregateCollection, self).get('crafts/samples',
                                             start, end)

    def save(self,):
        docs = []
        for time, hosts in self.items():
            doc = {
                '_id': '{}/{}/sample'.format(self.role, time.isoformat()),
                'role': self.role,
                'timestamp': time.isoformat(),
                'type': 'sample',
                'hosts': hosts
            }
            docs.append(doc)

        self._db.update(docs)

    def add(self, m):
        if m.timestamp not in self:
            self[m.timestamp] = {}

        if m.host not in self[m.timestamp]:
            self[m.timestamp][m.host] = {}

        self[m.timestamp][m.host].update(m.metrics)
