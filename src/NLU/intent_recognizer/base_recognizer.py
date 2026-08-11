from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class IntentResult:
    action_name: str
    confidence: float
    params: Dict[str, Any] = field(default_factory=dict)

class BaseIntentRecognizer(ABC):
    
    @abstractmethod
    def parse(self, user_text: str) -> IntentResult:
        """ Analiza el texto del usuario y extrae la intención"""
        pass