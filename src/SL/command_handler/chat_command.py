from typing import Any
from src.SL.command_handler.base_command import BaseCommand, CommandResult

class ChatCommand(BaseCommand):
    def execute(self, params: dict[str, Any]) -> CommandResult:
        respuesta_texto = params.get("response", "Sin respuesta")

        if not respuesta_texto:
            return CommandResult(
                success=False,
                msg="Jarvis no generó ninguna respuesta conversacional"
            )

        return CommandResult(
            success=True,
            msg=respuesta_texto
        )