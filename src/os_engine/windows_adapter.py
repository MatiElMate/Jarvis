from subprocess import PIPE
from src.os_engine import base_adapter
from subprocess import DEVNULL
from os import O_APPEND
from re import sub
import os
import subprocess
from urllib import urlparse
import logging
from src.os_engine.base_adapter import BaseAdapter
from pathlib import Path


logger = logging.getLogger(__name__)

class Windows(BaseAdapter):
    def open_aplication(self, app_path_or_cmd: str) -> bool:
        """ Abre una aplicación de forma asíncrona sin bloquear el asistente.
        Soporta rutas absolutas, comandos de sistema y protocolos URI (ej. whatsapp://)."""

        try:
            extended_path = urlparse(os.getenv(app_path_or_cmd))

            if(extended_path.scheme and extended_path.netloc):
                subprocess.Popen(
                    "start \"\" \"" + extended_path + "\"",
                    shell= True,
                    stdout= DEVNULL
                )
                return True
            else:
                subprocess.Popen(
                    [extended_path],
                    shell= True,
                    start_new_session= True,
                    stdout=True
                )
                return True
        
        except Exception as e:
            logger.error(f"[WindowsAdapter] Error al abrir aplicacion {app_path_or_cmd} : {e}")
            return False
    
    def open_url(self, url: str) -> bool:
        """ Abre un enlace web en el navegador predeterminado de Windows"""
        try:
            subprocess.Popen(
                "start \"\" \"" + url + "\"",
                shell = True,
                stdout= True
            )
            return True
        except Exception as e:
            logger.error(f"Error al abrir URL {url} : {e}")
            return False
    
    def is_process_running(self, process_name: str) -> bool:
        """ Consulta si un ejecutable o proceso está activo en Windows usando 'tasklist'."""

        try:
            name = process_name
            if not(Path(name).suffix == "exe"):
                name == f"{name} + .exe"
            
            result = subprocess.Popen(
                ["tasklist","/FI", "IMAGENAME eq" + name],
                stdout=PIPE,
                text= True
            )

            out_text = (result.stdout).lower()

            if name.lower() in out_text:
                return True
            else:
                return False
            
        except Exception as e:
            logger.error(f"[WindowsAdapter] Error al verificar proceso {process_name} : {e}")
            return False
        
    def execute_system_command(self, command: str) -> tuple[bool,str]:
        try:
            result = subprocess.run(
                command,
                shell= True,
                stdout=PIPE,
                stderr= PIPE,
                text= True
            )

            if result.stdout == 0:
                return (True, (result.stdout).strip())
            else:
                return (False, (result.stderr).strip())
        
        except Exception as e:
            logger.error(f"[WindowsAdapter] Error al ejecutar el comando {command} : {e}")
            return (False, e)