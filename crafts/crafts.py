#!/usr/bin/env python

'''
Crafts

Usage:
        crafts init <config-file> [<attachments>...] [options]
        crafts update [options]
        crafts clear [options]
        crafts -h

Options:
        -h --help       Show this screen.
        --version       Show version.
        -H url          CouchDB url [default: http://localhost:5984/]
        -D db           CouchDB database [default: crafts]
'''
from docopt import docopt
from couchdb import Server
from glob import glob
import json
import os

_here = os.path.dirname(os.path.realpath(__file__))


def update_design(db):
    design = {
        '_id': '_design/crafts',
        'language': 'coffeescript',
        'views': {},
        'lists': {}}

    old_design = db.get('_design/crafts')
    if old_design is not None:
        design['_rev'] = old_design['_rev']

    for script_file in glob(os.path.join(_here, 'couch', 'views', '*.coffee')):
        base = os.path.basename(script_file)
        view_name = os.path.splitext(base)[0]
        with open(script_file) as script:
            design['views'][view_name] = {'map': script.read()}

    for script_file in glob(os.path.join(_here, 'couch', 'lists', '*.coffee')):
        base = os.path.basename(script_file)
        view_name = os.path.splitext(base)[0]
        with open(script_file) as script:
            design['lists'][view_name] = script.read()

    db.save(design)


if __name__ == '__main__':
    args = docopt(__doc__, version='Crafts 0.1')

    couch = Server(args['-H'])

    if args['init']:
        db = couch.create(args['-D'])

        with open(args['<config-file>']) as config_file:
            config = json.load(config_file)
            config['_id'] = 'config'
            (doc_id, rev_id) = db.save(config)
            for attachment_file in args['<attachments>']:
                with open(attachment_file) as attachment:
                    db.put_attachment({'_id': doc_id, '_rev': rev_id},
                                      attachment)

    if args['init'] or args['update']:
        db = couch[args['-D']]
        update_design(db)

    elif args['clear']:
        del couch[args['-D']]
