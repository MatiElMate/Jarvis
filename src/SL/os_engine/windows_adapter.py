from subprocess import PIPE
from src.SL.os_engine import base_adapter
from subprocess import DEVNULL
from os import O_APPEND
from re import sub
import os
import subprocess
import logging
from src.SL.os_engine.base_adapter import BaseAdapter
from urllib.parse import urlparse
from pathlib import Path


logger = logging.getLogger(__name__)
creation_flags = getattr(subprocess, "DETACHED_PROCESS", 0x00000008)
class WindowsAdapter(BaseAdapter):
    def open_application(self, app_path_or_cmd: str) -> bool:
        """ Abre una aplicación de forma asíncrona sin bloquear el asistente.
        Soporta rutas absolutas, comandos de sistema y protocolos URI (ej. whatsapp://)."""

        try:
            extended_path = os.path.expandvars(app_path_or_cmd)

            parsed = urlparse(extended_path)

            if(parsed.scheme):
                subprocess.Popen(
                    f'start "" "{extended_path} ""',
                    shell= True,
                    stdout= subprocess.DEVNULL,
                    stderr= subprocess.DEVNULL
                )
                return True
            else:
                subprocess.Popen(
                    [extended_path],
                    shell= True,
                    creationflags= creation_flags,
                    stdout= subprocess.DEVNULL,
                    stderr= subprocess.DEVNULL
                )
                return True
        
        except Exception as e:
            logger.error(f"[WindowsAdapter] Error al abrir aplicacion {app_path_or_cmd} : {e}")
            return False
    
    def open_url(self, url: str) -> bool:
        """ Abre un enlace web en el navegador predeterminado de Windows"""
        try:
            subprocess.Popen(
               f'start "" "{url}"',
                shell = True,
                stdout=subprocess.DEVNULL
            )
            return True
        except Exception as e:
            logger.error(f"Error al abrir URL {url} : {e}")
            return False
    
    def is_process_running(self, process_name: str) -> bool:
        """ Consulta si un ejecutable o proceso está activo en Windows usando 'tasklist'."""

        try:
            name = process_name
            if Path(name).suffix != ".exe":
                name = f"{name}.exe"
            
            result = subprocess.run(
                ["tasklist","/FI", "IMAGENAME eq " + name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text= True
            )

            out_text = (result.stdout).lower()

            return name.lower() in out_text
            
        except Exception as e:
            logger.error(f"[WindowsAdapter] Error al verificar proceso {process_name} : {e}")
            return False
        
    def execute_system_command(self, command: str) -> tuple[bool,str]:
        try:
            result = subprocess.run(
                command,
                shell= True,
                stdout=subprocess.PIPE,
                stderr= subprocess.PIPE,
                text= True
            )

            if result.returncode == 0:
                return (True, (result.stdout).strip())
            else:
                return (False, (result.stderr).strip())
        
        except Exception as e:
            logger.error(f"[WindowsAdapter] Error al ejecutar el comando {command} : {e}")
            return (False, str(e))