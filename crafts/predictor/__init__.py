from crafts.common.metrics import AggregateCollection
from crafts.common.metrics import Metric
from crafts.common.metrics import PredictionCollection
import calendar
from datetime import datetime
from datetime import timedelta


class Predictor(object):
    def predict(self, window, start_time, cycle_size, interval):
        raise NotImplementedError(
            "predict needs to be implemented in subclass")


def make_prediction(db, predictor_cls, role, metric, measure,
                    window_start, window_size,
                    cycle_start, cycle_size, interval):
    start = window_start - timedelta(days=window_size)
    window = AggregateCollection(db, role)
    window.get(start, window_start)

    predictor = predictor_cls()
    history = [(calendar.timegm(time.timetuple()), value[metric][measure])
               for time, value in sorted(window.items())]
    predictions = predictor.predict(history, calendar.timegm(cycle_start.timetuple()), cycle_size, interval)

    pc = PredictionCollection(db, role)
    for time, prediction in predictions:
        pc.add(Metric(datetime.utcfromtimestamp(time), metrics={metric: {measure: prediction}}))

    return pc


if __name__ == '__main__':
    import sys
    from couchdb import Server
    from crafts.predictor.fft import FFTPredictor
    from crafts.predictor.markov import MarkovPredictor

    start = datetime.strptime(sys.argv[1], '%Y-%m-%d')

    pc = make_prediction(Server()['crafts'], MarkovPredictor, 'arts', 'requests',
            'sum', start, 7, start, 7, 5)
    pc.save()
