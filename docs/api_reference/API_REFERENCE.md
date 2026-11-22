# 📖 Referencia de API — Jarvis

> Documentación auto-generada el **2026-08-14 09:16:05**  
> Generada con Pydantic `model_json_schema()` + introspección de ABCs

---

## Índice

- 📦 [`CommandResult`](#commandresult)
- 📦 [`IntentResult`](#intentresult)
- 🔷 [`BaseCommand`](#basecommand)
- 🔷 [`BaseAdapter`](#baseadapter)
- 🔷 [`BaseAppFinder`](#baseappfinder)
- 🔷 [`BaseIntentRecognizer`](#baseintentrecognizer)

---

## 📦 Data Classes (Modelos de Datos)

Objetos de datos con validación de tipos. Documentados mediante modelos Pydantic espejo.

### `CommandResult`

📦 **Tipo**: Data Class  
📁 **Módulo**: `src/SL/command_handler/base_command.py`

> CommandResult(success: bool, msg: str, data: Optional[Dict[str, Any]] = None)

| Campo | Tipo | Requerido | Default | Descripción |
|-------|------|-----------|---------|-------------|
| `success` | `boolean` | ✅ | — | Campo 'success' |
| `msg` | `string` | ✅ | — | Campo 'msg' |
| `data` | `object` \| `null` | ❌ | `None` | Campo 'data' |

<details>
<summary>📋 JSON Schema completo</summary>

```json
{
  "description": "CommandResult(success: bool, msg: str, data: Optional[Dict[str, Any]] = None)",
  "properties": {
    "success": {
      "description": "Campo 'success'",
      "title": "Success",
      "type": "boolean"
    },
    "msg": {
      "description": "Campo 'msg'",
      "title": "Msg",
      "type": "string"
    },
    "data": {
      "anyOf": [
        {
          "additionalProperties": true,
          "type": "object"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Campo 'data'",
      "title": "Data"
    }
  },
  "required": [
    "success",
    "msg"
  ],
  "title": "CommandResult",
  "type": "object"
}
```
</details>

---

### `IntentResult`

📦 **Tipo**: Data Class  
📁 **Módulo**: `src/NLU/intent_recognizer/base_recognizer.py`

> Contenedor de respuesta estandarizado para la intención analizada.

| Campo | Tipo | Requerido | Default | Descripción |
|-------|------|-----------|---------|-------------|
| `action_name` | `string` | ✅ | — | Campo 'action_name' |
| `params` | `object` | ❌ | — | Campo 'params' |
| `confidence` | `number` | ❌ | `0.0` | Campo 'confidence' |

<details>
<summary>📋 JSON Schema completo</summary>

```json
{
  "description": "Contenedor de respuesta estandarizado para la intención analizada.",
  "properties": {
    "action_name": {
      "description": "Campo 'action_name'",
      "title": "Action Name",
      "type": "string"
    },
    "params": {
      "additionalProperties": true,
      "description": "Campo 'params'",
      "title": "Params",
      "type": "object"
    },
    "confidence": {
      "default": 0.0,
      "description": "Campo 'confidence'",
      "title": "Confidence",
      "type": "number"
    }
  },
  "required": [
    "action_name"
  ],
  "title": "IntentResult",
  "type": "object"
}
```
</details>

---

## 🔷 Clases Base Abstractas (Contratos)

Interfaces que definen contratos obligatorios para las implementaciones concretas.

### `BaseCommand`

🔷 **Tipo**: Clase Base Abstracta (ABC)  
📁 **Módulo**: `src/SL/command_handler/base_command.py`

> Clase base que define los contratos que va a seguir cada comando

#### Métodos

##### `execute(dictionary: dict) → Any`

Ejecuta un comando 

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `dictionary` | `dict` | — |

---

### `BaseAdapter`

🔷 **Tipo**: Clase Base Abstracta (ABC)  
📁 **Módulo**: `src/SL/os_engine/base_adapter.py`

> Clase Base Abstracta que define el contrato estricto para los adaptadores de
Sistema Operativo (Windows, Linux, etc.).

Cualquier adaptador concreto DEBE implementar todos los métodos marcados
con @abstractmethod.

#### Métodos

##### `execute_system_command(command: str) → tuple[bool, str]` 🔸 `@abstractmethod`

Ejecuta un comando arbitrario de consola y captura la respuesta.

:param command: Comando de consola (Bash/CMD/PowerShell).
:return: Tupla con (Éxito: bool, Salida/Error: str).

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `command` | `str` | Comando de consola (Bash/CMD/PowerShell). |

**Retorna**: Tupla con (Éxito: bool, Salida/Error: str).

##### `is_process_running(process_name: str) → bool` 🔸 `@abstractmethod`

Consulta si un proceso se encuentra activo en la lista de tareas del SO.

:param process_name: Nombre o fragmento del ejecutable a buscar.
:return: True si el proceso está corriendo, False en caso contrario.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `process_name` | `str` | Nombre o fragmento del ejecutable a buscar. |

**Retorna**: True si el proceso está corriendo, False en caso contrario.

##### `open_application(app_path_or_cmd: str) → bool` 🔸 `@abstractmethod`

Abre una aplicación de forma asíncrona (no bloqueante).

:param app_path_or_cmd: Ruta ejecutable o comando de sistema.
:return: True si se inició correctamente, False si falló.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `app_path_or_cmd` | `str` | Ruta ejecutable o comando de sistema. |

**Retorna**: True si se inició correctamente, False si falló.

##### `open_url(url: str) → bool` 🔸 `@abstractmethod`

Abre un enlace web en el navegador predeterminado del sistema.

:param url: Dirección web completa (ej. "https://google.com").
:return: True si se envió la orden de apertura, False si falló.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `url` | `str` | Dirección web completa (ej. "https://google.com"). |

**Retorna**: True si se envió la orden de apertura, False si falló.

---

### `BaseAppFinder`

🔷 **Tipo**: Clase Base Abstracta (ABC)  
📁 **Módulo**: `src/SL/app_finder/base_finder.py`

> Clase base abstracta que define el contrato estricto para los finders de cada SO


Cualquier finder concreto DEBE implementar todos los métodos marcados
con @abstractmethod.

#### Métodos

##### `get_apps() → dict[str, str]` 🔸 `@abstractmethod`

Escanea el sistema operativo en busca de aplicaciones instaladas.

Return:
    Un diccionario/mapa de pares clave-valor donde:
    - Clave: Nombre de la aplicación en minúsculas (ej: "google chrome", "spotify").
    - Valor: Ruta absoluta al ejecutable, acceso directo o comando del sistema
             (ej: "/usr/bin/google-chrome" o "C:\Program Files\...\spotify.exe").

**Retorna**: Un diccionario/mapa de pares clave-valor donde: - Clave: Nombre de la aplicación en minúsculas (ej: "google chrome", "spotify"). - Valor: Ruta absoluta al ejecutable, acceso directo o comando del sistema (ej: "/usr/bin/google-chrome" o "C:\Program Files\...\spotify.exe").

---

### `BaseIntentRecognizer`

🔷 **Tipo**: Clase Base Abstracta (ABC)  
📁 **Módulo**: `src/NLU/intent_recognizer/base_recognizer.py`

> Sin documentación.

#### Métodos

##### `parse(user_text: str) → IntentResult` 🔸 `@abstractmethod`

Analiza el texto del usuario y extrae la intención

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `user_text` | `str` | — |

---
