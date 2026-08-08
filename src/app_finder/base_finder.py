from abc import ABC, abstractmethod

class BaseAppFinder(ABC):
    """ Clase base abstracta que define el contrato estricto para los finders de cada SO
    
    
    Cualquier finder concreto DEBE implementar todos los métodos marcados
    con @abstractmethod.
    """
    @abstractmethod
    def get_apps() -> dict[str, str]:
        """
        Escanea el sistema operativo en busca de aplicaciones instaladas.
        
        Return:
            Un diccionario/mapa de pares clave-valor donde:
            - Clave: Nombre de la aplicación en minúsculas (ej: "google chrome", "spotify").
            - Valor: Ruta absoluta al ejecutable, acceso directo o comando del sistema
                     (ej: "/usr/bin/google-chrome" o "C:\Program Files\...\spotify.exe").
        """
        pass