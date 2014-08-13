from crafts.common.metrics import AggregateCollection
from crafts.common.metrics import PredictionCollection
from datetime import timedelta
from crafts.predictor import make_prediction
from sklearn.metrics import mean_squared_error
from scipy import optimize
from math import sqrt
from math import isnan

def rmsd(actual, predicted):
    result = sqrt(mean_squared_error(actual, predicted))
    if isnan(result):
        return 0.0
    else:
        return result

class ErrorMatrix(object):
    def __init__(self):
        self.lt_list = ([], [])
        self.gte_list = ([], [])
        self.actual = []
        self.predicted = []
            
    def add(self, actual, predicted):
        assert len(actual) == len(predicted),\
            "actual and predicted lists are not of equal length: {}, {}".format(len(actual), len(predicted))

        self.actual.extend(actual)
        self.predicted.extend(predicted)

    def calculate(self):
        self.lt_list = ([], [])
        self.gte_list = ([], [])

        for i in xrange(len(self.actual)):
            if self.predicted[i] < self.actual[i]:
                self.lt_list[0].append(self.actual[i])
                self.lt_list[1].append(self.predicted[i])
            else:
                self.gte_list[0].append(self.actual[i])
                self.gte_list[1].append(self.predicted[i])

        if len(self.actual) > 0:
            self.lt_percent = len(self.lt_list[0]) / float(len(self.actual))
            self.gte_percent = len(self.gte_list[0]) / float(len(self.actual))
        else:
            self.lt_percent = 0.0
            self.gte_percent = 0.0
        self.lt_rmsd = rmsd(self.lt_list[0], self.lt_list[1])
        self.gte_rmsd = rmsd(self.gte_list[0], self.gte_list[1])
        self.total_rmsd = rmsd(self.actual, self.predicted)

    def __str__(self):
        self.calculate()
        out_str = "Type\tRMSD\t\tPercent\n"
        out_str += "Under\t{}\t{}\n".format(self.lt_rmsd, self.lt_percent)
        out_str += "Over\t{}\t{}\n".format(self.gte_rmsd, self.gte_percent)
        out_str += "Total\t{}".format(self.total_rmsd)

        return out_str

def evaluate(actual_collection, predicted_collection, metric, measure, anomaly=None):
    if anomaly is None:
        actual = [value[metric][measure] for time, value in
                sorted(actual_collection.items())]
        predicted = [value[metric][measure] for time, value in
                sorted(predicted_collection.items())]
        return ((actual, predicted), ([], []))

    anomaly_values = ([], [])
    regular_values = ([], [])
    for time, raw_value in sorted(actual_collection.items()):
        value = raw_value[metric][measure]

        if time > anomaly[0] and time < anomaly[1]:
            anomaly_values[0].append(value)
        else:
            regular_values[0].append(value)
    for time, raw_value in sorted(predicted_collection.items()):
        value = raw_value[metric][measure]

        if time > anomaly[0] and time < anomaly[1]:
            anomaly_values[1].append(value)
        else:
            regular_values[1].append(value)

    return (regular_values, anomaly_values)

def validate(db, role, metric, measure, window_start, window_size, cycle_start, cycle_size,
             interval, num_folds, predictor_cls=None, anomaly=None, save=False):

    regular_err = ErrorMatrix()
    anomaly_err = ErrorMatrix()

    for _ in xrange(num_folds):
        actual_collection = AggregateCollection(db, role)
        actual_collection.get(cycle_start, cycle_start + timedelta(seconds=cycle_size))
        predicted_collection = make_prediction(db, predictor_cls, role, metric,
                measure, window_start, window_size, cycle_start, cycle_size, interval)
        if save:
            predicted_collection.save()

        regular_values, anomaly_values = evaluate(actual_collection,
            predicted_collection, metric, measure, anomaly=anomaly)

        regular_err.add(*regular_values)
        anomaly_err.add(*anomaly_values)

        if cycle_size > 0:
            window_start += timedelta(seconds=cycle_size)
            cycle_start += timedelta(seconds=cycle_size)
        else:
            window_start += timedelta(seconds=interval)
            cycle_start += timedelta(seconds=interval)
    
    regular_err.calculate()
    anomaly_err.calculate()
    return (regular_err, anomaly_err)

def optimization_func(params, db, role, metric, measure, window_start, window_size,
        cycle_start, cycle_size, interval, num_folds, predictor_cls):
    predictor_cls.set_params(params)
    error_matrix = validate(db, role, metric, measure, window_start, window_size,
            cycle_start, cycle_size, interval, num_folds, predictor_cls)[0]
    return error_matrix.total_rmsd

def tune(db, role, metric, measure, window_start, window_size, cycle_start, cycle_size, interval, 
        num_folds, predictor_cls=None):
    return optimize.brute(optimization_func, predictor_cls.param_spec(),
            finish=None, args=(db, role, metric, measure, window_start, window_size,
            cycle_start, cycle_size, interval, num_folds, predictor_cls))
