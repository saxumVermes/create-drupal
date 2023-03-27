import subprocess

from typing import List, Tuple
from commands.command import Command, Argument

class Composer(Command):

    @property
    def description(self):
        return 'Utilise composer inside the container'

    @property
    def name(self):
        return 'composer'
    
    def get_argument_list(self) -> List[Argument]:
        return [
            Argument(name='repo', is_optional=False)
        ]

    @classmethod
    def execute(self, args: dict):
        self.add_repository()
        


    def add_repository(self):
        exit_code, res = self.compose(['ps'])
        print(res)


    def compose(self, args) -> Tuple[int, str]:
        command = ['docker-compose', '-f', 'stack/docker-compose.yaml']
        if args:
            command.extend(args)

        process = subprocess.Popen(command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        
        if stderr:
            return 2, stderr.decode('utf-8')

        return 0, stdout.decode('utf-8')