from re import Pattern
from src.NLU.intent_recognizer.base_recognizer import IntentResult
import re
from typing import Dict, Any, Optional, List, Tuple 
from src.NLU.intent_recognizer.base_recognizer import BaseIntentRecognizer
import logging
from src.NLU.intent_recognizer.text_cleaner import text_normalizer

logger = logging.getLogger(__name__)


class RuleIntentRecognizer(BaseIntentRecognizer):
    """ Reconoce intenciones ultilizando patrones RegEx."""

    def __init__(self):

        self.patterns: List[Tuple[Pattern[str],str,str]] = [
            (
                re.compile(r"(?:abrir url|abrir sitio|navegar a|entrar a|entra a|entrar en|entra|entrar|navegame|ir a |navega)\s(.+)",re.IGNORECASE),
                "open_url",
                "url"
            ),
            (
                re.compile(r"(?:comprobar proceso|comprobar|revisar proceso|revisar|ver proceso|esta corriendo|ver estado de|fijate|ver)\s(.+)",re.IGNORECASE),
                "check_process",
                "process_name"
            ),
            (
                re.compile(r"(?:ejecutar comando|ejecutar|consola|cmd)\s(.+)",re.IGNORECASE),
                "execute_command",
                "command"
            ),
            (
                re.compile(r"(?:abrir|abre|abrime|iniciar|inicia|iniciame|lanza|lanzar|lanzame)\s(.+)",re.IGNORECASE),
            "open_app",
            "app_name"
            )
        ]

    def parse(self, user_text: str) -> IntentResult:

        clean_text = text_normalizer(user_text)

        if not clean_text:
            logger.debug("[RuleIntentRecognizer] Entrada vacía recibida.")
            return IntentResult(
                action_name="unknown",
                params={},
                confidence= 0.0
            )

        for pattern, action, param_key in self.patterns:
            match = pattern.search(clean_text)

            if match:
                value = match.group(1).strip()
                logger.info(
                    f"[RuleIntentRecognizer] Intención detectada: '{action}' -> {param_key}='{value}'"
                )
                return IntentResult(
                    action_name= action,
                    params= {param_key: value},
                    confidence= 0.9
                )

        logger.warning(
            f"[RuleIntentRecognizer] No se pudo clasificar la intención para: '{clean_text}'"
        )
        return IntentResult(
            action_name="unknown",
            params= {},
            confidence= 0.0
        )