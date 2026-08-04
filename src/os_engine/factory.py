from sys import platform
import os


_adapter_instance = None

def reset_adapter():
    """Limpia la instancia guardada."""
    global _adapter_instance
    _adapter_instance = None


def get_adapter():
    """Detecta el sistema operativo y retorna la instancia del adaptador correspondiente."""
    global _adapter_instance

    if _adapter_instance is not None:
        return _adapter_instance
        
    platform_os = platform.system().lower()

    if platform_os == "windows":
        from src.os_engine.windows_adapter import WindowsAdapter

        _adapter_instance = WindowsAdapter()
    elif platform_os == "linux":
        from src.os_engine.linux_adapter import LinuxAdapter

        _adapter_instance = LinuxAdapter()
    else:
        raise NotImplementedError(f"El sistema operativo " + platform_os + "no está soportado actualmente")

    return _adapter_instance