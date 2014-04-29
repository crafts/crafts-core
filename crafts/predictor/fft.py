from numpy.fft import fft
from numpy.fft import ifft
from crafts.predictor import Predictor


class FFTPredictor(Predictor):
    def predict(self, window, start_time, interval, cycle_size):
        history = [value['avg'] for value in window]
        history[50] = 0

        freq_dom = fft(history)
        print(freq_dom)
        freq_dom = map(lambda x: x if abs(x) > 500 else 0, freq_dom)

        prediction = [round(x, 0) for x in ifft(freq_dom)]
        print(sum([(a - b) ** 2 for (a, b) in zip(prediction, history)]) /
              len(history))

        return prediction
