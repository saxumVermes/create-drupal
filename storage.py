from io import TextIOWrapper
import json
import os

storage_dir = '.appData'
storage_name = f'{storage_dir}/local.storage.json'

def ensure_dir(func): 
    if not os.path.isdir(storage_dir):
        os.mkdir(storage_dir)
    
    return func


@ensure_dir
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

@ensure_dir
def delete(id: str):
    with open(storage_name, 'r+') as file:
        content = file.read()
        if content:
            content = json.loads(content)

        if not content:
            raise NoDataError('There is nothing to delete')

        del content['sites'][id]

        write_json(file, content)

@ensure_dir
def get(id: str):
    with open(storage_name) as file:
        content = file.read()
        if content:
            all_content = json.loads(content)
            return all_content['sites'].get(id, None)
        
        return None

@ensure_dir
def all():
    with open(storage_name) as file:
        content = file.read()
        if content:
            return json.loads(content)['sites']
        
        return None


def write_json(file: TextIOWrapper, content: dict):
    file.seek(0)
    file.truncate()
    file.write(json.dumps(content))

class NoDataError(Exception):
    pass
