class ScalerDriver(object):
    def scale_up(self, role, count):
        raise NotImplementedError(
            "scale_up needs to be implemented in subclass")

    def scale_down(self, role, count):
        raise NotImplementedError(
            "scale_down needs to be implemented in subclass")

    def describe_cluster(self):
        raise NotImplementedError(
            "describe_cluster needs to be implemented in subclass")
