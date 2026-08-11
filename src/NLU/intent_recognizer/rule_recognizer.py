from re import Pattern
from src.NLU.intent_recognizer.base_recognizer import IntentResult
import re
from typing import Dict, Any, Optional, List, Tuple 
from src.NLU.intent_recognizer.base_recognizer import BaseIntentRecognizer
import logging

logger = logging.getLogger(__name__)


class RuleIntentRecognizer(BaseIntentRecognizer):
    """ Reconoce intenciones ultilizando patrones RegEx."""

    def __init__(self):

        self.patterns: List[Tuple[Pattern[str],str,str]] = [
            (
                re.compile(r"(?:abrir|abre|abrime|iniciar|iniciame|lanza|lanzar|lanzame)\s(.+)"),re.IGNORECASE,
            "open_url",
            "app_name"
            ),
            (
                re.compile(r"(?:navegar|entra|entrar|abrir sitio|navegame|ir a)\s(.+)"),re.IGNORECASE,
                "open_url",
                "url"
            ),
            (
                re.compile(r"(?:comprobar|revisar|ver estado de|fijate)\s(.+)"),re.IGNORECASE,
                "check_process",
                "process_name"
            ),
            (
                re.compile(r"(?:ejecutar|ejecutar comando|consola|cmd)\s(.+)"),re.IGNORECASE,
                "execute_command",
                "command"
            )
        ]

    def parse(self, user_text: str) -> IntentResult:
        clean_text = user_text.strip().lower()

        if not clean_text:
            logger.debug("[RuleIntentRecognizer] Entrada vacía recibida.")
            return IntentResult(
                action_name="unknown",
                params={},
                confidence= 0.0
            )

        for (pattern, action, param_key) in self.patterns:
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