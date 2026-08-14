from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class CommandResult():
    success: bool
    msg: str
    data: Optional[Dict[str, Any]] = None

class BaseCommand(ABC):
    """ Clase base que define los contratos que va a seguir cada comando"""
    
    def execute(self, dictionary: dict):
        """ Ejecuta un comando """
        pass