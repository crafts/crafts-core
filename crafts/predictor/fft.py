from numpy.fft import fft
from numpy.fft import ifft
from crafts.predictor import Predictor


class FFTPredictor(Predictor):
    PERCENT = 0.5

    @staticmethod
    def set_params(*params):
        FFTPredictor.PERCENT = params[0]

    @staticmethod
    def get_params():
        return [FFTPredictor.PERCENT]

    @staticmethod
    def param_spec():
        return [slice(0.0, 1.05, 0.05)]

    def predict(self, window, start_time, cycle_size):
        times, values = zip(*window)
        freq_dom = fft(values)
        top_freqs = sorted(freq_dom)[:int(len(freq_dom) * FFTPredictor.PERCENT)]
        top_freqs.append(freq_dom[0])
        freq_dom = map(lambda x: x if x in top_freqs else 0, freq_dom)

        new_times = [(time - times[0]) + start_time for time in times]

        prediction = [round(x, 0) for x in ifft(freq_dom)]

        return zip(new_times, prediction)
