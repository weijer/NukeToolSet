#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :heshuai
# mtine       :2015/11/9
# version     :
# usage       :
# notes       :

# Built-in modules
import json
import os
# Third-party modules

# Studio modules

# Local modules


def get_json_data(path):
    if os.path.isfile(path):
        with open(path, 'r') as f:
            data = json.loads(f.read())
            return data
    else:
        return False


def set_json_data(path, data):
    with open(path, 'w') as f:
        json_data = json.dumps(data)
        f.write(json_data)
