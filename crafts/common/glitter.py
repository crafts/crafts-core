import logging

class GlitterHandler(logging.Handler):
   def __init__(self, host='localhost', port=5984,
         db='logs', user=None, password=None):

      auth = ''
      if user is not None and password is not None:
         auth = '{user}:{password}@'.format(user=user, password=password)

      self.couch_url = 'http://{auth}{host}:{port}/{db}'.format(
            auth=auth, host=host, port=port, db=db)

      super(GlitterHandler, self).__init__()

   def emit(self, record):
      try:
         import json
         import requests

         doc = record.__dict__
         headers = {'content-type': 'application/json'}
         res = requests.post(self.couch_url, json.dumps(doc), headers=headers);
         if 'error' in res.json():
            if res.json()['error'] == 'unauthorized':
               raise IOError('Authentication Failed')
            else:
               raise IOError(res.json())
      except (KeyboardInterrupt, SystemExit):
         raise
      except:
         self.handleError(record)
