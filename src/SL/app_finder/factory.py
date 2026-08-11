import platform
from src.SL.app_finder.base_finder import BaseAppFinder
import logging

logger = logging.getLogger(__name__)

def get_finder() -> BaseAppFinder:
    os_name = platform.system().lower()

    if os_name == "windows":
        from src.SL.app_finder.windows_finder import WindowsAppFinder
        logger.info("Cargando el buscador de apps de Windows...")
        return WindowsAppFinder()


    elif os_name == "linux":
        from src.SL.app_finder.linux_finder import LinuxAppFinder
        logger.info("Cargando el buscador de apps de Linux...")
        return LinuxAppFinder()


    else:
        logger.critical(f"[FactoryFinder] El sistema operativo {os_name} no está soportado por el buscardor de apps")
        raise(NotImplementedError(f"El sistema operativo {os_name} no está soportado por el buscardor de apps"))