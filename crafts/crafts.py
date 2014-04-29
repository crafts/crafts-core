#!/usr/bin/env python

'''
Crafts

Usage:
        crafts init <config-file> [<attachments>...] [options]
        crafts clear [options]
        crafts -h

Options:
        -h --help       Show this screen.
        --version       Show version.
        -H url          CouchDB url [default: http://localhost:5984/]
        -D db           CouchDB database [default: crafts]
'''
from docopt import docopt
from couchdb.client import Server
from glob import glob
import json
import os

_here = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    args = docopt(__doc__, version='Crafts 0.1')

    couch = Server(args['-H'])

    if args['init']:
        db = couch.create(args['-D'])
        design = {
                '_id': '_design/crafts',
                'language': 'coffeescript',
                'views': {}}

        for script_file in glob(os.path.join(_here, 'views', '*.coffee')):
            base = os.path.basename(script_file)
            view_name = os.path.splitext(base)[0]
            with open(script_file) as script:
                design['views'][view_name] = {'map': script.read()}

        db.save(design)

        with open(args['<config-file>']) as config_file:
            config = json.load(config_file)
            config['_id'] = 'config'
            (doc_id, rev_id) = db.save(config)
            for attachment_file in args['<attachments>']:
                with open(attachment_file) as attachment:
                    db.put_attachment({'_id':doc_id, '_rev':rev_id}, attachment)
    elif args['clear']:
        del couch[args['-D']]
