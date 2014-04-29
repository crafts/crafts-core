from crafts.common import metrics
from datetime import datetime
from datetime import timedelta

class Predictor(object):
    def predict(self, window, start_time, interval, cycle_size):
        raise NotImplementedError("predict needs to be implemented in subclass")

def make_prediction(db, predictor_cls, role, metric, window_size, cycle_start,
        interval, cycle_size):
    start = datetime.utcnow() - timedelta(days=window_size)
    window = metrics.PredictionCollection(db)
    window.get(role, metric, start)

    predictor = predictor_cls()
    return predictor.predict(window, cycle_start, interval, cycle_size)

if __name__ == '__main__':
    from couchdb import Server
    from crafts.predictor.lame import LamePredictor

    print make_prediction(Server()['crafts'], LamePredictor, 'arts', 'requests', 7, datetime.utcnow(), 1, 10)
