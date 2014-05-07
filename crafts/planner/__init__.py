from crafts.scaler.null import NullScaler
import math


class Planner(object):
    pass


def build_plan(predictions, throughput, scaler=NullScaler()):
    capacity = map(lambda p: math.ceil(p/throughput), predictions)

    print capacity
