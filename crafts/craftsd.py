#!/usr/bin/env python

import daemon
import imp
import os
import requests
import sys
import time
import urlparse

def usage():
   print('Usage: craftsd <CouchDB-url> <crafts-config>')

def run():
   if len(sys.argv) != 3:
      usage()
      return

   couch_url = urlparse.urlparse(sys.argv[1])
   r = requests.get(couch_url.geturl()+'/'+sys.argv[2])

   r.raise_for_status()

   config = r.json()
   
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
   run()
