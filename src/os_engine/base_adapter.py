from abc import ABC, abstractmethod

class BaseAdapter(ABC):
    """
    Clase Base Abstracta que define el contrato estricto para los adaptadores de
    Sistema Operativo (Windows, Linux, etc.).

    Cualquier adaptador concreto DEBE implementar todos los métodos marcados
    con @abstractmethod.
    """

    @abstractmethod
    def open_aplication(self, app_path_or_cmd: str) -> bool:
        """
        Abre una aplicación de forma asíncrona (no bloqueante).

        :param app_path_or_cmd: Ruta ejecutable o comando de sistema.
        :return: True si se inició correctamente, False si falló.
        """
        pass
    @abstractmethod
    def open_url(self, url: str) -> bool:
        """
        Abre un enlace web en el navegador predeterminado del sistema.

        :param url: Dirección web completa (ej. "https://google.com").
        :return: True si se envió la orden de apertura, False si falló.
        """
        pass

    @abstractmethod
    def is_process_running(self, process_name: str) -> bool:
        """
        Consulta si un proceso se encuentra activo en la lista de tareas del SO.

        :param process_name: Nombre o fragmento del ejecutable a buscar.
        :return: True si el proceso está corriendo, False en caso contrario.
        """
        pass

    @abstractmethod
    def execute_system_command(self, command: str) -> tuple[bool, str]:
        """
        Ejecuta un comando arbitrario de consola y captura la respuesta.

        :param command: Comando de consola (Bash/CMD/PowerShell).
        :return: Tupla con (Éxito: bool, Salida/Error: str).
        """
        pass