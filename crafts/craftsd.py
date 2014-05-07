#!/usr/bin/env python

from couchdb import Server
import daemon
import imp
import os
import logging
import logging.config
import sys
import tempfile
import time
import urlparse


def usage():
    print('Usage: craftsd <CouchDB-url> <db-name> <crafts-config>')


def run(raw_url, db_name, config_doc):
    db = Server(raw_url)[db_name]
    config = db.get(config_doc)

    if 'logger' in config:
        log_stream = db.get_attachment(config_doc, config['logger'])
        logging_conf = tempfile.NamedTemporaryFile(delete=False)
        logging_conf.write(log_stream.read())
        logging_conf.close()
        logging.config.fileConfig(logging_conf.name)
        os.unlink(logging_conf.name)

    def get_component(name):
        components = name.split('.')
        mod = __import__('.'.join(components[:-1]))
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod()

    maldriver = get_component(config['maldriver'])
    predictor = get_component(config['predictor'])
    planner = get_component(config['planner'])
    scaler = get_component(config['scaler'])

    with daemon.DaemonContext():
        pass

if __name__ == '__main__':
    if len(sys.argv) != 4:
        usage()
    else:
        run(sys.argv[1], sys.argv[2], sys.argv[3])
