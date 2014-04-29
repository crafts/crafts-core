from collections import defaultdict
import crafts.scaler
import uuid

class NullScaler(crafts.scaler.ScalerDriver):
    def __init__(self, cluster=defaultdict(list)):
        self.cluster = cluster

    def scale_up(self, role, count):
        for _ in xrange(count):
            self.cluster[role].append(str(uuid.uuid4()))

    def scale_down(self, role, count):
        self.cluster[role] = self.cluster[role][:-count]

    def describe_cluster(self):
        return self.cluster
