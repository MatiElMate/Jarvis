import logging
from typing import Dict, Any, Optional

from src.SL.command_handler.dispatcher import CommandDispatcher
from src.NLU.intent_recognizer.base_recognizer import BaseIntentRecognizer
from src.NLU.intent_recognizer.factory import get_intent_recognizer

logger = logging.getLogger(__name__)

class AsistantCore:
    """
    Orquestador principal del asistente virtual.
    Une el módulo de NLU (intención) con el CommandDispatcher (ejecución).
    """

    def __init__(self, dispatcher: CommandDispatcher, recognizer: Optional[BaseIntentRecognizer] = None):
        
        self.dispatcher = dispatcher

        if recognizer != None:
            self.recognizer = recognizer
        else:
            self.recognizer = get_intent_recognizer("rule")

        logger.info("Core del sistema inicializado correctamente")


    def procces_input(self, user_text: str) -> Dict[str,Any]:
        """
        Flujo principal:
        Texto -> Reconocimiento de Intención -> Despacho de Comando -> Respuesta
        """

        logger.info(f"Iniciando proceso de reconocimiento para: {user_text}")

        intention = self.recognizer.parse(user_text)

        if intention.action_name == "unknown":
            logger.warning(f"No se pudo interpretar la accion: {user_text}")
            return Dict(
                success= False,
                msg= f"Lo lamento, no puedo entender la solicitud",
                action= "unknown",
                data= {}
            )      
            
            dispatch = self.dispatcher.dispatch(intention.action_name,intention.params)

        return Dict(
            success= dispatch.success,
            msg= dispatch.msg,
            action= intention.action_name,
            data=dispatch.data
        )