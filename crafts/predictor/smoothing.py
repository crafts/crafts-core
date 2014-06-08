from crafts.predictor import Predictor

class ExponentialSmoothingPredictor(Predictor):
    ALPHA = 0.6
    BETA = 0.3

    @staticmethod
    def set_params(params):
        ExponentialSmoothingPredictor.ALPHA = float(params[0])
        ExponentialSmoothingPredictor.BETA = float(params[1])


    @staticmethod
    def get_params():
        return [ExponentialSmoothingPredictor.ALPHA,
                ExponentialSmoothingPredictor.BETA]

    @staticmethod
    def param_spec():
        return [slice(0.3, 0.7, 0.1), slice(0.3, 0.7, 0.1)]

    def predict(self, window, start_time, cycle_size, interval):
        alpha = ExponentialSmoothingPredictor.ALPHA
        beta = ExponentialSmoothingPredictor.BETA

        times, values = zip(*window)

        s_t = window[1][1]
        b_t = window[1][1] - window[0][1]
        for value in values[2:]:
            s_tp = s_t
            s_t = alpha * value + (1 - alpha) * (s_t + b_t)
            b_t = beta * (s_t - s_tp) + (1 - beta) * b_t

        ticks = (start_time - times[-1]) / interval
        prediction = s_t + ticks * b_t

        return [(start_time, prediction)]
