import sys

from couchdb import Server
from datetime import timedelta
from predictor.fft import FFTPredictor
from tuner import tune

def test_validate(start):
   return tune(Server()['crafts'], 'arts', 'requests', 'sum', start, 7, 7,
         3, FFTPredictor)

if __name__ == '__main__':
   from datetime import datetime

   start = datetime.strptime(sys.argv[1], '%Y-%m-%d')
   print(test_validate(start))
