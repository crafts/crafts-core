from common.metrics import AggregateCollection
from common.metrics import PredictionCollection
from datetime import timedelta
from predictor import make_prediction
from sklearn.metrics import mean_squared_error
from scipy import optimize
from math import sqrt

def rmsd(actual, predicted):
    return sqrt(mean_squared_error(actual, predicted))

class ErrorMatrix(object):
    def __init__(self, actual, predicted):
        assert len(actual) == len(predicted), "actual and predicted lists are not of equal length"

        lt_list = ([], [])
        gte_list = ([], [])
        for i in xrange(len(actual)):
            if predicted[i] < actual[i]:
                lt_list[0].append(actual[i])
                lt_list[1].append(predicted[i])
            else:
                gte_list[0].append(actual[i])
                gte_list[1].append(predicted[i])

        self.lt_rmsd = rmsd(lt_list[0], lt_list[1])
        self.lt_percent = len(lt_list[0]) / float(len(actual))
        self.gte_rmsd = rmsd(gte_list[0], gte_list[1])
        self.gte_percent = len(gte_list[0]) / float(len(actual))
        self.total_rmsd = rmsd(actual, predicted)

    def __str__(self):
        out_str = "Type\tRMSD\t\tPercent\n"
        out_str += "Under\t{}\t{}\n".format(self.lt_rmsd, self.lt_percent)
        out_str += "Over\t{}\t{}\n".format(self.gte_rmsd, self.gte_percent)
        out_str += "Total\t{}".format(self.total_rmsd)

        return out_str

def evaluate(actual_collection, predicted_collection, metric, measure):
    actual = [value[metric][measure] for time, value in
            sorted(actual_collection.items())]
    predicted = [value[metric][measure] for time, value in
            sorted(predicted_collection.items())]

    return ErrorMatrix(actual, predicted)

def validate(db, role, metric, measure, start, window_size, cycle_size,
             num_folds, predictor_cls):

    err = []
    for _ in xrange(num_folds):
        actual_collection = AggregateCollection(db, role)
        actual_collection.get(start, start + timedelta(days=cycle_size))
        predicted_collection = make_prediction(db, predictor_cls, role, metric,
                measure, start, window_size, start, cycle_size)
        err.append(evaluate(actual_collection, predicted_collection, metric,
            measure))
        start += timedelta(days=cycle_size)
    
    return err

def optimization_func(params, db, role, metric, measure, start, window_size,
        cycle_size, num_folds, predictor_cls):
    predictor_cls.set_params(params)
    error_matrices = validate(db, role, metric, measure, start, window_size,
            cycle_size, num_folds, predictor_cls)
    result = sum([em.total_rmsd for em in error_matrices]) / len(error_matrices)
    print("RMSD for {}: {}".format(params, result))
    return result

def tune(db, role, metric, measure, start, window_size, cycle_size, num_folds,
        predictor_cls):
    return optimize.brute(optimization_func, predictor_cls.param_spec(),
            finish=None, args=(db, role, metric, measure, start, window_size,
            cycle_size, num_folds, predictor_cls))
