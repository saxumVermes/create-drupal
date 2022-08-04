#!/usr/bin/env python3
from genericpath import isdir
import os
import subprocess
import sys
import pty

from argparse import ArgumentParser
from typing import Tuple
from pkg_resources import ensure_directory
from prettytable import PrettyTable
import yaml
from model import Site

import storage
import storage_decorator
from config import config


SUCCESS = 0
NO_DATA_ERROR = 1
COMPOSE_ERROR = 2
SKIPPED = 18

NGROK_DIR = '.appData/ngrok'

def select(args) -> int:
    id = args['project_name']
    info = storage.get(id)
    if not info:
        print('No such site')
        return NO_DATA_ERROR

    with open('stack/.env', 'w') as file:
        content = f'''MYSQL_ROOT_PASSWORD=mysql
MYSQL_USER=drupal
MYSQL_PASSWORD=drupal
MYSQL_ROOT_HOST=%
MYSQL_DATABASE=main

# docker-compose project name
COMPOSE_PROJECT_NAME={id}
HOSTNAME={id}

NGINX_PORT={info['nginx_port']}
MYSQL_PORT={info['mysql_port']}

GIT_USER_NAME={config['git']['user']['name']}
GIT_USER_EMAIL={config['git']['user']['email']}
'''

        file.seek(0)
        file.write(content)

        storage_decorator.select(id)


def register_site(args) -> int:
    id = args['project_name']
    nginx_port = args.get('nginx_port')
    mysql_port = args.get('mysql_port')
    ngrok_subdomain = args.get('ngrok_subdomain')

    if not nginx_port:
        nginx_port = input('Please provide an nginx port: ')

    if not mysql_port:
        mysql_port = input('Please provide a mysql port: ') 
    
    ngrok_subdomain =  ngrok_subdomain if ngrok_subdomain else id
    storage.upsert(id, {
        'nginx_port': nginx_port,
        'mysql_port': mysql_port,
        'ngrok_subdomain': ngrok_subdomain,
    })

    select({'project_name': id})

    if ngrok_subdomain:
        insert_ngrok_data(Site(nginx_port, mysql_port, id, 'localhost', ngrok_subdomain))

    return SUCCESS


def describe(args) -> int:
    id = args['project_name']
    info = storage.get(id)
    if info is None:
        print('No data')
        return NO_DATA_ERROR

    table = PrettyTable()
    table.add_column('Drupal ID', [id])
    table.add_column('Nginx Port',[info['nginx_port']])
    table.add_column('Mysql Port', [info['mysql_port']])

    print(table.get_string())
    return SUCCESS
    

def list_sites(args):
    all = storage.all()
    if all is None:
        print('No data')
        return NO_DATA_ERROR

    table = PrettyTable()
    data = {
        'id': [],
        'np': [],
        'mp': [],
        'ns': [],
    }
 
    active = storage_decorator.active()
    for name, ports in all.items():
        fname = name
        if active == name:
            fname = '* '+name
        data['id'].append(fname)
        data['np'].append(ports['nginx_port'])
        data['mp'].append(ports['mysql_port'])
        domain = 'http(s)://{}.ngrok.io'
        subdomain = ports['ngrok_subdomain'] if ports.get('ngrok_subdomain') else name
        data['ns'].append(domain.format(subdomain))

    table.add_column('Drupal ID', data['id'])
    table.add_column('Nginx Port', data['np'])
    table.add_column('Mysql Port', data['mp'])
    table.add_column('Ngrok Domain', data['ns'])


    print(table.get_string())
    return SUCCESS


def delete_site(args):
    id = args['project_name']
    id = args['project_name']
    info = storage.get(id)
    if not info:
        print('There is nothing to delete')
        return NO_DATA_ERROR

    select(args)
    exit_code, message = compose(['down', '-v'])
    storage.delete(id)
    print(f'[INFO] docker-compose output: {message}')
    
    print(f'Stack with id {id} has been deleted')
    return SUCCESS


def insert_ngrok_data(site: Site):
    if not os.path.isdir(NGROK_DIR):
        os.mkdir(NGROK_DIR)
    with open(NGROK_DIR + '/ngrok.yml', 'r+') as f:
        content = f.read()
        content = yaml.load(content, Loader=yaml.SafeLoader)
        if not content:
            raise MissingNgrokCredentialsError()
        content['tunnels'] = {
            site.name: {
                'proto': 'http',
                'addr': site.getHostAndPort(),
                'subdomain': site.domain,
            }
        }
        f.seek(0)
        f.write(yaml.dump(content))


def compose(args) -> Tuple[int, str]:
    command = ['docker-compose', '-f', 'stack/docker-compose.yaml']
    if args:
        command.extend(args)

    process = subprocess.Popen(command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    
    if stderr:
        return COMPOSE_ERROR, stderr.decode('utf-8')

    return SUCCESS, stdout.decode('utf-8')


def enter(args):
    service = args['service']
    command = ['docker-compose', '-f', 'stack/docker-compose.yaml', 'exec', '-e', 'COLUMNS=150', service, '/bin/bash']
    pty.spawn(command)


def ngrok(args):
    command = ['ngrok', 'start', '--all', '--config', '.appData/ngrok/ngrok.yml']
    process = subprocess.Popen(command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    
    if stderr:
        print(stderr.decode('utf-8'))
        return 1

    print(stdout.decode('utf-8'))
    return SUCCESS, stdout.decode('utf-8')


#### Command registrar

registry = {
  'create': register_site,
  'ngrok': ngrok,
  'describe': describe,
  'list': list_sites,
  'select': select,
  'delete': delete_site,
  'enter': enter,
}

def run(command_name: str, args: dict) -> int:
    func = registry[command_name]
    exit_code = func(args)
    return exit_code

def handle_compose_command() -> int:
    if not sys.argv[1:]:
        return SKIPPED

    is_compose_command = True if sys.argv[1] == 'compose' else False
    if not is_compose_command:
        return SKIPPED

    exit_code, messaage = compose(sys.argv[2:])
    print(messaage)
    return exit_code

def main() -> None:
    # special case
    exit_code = handle_compose_command()
    if exit_code != SKIPPED:
        return

    parser = ArgumentParser()
    sub_parser = parser.add_subparsers()
    create = sub_parser.add_parser('create')
    create.add_argument('project_name', help='The identifier of the drupal stack', type=str)
    create.add_argument('--nginx-port', '-np', help='Nginx port mapping', type=str)
    create.add_argument('--mysql-port', '-mp', help='Mysql port mapping', type=str)
    create.add_argument('--ngrok-subdomain', '-nsd', help='Ngrok subdomain', type=str)
    
    describe = sub_parser.add_parser('describe')
    describe.add_argument('project_name', help='The identifier of the drupal stack', type=str)

    sub_parser.add_parser('list')

    # Not used, but at least generates a help message
    compose = sub_parser.add_parser('compose')
    compose.add_argument('command', help='The command to pass to docker-compose', type=str, nargs='*')

    enter = sub_parser.add_parser('enter')
    enter.add_argument('service', help='The service container to enter', type=str)

    select = sub_parser.add_parser('select')
    select.add_argument('project_name', help='The identifier of the drupal stack', type=str)

    delete = sub_parser.add_parser('delete')
    delete.add_argument('project_name', help='The identifier of the drupal stack', type=str)

    ngrok = sub_parser.add_parser('ngrok')
    ngrok_subpar = ngrok.add_subparsers()
    ngrok_subpar.add_parser('start', help='Start ngrok tunnel')
    
    args = vars(parser.parse_args())

    if len(sys.argv) < 2:
        parser.print_help()
        return

    run(sys.argv[1], args)


class MissingNgrokCredentialsError(Exception):
    pass

if __name__ == '__main__':
    main()
