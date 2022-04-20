import json
import os

from storage import storage_name, write_json


def select(id):
    with open(storage_name, 'r+') as file:
        content = file.read()
        if not content:
            content = {}
            content['active'] = id
        
        content = json.loads(content)
        content['active'] = id
        write_json(file, content)


def active():
    with open(storage_name, 'r+') as file:
        content = file.read()
        if not content:
            raise ValueError('no active ')
        content = json.loads(content)
        return content['active']
