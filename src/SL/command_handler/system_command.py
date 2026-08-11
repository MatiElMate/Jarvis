from urllib3.util import url
from src.SL.os_engine.base_adapter import BaseAdapter
from src.SL.app_finder.registry import AppRegistry
from typing import Optional, Dict, Any
from dataclasses import dataclass
import requests
import logging
from src.SL.command_handler.base_command import BaseCommand

logger = logging.getLogger(__name__)


@dataclass
class CommandResult():
    success: bool
    msg: str
    data: Optional[Dict[str, Any]] = None

class OpenAppCommand(BaseCommand):
    """Comando para buscar y abrir una aplicacion en el sistema"""

    def __init__(self, app_registry: AppRegistry, os_engine: BaseAdapter):
        self.app_registry = app_registry
        self.os_engine = os_engine

    
    def execute(self, dictionary: Dict[str, Any]) -> CommandResult:
        app_name = dictionary.get("app_name")

        if not app_name:
            logger.warning(f"[SystemCommand] No se especificó una aplicación")
            return CommandResult(
                success = False,
                msg = "No se especificó el nombre de la aplicacion"
            )
        
        app_path = self.app_registry.get_app_path(app_name)

        if not app_path:
            logger.warning(f"[SystemCommand] No se encontró la aplicación {app_name}")
            return CommandResult(
                success= False,
                msg = f"No se encontró la aplicación: {app_name}"
            )

        os_open = self.os_engine.open_application(app_path)

        if os_open:
            logger.info(f"[SystemCommand] Se inició la aplicación {app_name}")
            return CommandResult(
                success= True,
                msg = f"Aplicación iniciada: {app_name}",
                data = {"path": app_path}
            )
        else:
            logger.error(f"[SystemCommand] Error al abrir la aplicación {app_name}")
            return CommandResult(
                success= False,
                msg= f"Error al intentar abrir: {app_name}" 
            )

class OpenUrlCommand(BaseCommand):
    """ Comando para abrir URLs con el navegador predeterminado del sistema"""

    def __init__(self, os_adapter: BaseAdapter):
        self.os_engine = os_adapter

    def execute(self, dictionary: Dict[str, Any]) -> CommandResult:
        url = dictionary.get("url")
        if not url:
            logger.warning(f"[SystemCommand] No se recibió ninguna url")
            return CommandResult(
                success= False,
                msg = f"No se encontró envió ninguna url"
            )

        if not (url.startswith("http://") or url.startswith("https://")):
            url = "https://" + url

        
        user_url = self.os_engine.open_url(url)
        
        if user_url:
            logger.info(f"[SystemCommand] Éxito al abrir la URL {url}")
            return CommandResult(
                success= True,
                msg=f"La URL {url} se abrió con éxito",
                data= {"url": url}
            )
        else:
            logger.error(f"[SystemCommand] Error al abrir la URL {url}")
            return CommandResult(
                success= False,
                msg=f"Error al abrir {url}"
                )

class CheckProcessCommand(BaseCommand):
    """ Comando para detectar si un proceso está corriendo en el sistema"""

    def __init__(self, os_adapter: BaseAdapter):
        self.os_engine = os_adapter

    def execute(self, dictionary: Dict[str, Any]) -> CommandResult:
        process_name = dictionary.get("process_name")

        if not process_name:
            logger.warning(f"[SystemCommand] No se especificó un proceso")
            return CommandResult(
                success= False,
                msg= f"No se especificó un proceso"
            )
        
        running = self.os_engine.is_process_running(process_name)

        if running:
            logger.info(f"[SystemCommand] Se encontró el proceso {process_name}")
            return CommandResult(
                success= True,
                msg= f"El proceso {process_name} está corriendo actualmente",
                data= {"process_name" : process_name, "is_running" : running}
            )
        else:
            logger.info(f"[SystemCommand] El proceso {process_name} está actualmente inactivo")
            return CommandResult(
                success= True,
                msg= f"El proceso {process_name} no está corriendo actualmente",
                data= {"process_name" : process_name, "is_running" : running}
            )


class ExecuteSystemCommand(BaseCommand):

    """ Comando dedicado a ejecutar comandos propios del sistema operativo"""

    def __init__(self, os_adapter: BaseAdapter):
        self.os_engine = os_adapter

    def execute(self, dictionary : Dict[str, Any]) -> CommandResult:
        cmd_str = dictionary.get("command")

        if not cmd_str:
            logger.critical(f"[SystemCommand] No se proporciono un comando a ejecutar")
            return CommandResult(
                success= False,
                msg= f"No se proporcionó un comando"
            )

        command_status, output = self.os_engine.execute_system_command(cmd_str)

        if command_status:
            logger.info(f"[SystemCommand] Se ejecutó el comando {cmd_str}")
            return CommandResult(
                success= True,
                msg= f"El comando {cmd_str} se ejecutó con éxito",
                data={"command" : cmd_str, "output": output}
            )
        else:
            logger.error(f"[SystemCommand] Error al ejecutar el comando {cmd_str} | Error: {output}")
            return CommandResult(
                success=False,
                msg=f"Error al ejecutar el comando {output}",
                data={"command" : cmd_str, "output": output}
            )







# class VolumeControlCommand(BaseCommand):
#     """ COmando para ajustar el volumen del sistema"""
#     def __init__(self, os_engine: BaseAdapter):
#         self.os_engine = os_engine

#     def execute(self, dictionary: dict) -> CommandResult:
#         action = dictionary.get("action")
#         value = dictionary.get("value")

#         if action == "up":
#             self.os_engine.volume_up()
#             return CommandResult(
#                 success=True,
#                 msg= "Volumen aumentado."
#             )
#         elif action == "down":
#             self.os_engine.volume_down()
#             return CommandResult(
#                 success=True,
#                 msg= "Volumen reducido."
#             )
#         elif action == "mute":
#             self.os_engine.toggle_mute()
#             return CommandResult(
#                 success=True,
#                 msg= "Estado de silencio cambiado."
#             )
#         elif action == "set" and value is number:
#             self.os_engine.set_volume(value)
#             return CommandResult(
#                 success=True,
#                 msg= "Volumen aumentado."
#             )
#         else:
#             return CommandResult(
#                 success=False,
#                 msg= f"Acción de volumen no valida: {action}"
#             )

