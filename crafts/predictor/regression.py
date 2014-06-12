from crafts.predictor import Predictor
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import timedelta
from datetime import datetime

class RegressionPredictor(Predictor):
    WIDTH = 300

    @staticmethod
    def set_params(*params):
        RegressionPredictor.WIDTH = params[0]

    @staticmethod
    def get_params():
        return [RegressionPredictor.WIDTH]

    @staticmethod
    def param_spec():
        return [slice(150, 950, 150)]

    def _get_values(self, window, target):
        new_window = []
        for timestamp, value in window:
            if abs(timestamp - target) % 604800 <= RegressionPredictor.WIDTH:
                new_window.append((timestamp, value))

        return new_window

class LinearRegressionPredictor(RegressionPredictor):

    def predict(self, window, start_time, cycle_size, interval):
        predictions = []

        for offset in xrange(0, cycle_size + 1, interval):
            target = start_time + offset
            training = self._get_values(window, target)
            times, values = zip(*training)
            lr = LinearRegression()
            lr.fit(np.array(times)[:,np.newaxis], values)
            prediction = lr.predict(target)

            predictions.append((target, prediction[0]))

        return predictions



class ThielSenPredictor(RegressionPredictor):
    def predict(self, window, start_time, cycle_size, interval):
        predictions = []
        
        for offset in xrange(0, cycle_size + 1, interval):
            target = start_time + offset
            training = self._get_values(window, target)

            slopes = []
            for ida, (time_a, value_a) in enumerate(training):
                for idb, (time_b, value_b) in enumerate(training):
                    slopes.append(value_b - value_a / time_b - value_b)

            slope = sorted(slopes)[len(slopes) / 2]

            lines = []
            for time, value in training:
                lines.append(value - time * slope)

            intercept = sorted(lines)[len(lines) / 2]

            predictions.append((target, target * slope + intercept))

        return predictions
