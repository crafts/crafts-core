import arts.arts as arts
import json
import subprocess
import sys
from couchdb import Server
from crafts.predictor.fft import FFTPredictor
from crafts.predictor.markov import MarkovPredictor
from crafts.predictor.regression import LinearRegressionPredictor
from crafts.predictor.smoothing import ExponentialSmoothingPredictor
from crafts.tuner import tune
from crafts.tuner import validate
from datetime import datetime
from datetime import timedelta

def output_results(result):
    print(result)

    print("LaTeX formatted")
    print("Under & {} & {}\\% \\\\ \\hline".format(
        int(round(result.lt_rmsd)), round(result.lt_percent * 100, 1)))
    print("Over & {} & {}\\% \\\\ \\hline".format(
        int(round(result.gte_rmsd)), round(result.gte_percent * 100, 1)))
    print("Total & {} & \\\\ \\hline".format(
        int(round(result.total_rmsd))))

def evaluate(start, predictor_cls, args, do_tune=False):
    if do_tune:
        optimal = tune(*args, predictor_cls=predictor_cls)

        print(optimal)
        predictor_cls.set_params(optimal)

    results = validate(*args, predictor_cls=predictor_cls, save=True)

    output_results(results)

if __name__ == '__main__':
    from datetime import datetime

    predictor = sys.argv[1]
    do_tune = json.loads(sys.argv[2])
    arts.load(sys.argv[3])
   
    args = [Server()['crafts'], 'arts', 'requests', 'sum']

    if predictor == "Translation":
        start = datetime(2007, 9, 28)
        args.extend([start, 7, start, 604800, 300, 3])
        predictor_cls = FFTPredictor
        FFTPredictor.set_params(0)
    elif predictor == "FFT":
        start = datetime(2007, 9, 28)
        args.extend([start, 7, start, 604800, 300, 3])
        predictor_cls = FFTPredictor
    elif predictor == "Markov":
        start = datetime(2007, 9, 28)
        args.extend([start, 7, start + timedelta(minutes=5), 0, 300, 2016])
        predictor_cls = MarkovPredictor
    elif predictor == "Smoothing":
        start = datetime(2007, 9, 28)
        args.extend([start, 7, start + timedelta(minutes=15), 0, 300, 2016])
        predictor_cls = ExponentialSmoothingPredictor
    elif predictor == "Regression":
        start = datetime(2007, 10, 14)
        args.extend([start, 21, 7, 300, 1])
        predictor_cls = LinearRegressionPredictor

    evaluate(start, predictor_cls, args, do_tune)
