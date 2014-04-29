class MALDriver(object):
    def get_metrics(self, start, stop):
        raise NotImplementedError(
            "get_metrics needs to be implemented in subclass")
