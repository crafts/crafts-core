from crafts.predictor import Predictor
from sklearn.linear_model import LinearRegression

class LinearRegressionPredictor(Predictor):
    def predict(self, window, start_time, cycle_size):
        times, values = zip(*window)

        for _ in xrange(cycle_size):

        lr = LinearRegression()
        lr.fit(times, values)

class ThielSenPredictor(Predictor):
    def predict(self, window, start_time, cycle_size):
        pass
