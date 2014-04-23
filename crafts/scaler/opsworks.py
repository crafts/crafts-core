import boto.opsworks.layer1
import crafts.scaler
import random

class OpsWorksScalerDriver(crafts.scaler.ScalerDriver):
   STACK = '3f4b80d8-d601-4cd3-a92f-3b784482c99a'

   def __init__(self, config):
      self.config = config
      self.c = boto.opsworks.layer1.OpsWorksConnection()

   def scale_up(self, role, count):
      for i in xrange(count):
         self.c.create_instance(OpsWorksScalerDriver.STACK, role, "t1.micro")
      pass

   def scale_down(self, role, count):
      nodes = self.describe_cluser(role)

      node_ids = [node["id"] for node in random.sample(nodes, count)]

      map(self.c.delete_instance, node_ids)

   def describe_cluster(self, role=None):
      return self.c.describe_instances(OpsWorksScalerDriver.STACK, role)
