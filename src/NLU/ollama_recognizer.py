from src.NLU.intent_recognizer import IntentResult
import logging
from src.NLU.intent_recognizer import BaseIntentRecognizer
import json
import ollama

logger = logging.getLogger(__name__)

class OllamaRecognizer(BaseIntentRecognizer):
    def __init__(self, modelo_ollama = "llama3.2:1b"):
        self.modelo = modelo_ollama

        self.prompt_sistema = """
        Eres Jarvis, un asistente virtual avanzado. 
        Tienes acceso a las siguientes herramientas. Si el usuario te pide usarlas, DEBES responder ÚNICAMENTE con un JSON con este formato exacto: {"action_name": "nombre_herramienta", "params": {"parametro": "valor"}, "success": booleano si la respuesta fue correcta}
        
        Herramientas disponibles:
        - open_app (parámetros: app_name)
        - open_url (parámetros: url)
        - check_process (parámetros: process_name)
        - execute_command (parámetros: command)
        
        Si el usuario te hace una pregunta general, te saluda o quiere conversar, responde ÚNICAMENTE con un JSON con este formato:
        {"action_name": "chat", "params": {"response": "Tu respuesta conversacional aquí."}, "success": booleano si la respuesta fue correcta}
        
        NO incluyas texto fuera del JSON.
        """

    def parse(self, user_input: str) -> IntentResult:
        prompt_completo = self.prompt_sistema + "\n Usuario: " + user_input

        mensajes = [
            {"role": "system", "content": self.prompt_sistema},
            {"role": "user", "content": user_input}
        ]

        try:
            respuesta_http = ollama.chat(
                model=self.modelo,
                messages=mensajes,
                stream=False,
                format="json"
            )
            
            respuesta_ollama = json.loads(respuesta_http["message"]["content"])
            
            # 1. Extraemos la acción que propuso el modelo
            action_propuesta = respuesta_ollama.get("action_name", "unknown")
            
            # 2. Lista estricta de las herramientas que Jarvis realmente tiene
            herramientas_validas = ["open_app", "open_url", "check_process", "execute_command"]
            
            # 3. MAPEO DEFENSIVO: Si inventó una acción (como "saludo"), lo forzamos a "chat"
            if action_propuesta not in herramientas_validas:
                action_propuesta = "chat"
            
            # Si el modelo no incluyó "response" en params para un chat, le damos un valor por defecto
            params = respuesta_ollama.get("params", {})
            if action_propuesta == "chat" and "response" not in params:
                params["response"] = "Entendido."

            
            return IntentResult(
                action_name=action_propuesta,
                params=params,
                confidence=1.0
            )

        except Exception as e:
            logger.error(f"[OllamaRecognizer] Error procesando la intención: {e}")
            return IntentResult(action_name="unknown", params={}, confidence=0.0)