import crafts.scaler

class ARTSScalerDriver(crafts.scaler.ScalerDriver):
   def __init__(self, generator):
      self.generator = generator

   def scale_up(self, role, count):
      self.generator.scale_up(role, count)

   def scale_down(self, role, count):
      self.generator.scale_down(role count)

   def describe_cluster(self):
      return self.generator.describe_cluster()
