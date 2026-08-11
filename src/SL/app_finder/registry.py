import logging
from typing import Optional
from src.SL.app_finder.factory import get_finder

logger = logging.getLogger(__name__)

class AppRegistry():
    def __init__(self):
        self.apps: dict[str, str] = {}
        self.alias: dict[str, str] = {
            "browser": "google chrome",
            "navegador": "google chrome",
            "musica": "spotify",
            "codigo": "visual studio code",
        }
    
    def refresh_cache(self) -> None:
        """ Refresca la caché del registrador"""
        finder = get_finder()
        self.apps = finder.get_apps()
        

    def get_app_path(self, user_prompt) -> Optional[str]:
        if not self.apps:
            self.refresh_cache()

        clean_text = user_prompt.strip().lower()

        if clean_text in self.alias:
            clean_text = self.alias[clean_text]
        
        if clean_text in self.apps:
            return self.apps[clean_text]

        for name, path in self.apps.items():
            if clean_text in name or name in clean_text:
                logger.info(
                    f"[AppRegistry] Coincidencia parcial: '{user_prompt}' -> '{name}'"
                )
                return path
        logger.warning(
            f"[AppRegistry] No se encontró ninguna aplicacion para '{user_prompt}'"
        )
        return None