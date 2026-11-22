from typing import List, Dict, Any

class ToolsRegistry:
    """ Registra y gestiona las definiciones de herramientas para el LLM"""

    def __init__(self):
        self.tools: List[Dict[str,Any]] = []
        self.register_defaults()

    def register_defaults(self):
        """ Registra las herramientas por defecto del sistema"""

        self.tools =[
            {
                "type" : "function",
                "function" : {
                    "name" : "open_app",
                    "description" : "Abre una aplicacion instalada en el sistema operativo",
                    "parameters" :  {
                        "type" : "object",
                        "propierties" : {
                            "app_name" : {
                                "type" : "string",
                                "description" : "Nombre de la aplicación a abrir"
                            }
                        },
                        "required" : ["app_name"]
                    }
                }
            },
            {
                "type" : "function",
                "function" : {
                    "name" : "open_url",
                    "description" : "Abre una URL en el navegador web predeterminado",
                    "parameters" :  {
                        "type" : "object",
                        "propierties" : {
                            "url" : {
                                "type" : "string",
                                "description" : "La URL a abrir"
                            }
                        },
                        "required" : ["url"]
                    }
                }
            },
            {
                "type" : "function",
                "function" : {
                    "name" : "check_process",
                    "description" : "Verifica que un proceso está corriendo en el sistema",
                    "parameters" :  {
                        "type" : "object",
                        "propierties" : {
                            "process_name" : {
                                "type" : "string",
                                "description" : "Nombre del proceso a verificar"
                            }
                        },
                        "required" : ["process_name"]
                    }
                }
            },
            {
                "type" : "function",
                "function" : {
                    "name" : "execute_command",
                    "description" : "Ejecuta un comando en la terminal del sistema",
                    "parameters" :  {
                        "type" : "object",
                        "propierties" : {
                            "command" : {
                                "type" : "string",
                                "description" : "Nombre del comando a ejecutar"
                            }
                        },
                        "required" : ["command"]
                    }
                }
            },
        ]

        def get_tools(self) -> List[Dict[str,Any]]:
            """ Retorna la lista de tools en formato Ollama"""
            return self.tools

        def get_tools_name(self) -> List[str]:
            """ Retorna solo los nombre de kas tools registradas"""
            return [t["funcion"]["name"] for t in self.tools]