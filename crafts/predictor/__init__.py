class Predictor(object):
   def __init__(self, config):
      self.config = config

   def predict(self, start, stop):
      raise NotImplementedError("predict needs to be implemented in subclass")
