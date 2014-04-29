import logging

class GlitterHandler(logging.Handler):
   def __init__(self, url='http://localhost:5984/', db='logs'):
      from couchdb import Server

      self.db = Server(url)[db]

      super(GlitterHandler, self).__init__()

   def emit(self, record):
      try:
         self.db.save(record.__dict__)
      except (KeyboardInterrupt, SystemExit):
         raise
      except:
         self.handleError(record)
