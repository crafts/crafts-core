#!/usr/bin/env python

import daemon
import imp
import os
import requests
import logging
import logging.config
import sys
import tempfile
import time
import urlparse

def usage():
   print('Usage: craftsd <CouchDB-url> <crafts-config>')

def run(raw_url, config_doc):
   couch_url = urlparse.urlparse(raw_url)
   r = requests.get(couch_url.geturl()+'/'+config_doc)

   r.raise_for_status()

   config = r.json()

   if 'logger' in config:
      r = requests.get(couch_url.geturl()+'/'+config_doc+'/'+config['logger'])
      logging_conf = tempfile.NamedTemporaryFile(delete=False)
      logging_conf.write(r.text)
      logging_conf.close()
      logging.config.fileConfig(logging_conf.name)
      os.unlink(logging_conf.name)
   
   def get_component(name):
      components = name.split('.')
      mod = __import__('.'.join(components[:-1]))
      for comp in components[1:]:
         mod = getattr(mod, comp)
      return mod(config)

   maldriver = get_component(config['maldriver'])
   predictor = get_component(config['predictor'])
   planner   = get_component(config['planner'])
   scaler    = get_component(config['scaler'])

   with daemon.DaemonContext():
      pass

if __name__ == '__main__':
   if len(sys.argv) != 3:
      usage()
   else:
      run(sys.argv[1], sys.argv[2])
