from numpy.fft import fft
from numpy.fft import ifft
from crafts.predictor import Predictor


class FFTPredictor(Predictor):
    PERCENT = 0.96

    @staticmethod
    def set_params(*params):
        FFTPredictor.PERCENT = params[0]

    @staticmethod
    def get_params():
        return [FFTPredictor.PERCENT]

    @staticmethod
    def param_spec():
        return [slice(0.95, 1.00, 0.01)]

    def predict(self, window, start_time, cycle_size, interval):
        times, values = zip(*window)
        freq_dom = fft(values)
        threshold = abs(sorted(freq_dom, key=abs)[int((len(freq_dom) - 1) * FFTPredictor.PERCENT)])

        freq_dom = map(lambda x: 0 if abs(x) < threshold else x, freq_dom)

        new_times = [(time - times[0]) + start_time for time in times]

        prediction = [round(x, 0) for x in ifft(freq_dom)]

        return zip(new_times, prediction)
