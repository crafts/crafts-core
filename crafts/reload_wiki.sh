#!/usr/bin/env sh

~/thesis/crafts-core/crafts/crafts-cli.py clear -H http://andrew:password@localhost:5984/
~/thesis/crafts-core/crafts/crafts-cli.py init config/config.json -H http://andrew:password@localhost:5984/
~/thesis/arts/arts/arts.py load ~/thesis/data/wiki/output/part-0000* -H handlers.CraftsHandler
