import json
import requests

class MALDriver(object):
   def __init__(self, config):
      self.config = config

   def get_metrics(self, *args, **kwargs):
      raise NotImplementedError("get_metrics needs to be implemented in subclass")

def insert_metrics(metrics):
   '''
   Inserted metrics must be of the form specified in docs/mal/stat-example.json
   '''

   print(metrics)

   def format_id(metric):
      metric["_id"] = metric["host"]+"/"+metric["timestamp"]
      return metric

   map(format_id, metrics)
   data = {"docs": metrics}
   headers = {'content-type': 'application/json'}
   r = requests.post("http://localhost:5984/crafts/_bulk_docs", json.dumps(data), headers=headers);
