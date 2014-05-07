from crafts.common.metrics import AggregateCollection
from crafts.common.metrics import Metric
from crafts.common.metrics import PredictionCollection
from datetime import datetime
from datetime import timedelta


class Predictor(object):
    def predict(self, window, start_time, interval, cycle_size):
        raise NotImplementedError(
            "predict needs to be implemented in subclass")


def make_prediction(db, predictor_cls, role, metric, measure, window_size,
                    cycle_start, interval, cycle_size):
    start = datetime.utcnow() - timedelta(days=window_size)
    window = AggregateCollection(db, role)
    window.get(start)

    predictor = predictor_cls()
    history = [(time, value[metric][measure])
               for time, value in window.items()]
    predictions = predictor.predict(history, cycle_start, interval, cycle_size)

    pc = PredictionCollection(db, role)
    for time, prediction in predictions:
        pc.add(Metric(time, metrics={metric: {measure: prediction}}))

    pc.save()


if __name__ == '__main__':
    from couchdb import Server
    from crafts.predictor.fft import FFTPredictor

    make_prediction(Server()['crafts'], FFTPredictor, 'arts', 'requests',
                    'sum', 7, datetime.utcnow(), 1, 10)
