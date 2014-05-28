from crafts.common.metrics import AggregateCollection
from crafts.common.metrics import Metric
from crafts.common.metrics import PredictionCollection
from datetime import datetime
from datetime import timedelta


class Predictor(object):
    def predict(self, window, start_time, cycle_size):
        raise NotImplementedError(
            "predict needs to be implemented in subclass")


def make_prediction(db, predictor_cls, role, metric, measure,
                    window_start, window_size,
                    cycle_start, cycle_size):
    start = window_start - timedelta(days=window_size)
    window = AggregateCollection(db, role)
    window.get(start, window_start)

    predictor = predictor_cls()
    history = [(time, value[metric][measure])
               for time, value in sorted(window.items())]
    predictions = predictor.predict(history, cycle_start, cycle_size)

    pc = PredictionCollection(db, role)
    for time, prediction in predictions:
        pc.add(Metric(time, metrics={metric: {measure: prediction}}))

    return pc


if __name__ == '__main__':
    import sys
    from couchdb import Server
    from crafts.predictor.fft import FFTPredictor

    start = datetime.strptime(sys.argv[1], '%Y-%m-%d')

    pc = make_prediction(Server()['crafts'], FFTPredictor, 'arts', 'requests',
            'sum', start, 7, start, 7)
    pc.save()
