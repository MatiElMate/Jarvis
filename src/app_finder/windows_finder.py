import os
import logging
from pathlib import Path
from src.app_finder.base_finder import BaseAppFinder

logger = logging.getLogger(__name__)

class WindowsAppFinder(BaseAppFinder):

    def __init__(self):
        self._home = Path.home()
        
        self._desktop_paths = [
            Path(os.path.expandvars(r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs")),
            Path(os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs")),
        ]

    @property
    def desktop_paths(self) -> list[Path]:
        return self._desktop_paths

    
    def get_apps(self) -> dict[str,str]:
        apps = {}

        for folder in self.desktop_paths:
            if not(folder.exists()):
                continue

            for file in folder.rglob("*.lnk"):
                try:
                    app_name = file.stem.lower()

                    app_path = str(file.resolve())

                    if app_name not in apps:
                        apps[app_name] = app_path
                
                except Exception as e:
                    logger.debug(
                        f"[WindowsFinder] Error procesando el archivo {file} : {e}"
                        )
                    continue


        logger.info(
            f"[WindowsFinder] Se encontraron {len(apps)} aplicaciones en Windows"
            )
        return apps                
