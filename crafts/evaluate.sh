#!/usr/bin/env sh

~/thesis/crafts-core/crafts/crafts-cli.py clear -H http://localhost:5984/
~/thesis/crafts-core/crafts/crafts-cli.py init config/config.json -H http://localhost:5984/
python evaluate/evaluate.py $@
