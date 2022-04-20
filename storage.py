from io import TextIOWrapper
import json
import os

storage_dir = '.appData'
storage_name = f'{storage_dir}/local.storage.json'

def ensure_storage(func): 
    if not os.path.isdir(storage_dir):
        os.mkdir(storage_dir)
    
    if not os.path.isfile(storage_name):
        with open(storage_name, 'w') as file:
            file.write(json.dumps({'sites': {}}))

    return func


@ensure_storage
def upsert(id: str, value: dict):
    with open(storage_name, 'r+') as file:
        content = file.read()
        if content:
            content = json.loads(content)
        else:
            content = {}

        content['sites'][id] = value

        file.seek(0)
        file.truncate()
        file.write(json.dumps(content))

@ensure_storage
def delete(id: str):
    with open(storage_name, 'r+') as file:
        content = file.read()
        if content:
            content = json.loads(content)

        if not content:
            raise NoDataError('There is nothing to delete')

        del content['sites'][id]

        write_json(file, content)

@ensure_storage
def get(id: str):
    with open(storage_name) as file:
        content = file.read()
        if content:
            all_content = json.loads(content)
            return all_content['sites'].get(id, None)
        
        return None

@ensure_storage
def all():
    with open(storage_name) as file:
        content = file.read()
        if not content:
            return None

        content = json.loads(content)['sites']
        
        return None if len(content) == 0 else content


def write_json(file: TextIOWrapper, content: dict):
    file.seek(0)
    file.truncate()
    file.write(json.dumps(content))

class NoDataError(Exception):
    pass
