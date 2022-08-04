from locale import locale_encoding_alias
from typing import Tuple


class Site:

    def __init__(self, nginx: str, mysql: str, name: str, hostname: str, domain: str):
        self._nginx = nginx
        self._mysql = mysql
        self._name = name
        self._domain = domain
        self._hostname = hostname

    @property
    def nginx(self):
        return self._nginx

    @property
    def mysql(self):
        return self._mysql

    @property
    def name(self):
        return self._name

    @property
    def domain(self):
        return self._domain

    @property
    def hostname(self):
        return self._hostname

    def getHostAndPort(self):
        return f'{self._hostname}:{self._nginx}'