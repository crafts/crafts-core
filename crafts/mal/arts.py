class ARTSMALDriver(crafts.mal.MALDriver):
   def __init__(self, generator=None):
      self.generator = generator

   def get_metrics(self, start, stop):
      self.generator.get_metrics(start, stop)
