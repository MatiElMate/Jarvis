from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class IntentResult:
    """Contenedor de respuesta estandarizado para la intención analizada."""

    action_name: str
    params: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0

class BaseIntentRecognizer(ABC):
    
    @abstractmethod
    def parse(self, user_text: str) -> IntentResult:
        """ Analiza el texto del usuario y extrae la intención"""
        pass