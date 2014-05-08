from numpy.fft import fft
from numpy.fft import ifft
from crafts.predictor import Predictor


class FFTPredictor(Predictor):
    def predict(self, window, start_time, interval, cycle_size):
        times, values = zip(*window)
        freq_dom = fft(values)
        print(freq_dom)
        freq_dom = map(lambda x: x if abs(x) > 500 else 0, freq_dom)

        new_times = [(time - times[0]) + start_time for time in times]

        prediction = [round(x, 0) for x in ifft(freq_dom)]

        return zip(new_times, prediction)
