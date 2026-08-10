import logging
from typing import Any, Dict, Optional

from src.app_finder.registry import AppRegistry
from src.command_handler.system_command import (
    BaseCommand,
    CheckProcessCommand,
    CommandResult,
    ExecuteSystemCommand,
    OpenAppCommand,
    OpenUrlCommand,
)
from src.os_engine.base_adapter import BaseAdapter

logger = logging.getLogger(__name__)

class CommandDispatcher():
    """
    Despachador central que asocia nombres de acciones con su comando correspondiente
    y ejecuta las solicitudes enviadas por el sistema.
    """

    def __init__(self, app_registry: AppRegistry, os_adapter: BaseAdapter):
        self.app_registry = app_registry
        self.os_adapter = os_adapter
        self.commands = {}

    def _default_command_register(self):
        self.command_register("open_app", OpenAppCommand(self.app_registry, self.os_adapter))
        self.command_register("open_url", OpenUrlCommand(self.os_adapter))
        self.command_register("check_process", CheckProcessCommand(self.os_adapter))
        self.command_register("execute_command", ExecuteSystemCommand(self.os_adapter))

    
    def command_register(self, action:str, command: BaseCommand):
        key = action.lower().strip()

        self.commands[key] = command
        logger.debug(f"[Dispatcher] Comando registrado correctamente : {command}")

    
    def dispatch(self, action: str, params: Optional[Dict[str,Any]] = None) -> CommandResult:
        if not params:
            params = {}
        
        action_key = action.lower().strip()

        if action_key not in self.commands:
            logger.warning(f"[Dispatcher] Acción no reconocida: {action}")
            return CommandResult(
                success= False,
                msg=f"No se encontró ningun comando para la accion: {action}"
            )

        target_command = self.commands[action_key]
        logger.info(f"[Dispatcher] Ejecutando acción: {action_key}")

        return target_command.execute(params)