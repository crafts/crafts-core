from crafts.predictor import Predictor
from datetime import timedelta
import numpy as np

class MarkovPredictor(Predictor):
    NUM_BUCKETS = 75

    @staticmethod
    def set_params(*params):
        MarkovPredictor.NUM_BUCKETS = int(params[0])

    @staticmethod
    def get_params():
        return MarkovPredictor.NUM_BUCKETS

    @staticmethod
    def param_spec():
        return [slice(50, 100, 5)]

    def predict(self, window, start_time, cycle_size, interval):
        time, values = zip(*window)
        max_val = max(values)
        min_val = min(values)

        bucket_width = (max_val - min_val) / MarkovPredictor.NUM_BUCKETS

        p_matrix = np.zeros(shape=(MarkovPredictor.NUM_BUCKETS, MarkovPredictor.NUM_BUCKETS))

        def clamp(value):
            return min(max(0, value), MarkovPredictor.NUM_BUCKETS - 1)

        for idx in xrange(len(values) - 2):
            start_bucket = clamp((values[idx] - min_val) / bucket_width)
            end_bucket = clamp((values[idx + 1] - min_val) / bucket_width)

            try:
                p_matrix[start_bucket][end_bucket] += 1
            except IndexError as e:
                pass
                #print(start_bucket, end_bucket)

        for idx in xrange(len(p_matrix)):
            p_matrix[idx] = map(lambda x: x / len(values), p_matrix[idx])

        p_matrix = np.matrix(p_matrix)
        ticks = (start_time - max(time)) / interval

        p_future = p_matrix ** ticks
        current_bucket = clamp((values[-1] - min_val) / bucket_width)
        new_bucket = p_future[current_bucket].argmax()

        prediction = min_val + (new_bucket * bucket_width)

        return [(start_time, prediction)]
