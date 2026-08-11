from re import sub
import logging
from pathlib import Path
from src.SL.app_finder.base_finder import BaseAppFinder

logger = logging.getLogger(__name__)


class LinuxAppFinder(BaseAppFinder):

    def __init__(self):
        self._home = Path.home()
        
        self._desktop_paths = [
            Path("/usr/share/applications"),
            Path("/usr/local/share/applications"),
            self._home / ".local/share/applications"  # Usamos pathlib para unir rutas
        ]

    @property
    def desktop_paths(self) -> list[Path]:
        return self._desktop_paths

    
    def _parse_desktop_file(self,file_path) -> tuple[str|None, str|None]:
        name = None
        command = None
        hidden = False

        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
            
                if line.startswith("Name=") and name is None:
                    name = line.split("=", 1)[1]

                elif line.startswith("Exec=") and command is None:
                    brute_command = line.split("=",1)[1]
                    command = brute_command.split("%")[0].strip().replace('"',"")
            
                elif line.startswith("NoDisplay=true"):
                    hidden = True
        
        if hidden:
            return (None,None)
        else:
            return (name,command)

    def get_apps(self) -> dict[str,str]:
        apps = {}

        for folder in self.desktop_paths: 
            if not(folder.exists()):
                continue
            
            for file in folder.glob("*.desktop"):
                try:
                    name,command = self._parse_desktop_file(file)
                    if name and command:
                        apps[name.lower()] = command
                        
                except Exception as e:
                    logger.debug(
                        f"[LinuxFinder] Error leyendo {file} : {e}"
                        )
        
        
        logger.info(
            f"[LinuxFinder] Se encontraron {len(apps)} aplicaciones en Linux"
            )
        return apps