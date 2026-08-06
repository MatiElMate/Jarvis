from re import sub
import shlex
import subprocess
import logging
from src.os_engine.base_adapter import BaseAdapter

logger = logging.getLogger(__name__)

class Linux(BaseAdapter):
    def open_aplication(self, app_cmd: str) -> bool:
        """
        Abre una aplicación en Linux usando su comando global de terminal.
        Ejemplos de app_cmd: 'code', 'google-chrome', 'spotify'
        """
        try: 
            args = shlex.spli(app_cmd)

            subprocess.Popen(
                args,
                stdout= subprocess.DEVNULL,
                stderr= subprocess.DEVNULL,
                start_new_session= True
            )
            return True
        
        except FileNotFoundError:
            logger.error(f"[LinuxAdapter] No se encontró el comando '{app_cmd} en el PATH del sistema'")
            return False
        
        except Exception as e:
            logger.error(f"[LinuxAdapter] Error al abrir '{app_cmd} : {e}'")
            return False

    def open_url(self,url:str) -> bool:
        """ Abre una URL en el navegador predeterminado de Linux usando xdg-open."""
        try:
            subprocess.Popen(
                ["xdg-open",url],
                stdout= subprocess.DEVNULL,
                stderr= subprocess.DEVNULL,
                start_new_session= True
            )
            return True

        except Exception as e:
            logger.error(f"[LinuxAdapter] Error al abrir al URL '{url} : {e}'")
            return False
    
    def is_process_running(self, process_name: str) -> bool:
        """ Verifica si un proceso está activo en Linux usando la herramienta pgrep"""
        try:
            result = subprocess.run(
                ["pgrep", "-f", process_name],
                stdout= subprocess.PIPE,
                stderr= subprocess.PIPE,
                text= True
            )
            return result.resturncode == 0

        except Exception as e:
            logger.error(f"[LinuxAdapter] Error al verificar el proceso '{process_name}' : {e}")
            return False

    def execute_system_command(self, command: str) -> tuple[bool,str]:
        """ Ejecuta un comando de la consola Linux y retorna su resultado"""
        try: 
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text= True
            )
            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                return False, result.stderr.strip()
        
        except Exception as e:
            logger.error(f"[LinuxAdapter] Error al ejecutar el comando '{command} : {e}'")
            return False, str(e)