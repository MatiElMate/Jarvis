import logging
import sys
from typing import Dict, Any

from src.SL.os_engine.factory import get_adapter

from src.SL.app_finder.factory import get_finder
from src.SL.app_finder.registry import AppRegistry

from src.SL.command_handler.base_command import CommandResult

from src.SL.command_handler.dispatcher import CommandDispatcher
from src.SL.command_handler.system_command import OpenAppCommand, OpenUrlCommand, ExecuteSystemCommand, CheckProcessCommand

from src.NLU.intent_recognizer.factory import get_intent_recognizer
from src.core.assistant import AssistantCore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("jarvis.log", encoding="utf-8"),
        logging.StreamHandler(sys.stderr),
    ],
)
logger = logging.getLogger("JarvisCLI")

def init_asistant() -> AssistantCore:
    """
        Ensambla e inyecta todas las dependencias del sistema
    """
    logger.info("[Main] Inicializando componentes de infraestructura...")
    
    app_registry = AppRegistry()
    os_adapter = get_adapter()

    dispatcher = CommandDispatcher(app_registry,os_adapter)
    dispatcher._default_command_register()

    recognizer = get_intent_recognizer()

    return AssistantCore(
        dispatcher= dispatcher,
        recognizer= recognizer
    )


def print_response(response: Dict[str,Any]) -> None:
    """
        Formatea la respuesta generada por AssistantCore en la consola.
    """
    if response.get("success"):
        data = response.get("data") or {}
        if data.get("output") is not None:
            print(f"\n [Correcto!] {response.get('msg')}, la salidida fue: \n {data.get('output')}")
        else:
            print(f"\n [Correcto!] {response.get('msg')}")
            logger.info(f"[Main] abierto con {response.get('action')} desde {response.get('data')}")
    else:
        print(f"\n [Error] {response.get('msg')}")


def main() -> None:
    """
        Bucle interactivo de entrada y salida por consola
    """

    
    try:
        assistant = init_asistant()
    
    except Exception as e:
        logger.critical(f"[Main] Error al intentar iniciar el asistente: {e}")
        sys.exit(1)
    

    print("\n Asistente inicializado")
    print("\n BIP bOp")
    print("\n Escribe 'salir' para terminar")
    print("=" * 55 + "\n")
    print("\n Esperando ordenes...")
    print("\n Ejemplos: 'abrir spotify', 'navegar a google.com'")
    print("\n Bip Bop?")
    print("=" * 55 + "\n")


    while(True):
        try:
            user_input = input("Jarvis> ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ("salir", "exit", "quit", "q"):
                print("\nNos vemos luego...")
                print("\nBop Bip Bup")
                break

            response = assistant.process_input(user_input)
            print_response(response)

        except KeyboardInterrupt as user_interruption:
            print("\n Operacion cancelada por el usuario. Saliendo...")
            break

        except Exception as e:
            logger.error(f"[Main]: Error en el bucle principal: {e}")
            print(f"\n Ocurrió un error inesperado: {e}")


if __name__ == "__main__":
    main()

