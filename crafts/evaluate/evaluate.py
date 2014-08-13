import arts.arts as arts
import json
import subprocess
import sys
from couchdb import Server
from crafts.predictor.fft import FFTPredictor
from crafts.predictor.markov import MarkovPredictor
from crafts.predictor.regression import ThielSenPredictor
from crafts.predictor.smoothing import ExponentialSmoothingPredictor
from crafts.tuner import tune
from crafts.tuner import validate
from datetime import datetime
from datetime import timedelta

def output_results(result, anomaly=None):

    if anomaly is None:
        print("Under & {} & {}\\% \\\\ \\hline".format(
            int(round(result.lt_rmsd)), round(result.lt_percent * 100, 1)))
        print("Over & {} & {}\\% \\\\ \\hline".format(
            int(round(result.gte_rmsd)), round(result.gte_percent * 100, 1)))
        print("Total & {} & \\\\ \\hline".format(
            int(round(result.total_rmsd))))
    else:
        print("Under & {} & {}\\% & {} & {}\\% \\\\ \\hline".format(
            int(round(result.lt_rmsd)), round(result.lt_percent * 100, 1),
            int(round(anomaly.lt_rmsd)), round(anomaly.lt_percent * 100, 1)))
        print("Over & {} & {}\\% & {} & {}\\% \\\\ \\hline".format(
            int(round(result.gte_rmsd)), round(result.gte_percent * 100, 1),
            int(round(anomaly.gte_rmsd)), round(anomaly.gte_percent * 100, 1)))
        print("Total & {} & & {} & \\\\ \\hline".format(
            int(round(result.total_rmsd)),
            int(round(anomaly.total_rmsd))))

def evaluate(start, predictor_cls, args, anomaly, do_tune=False):
    if do_tune:
        optimal = tune(*args, predictor_cls=predictor_cls)

        print(optimal)
        predictor_cls.set_params(optimal)

    regular_results, anomaly_results = validate(*args, predictor_cls=predictor_cls, anomaly=anomaly, save=True)

    output_results(regular_results, anomaly_results)

if __name__ == '__main__':
    from datetime import datetime

    predictor = sys.argv[1]
    do_tune = json.loads(sys.argv[2])
    arts.load(sys.argv[3])
       
    args = [Server()['crafts'], 'arts', 'requests', 'sum']
    start = datetime(2007, 10, 14, tzinfo=None)

    if predictor == "Translation":
        args.extend([start, 7, start, 604800, 300, 1])
        predictor_cls = FFTPredictor
        FFTPredictor.set_params(0)
    elif predictor == "FFT":
        args.extend([start, 7, start, 604800, 300, 1])
        predictor_cls = FFTPredictor
    elif predictor == "Markov":
        args.extend([start, 7, start + timedelta(minutes=15), 0, 300, 2016])
        predictor_cls = MarkovPredictor
    elif predictor == "Smoothing":
        args.extend([start, 1, start + timedelta(minutes=15), 0, 300, 2016])
        predictor_cls = ExponentialSmoothingPredictor
    elif predictor == "Regression":
        args.extend([start, 21, start, 604800, 300, 1])
        predictor_cls = ThielSenPredictor

    evaluate(start, predictor_cls, args, (datetime(2007, 10, 19, 17, tzinfo=None), datetime(2007, 10, 19, 17, 15, tzinfo=None)), do_tune)
