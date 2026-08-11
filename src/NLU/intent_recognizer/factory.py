import logging
from src.NLU.intent_recognizer.base_recognizer import BaseIntentRecognizer, IntentResult
from src.NLU.intent_recognizer.rule_recognizer import RuleIntentRecognizer

logger = logging.getLogger(__name__)

def get_intent_recognizer(recognizer_type: str = "rule") -> BaseIntentRecognizer:
    """ Fábrica que instancia y devuelve el clasificador de intenciones seleccionado"""

    clean_type = recognizer_type.strip().lower()

    if clean_type == "rule":
        logger.debug("Instanciando RuleIntentRecognizer")
        return RuleIntentRecognizer()

    logger.warning(f"Tipo no soportado, usando 'rule' por defecto: {recognizer_type}")

    return RuleIntentRecognizer()