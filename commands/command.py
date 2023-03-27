from typing import List
from abc import ABC, abstractproperty, abstractclassmethod

class Argument:

    def __init__(self, name: str, short_name = None, help_msg = None, type = str, is_optional: bool = True):
        self._name = name
        self._short_name = short_name
        self._help_msg = help_msg
        self._type = type
        self._is_optional = is_optional

    @property
    def name(self):
        return self._name

    @property
    def short_name(self) -> str:
        return self._short_name

    @property
    def help_msg(self):
        return self._help_msg

    @property
    def type(self):
        return self._type
    
    def is_optional(self):
        return self._is_optional


class Command(ABC):
    
    def get_argument_list(self) -> List[Argument]:
        return []

    @abstractproperty
    def name(self) -> str:
        pass

    @abstractproperty
    def description(self) -> str:
        pass

    @abstractclassmethod
    def execute(self, args: dict) -> int:
        pass

