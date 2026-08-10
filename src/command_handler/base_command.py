from abc import ABC, abstractmethod

class BaseCommand(ABC):
    """ Clase base que define los contratos que va a seguir cada comando"""
    
    def execute(self, dictionary: dict):
        """ Ejecuta un comando """
        pass