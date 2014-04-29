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
    prediction = predictor.predict(window, cycle_start, interval, cycle_size)
    return prediction

if __name__ == '__main__':
    from couchdb import Server
    from crafts.predictor.fft import FFTPredictor

    make_prediction(Server()['crafts'], FFTPredictor, 'arts', 'requests', 7, datetime.utcnow(), 1, 10)
