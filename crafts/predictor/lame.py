from datetime import timedelta
import crafts.predictor


class LamePredictor(crafts.predictor.Predictor):
    def predict(self, window, start_time, interval, cycle_size):
        predictions = []

        for offset in xrange(0, cycle_size * interval, interval):
            time = start_time + timedelta(minutes=offset)

            result = window.find_nearest(time - timedelta(weeks=1))

            predictions.append(result['avg'])

        return predictions
