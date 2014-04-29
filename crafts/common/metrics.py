from couchdb import Server 

class Metric(dict):
    def __init__(self, timestamp, role, host, metrics={}):
        self.timestamp = timestamp
        self.role = role
        self.host = host
        self.metrics = metrics
        super(Metric, self).__init__(metrics)

class MetricCollection(dict):
    def __init__(self, db):
        self._db = db

        super(MetricCollection, self).__init__()

    def save(self):
        docs = []
        for timestamp, sample in self.items():
            docs.append({
                '_id': str(timestamp),
                'type': 'sample',
                'roles': sample})
        
        self._db.update(docs)

    def add(self, m):
        if m.timestamp not in self:
            self[m.timestamp] = {}

        if m.role not in self[m.timestamp]:
            self[m.timestamp][m.role] = {'stats': {}}

        self[m.timestamp][m.role][m.host] = m.metrics

        for name, metric in m.metrics.items():
            if name not in self[m.timestamp][m.role]['stats']:
                self[m.timestamp][m.role]['stats'][name] = {
                        'count': 0,
                        'sum': 0,
                        'min': metric,
                        'max': 0,
                        'avg': 0,
                        'var': 0}

            stats = self[m.timestamp][m.role]['stats'][name]
            stats['count'] += 1
            stats['sum'] += metric
            stats['min'] = min(stats['min'], metric)
            stats['max'] = max(stats['max'], metric)

            newavg = stats['sum'] / stats['count']
            if stats['count'] > 1:
                stats['var'] = ((stats['count'] - 2) / (stats['count'] - 1)) * stats['var'] +\
                        (1 / stats['count']) * (newavg - stats['avg']) ** 2
            else:
                stats['var'] = 0

            stats['avg'] = newavg

