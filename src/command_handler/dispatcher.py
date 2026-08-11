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

        self._default_command_register()

    def _default_command_register(self):
        self.register_command("open_app", OpenAppCommand(self.app_registry, self.os_adapter))
        self.register_command("open_url", OpenUrlCommand(self.os_adapter))
        self.register_command("check_process", CheckProcessCommand(self.os_adapter))
        self.register_command("execute_command", ExecuteSystemCommand(self.os_adapter))

    
    def register_command(self, action:str, command: BaseCommand):
        key = action.lower().strip()

        self.commands[key] = command
        logger.debug(f"[Dispatcher] Comando registrado correctamente : {command}")

    
    def dispatch(self, action: str, params: Optional[Dict[str,Any]] = None) -> CommandResult:
        if params is None:
            params = {}
        
        action_key = action.strip().lower()

        if action_key not in self.commands:
            logger.warning(f"[Dispatcher] Acción no reconocida: {action}")
            return CommandResult(
                success= False,
                msg=f"No se encontró ningun comando para la accion: {action}"
            )

        logger.info(f"[Dispatcher] Ejecutando acción: {action_key}")

        return self.commands[action_key].execute(params)