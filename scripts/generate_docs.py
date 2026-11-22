#!/usr/bin/env python3
"""
Generador automático de documentación a partir de los objetos base del proyecto.

Introspecciona los dataclasses y ABCs existentes, genera modelos Pydantic espejo
(sin modificar el código fuente), y exporta:
  - JSON Schema por cada objeto
  - Un documento Markdown consolidado con toda la referencia

Uso:
    python scripts/generate_docs.py
"""

import inspect
import json
import sys
import os
import dataclasses
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, get_type_hints

# Agregar el root del proyecto al path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from pydantic import BaseModel, Field, create_model

# ─────────────────────────────────────────────
# Configuración: Qué objetos documentar
# ─────────────────────────────────────────────

# Importar todos los objetos base
from src.SL.command_handler.base_command import CommandResult, BaseCommand
from src.SL.app_finder.base_finder import BaseAppFinder
from src.SL.os_engine.base_adapter import BaseAdapter
from src.NLU.intent_recognizer.base_recognizer import IntentResult, BaseIntentRecognizer

OUTPUT_DIR = PROJECT_ROOT / "docs" / "api_reference"


# ─────────────────────────────────────────────
# Utilidades de introspección
# ─────────────────────────────────────────────

def _python_type_to_str(tp: Any) -> str:
    """Convierte un tipo Python a su representación legible en string."""
    origin = getattr(tp, "__origin__", None)
    args = getattr(tp, "__args__", None)

    if tp is type(None):
        return "None"
    if tp is inspect.Parameter.empty or tp is inspect._empty:
        return "Any"
    if origin is not None:
        origin_name = getattr(origin, "__name__", str(origin))
        if origin_name == "Union" and args and type(None) in args:
            inner = [_python_type_to_str(a) for a in args if a is not type(None)]
            return f"Optional[{', '.join(inner)}]"
        if args:
            inner = ", ".join(_python_type_to_str(a) for a in args)
            return f"{origin_name}[{inner}]"
        return origin_name
    if hasattr(tp, "__name__"):
        return tp.__name__
    return str(tp)


def _extract_docstring_params(docstring: str) -> Dict[str, str]:
    """Extrae descripciones de parámetros desde un docstring (:param ... / :return ...)."""
    params = {}
    if not docstring:
        return params

    current_key = None
    for line in docstring.split("\n"):
        stripped = line.strip()
        if stripped.startswith(":param "):
            parts = stripped[6:].split(":", 1)
            if len(parts) == 2:
                current_key = parts[0].strip()
                params[current_key] = parts[1].strip()
        elif stripped.startswith(":return:"):
            current_key = "_return"
            params[current_key] = stripped[8:].strip()
        elif stripped.startswith("Return:"):
            current_key = "_return"
            params[current_key] = ""
        elif current_key and stripped and not stripped.startswith(":"):
            params[current_key] = (params.get(current_key, "") + " " + stripped).strip()

    return params


# ─────────────────────────────────────────────
# Generador de modelos Pydantic desde dataclasses
# ─────────────────────────────────────────────

def dataclass_to_pydantic(dc_cls) -> type[BaseModel]:
    """
    Convierte un dataclass existente a un modelo Pydantic espejo,
    preservando nombres, tipos, defaults y docstrings.
    """
    fields = {}
    hints = get_type_hints(dc_cls)
    dc_fields = dataclasses.fields(dc_cls)

    doc_params = _extract_docstring_params(dc_cls.__doc__ or "")

    for f in dc_fields:
        field_type = hints.get(f.name, Any)
        description = doc_params.get(f.name, f"Campo '{f.name}'")

        if f.default is not dataclasses.MISSING:
            fields[f.name] = (field_type, Field(default=f.default, description=description))
        elif f.default_factory is not dataclasses.MISSING:
            fields[f.name] = (field_type, Field(default_factory=f.default_factory, description=description))
        else:
            fields[f.name] = (field_type, Field(..., description=description))

    model = create_model(
        dc_cls.__name__,
        __doc__=dc_cls.__doc__,
        **fields
    )
    return model


# ─────────────────────────────────────────────
# Introspección de ABCs
# ─────────────────────────────────────────────

def introspect_abc(abc_cls) -> Dict[str, Any]:
    """
    Introspecciona una clase ABC y devuelve un diccionario con
    toda su información documentable.
    """
    info = {
        "name": abc_cls.__name__,
        "module": abc_cls.__module__,
        "docstring": inspect.cleandoc(abc_cls.__doc__ or "Sin documentación."),
        "methods": []
    }

    for name, method in inspect.getmembers(abc_cls, predicate=inspect.isfunction):
        if name.startswith("_") and name != "__init__":
            continue

        sig = inspect.signature(method)
        doc = inspect.cleandoc(method.__doc__ or "")
        doc_params = _extract_docstring_params(method.__doc__ or "")
        hints = get_type_hints(method) if method.__doc__ else {}

        params = []
        for pname, param in sig.parameters.items():
            if pname == "self":
                continue
            param_type = hints.get(pname, param.annotation)
            params.append({
                "name": pname,
                "type": _python_type_to_str(param_type),
                "description": doc_params.get(pname, ""),
                "default": str(param.default) if param.default is not inspect.Parameter.empty else None
            })

        return_type = hints.get("return", sig.return_annotation)

        method_info = {
            "name": name,
            "is_abstract": getattr(method, "__isabstractmethod__", False),
            "docstring": doc,
            "params": params,
            "return_type": _python_type_to_str(return_type),
            "return_description": doc_params.get("_return", "")
        }
        info["methods"].append(method_info)

    return info


# ─────────────────────────────────────────────
# Generación de JSON Schema
# ─────────────────────────────────────────────

def generate_abc_json_schema(abc_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Genera un JSON Schema-like para una ABC, documentando sus métodos como
    un contrato de interfaz.
    """
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": abc_info["name"],
        "description": abc_info["docstring"],
        "type": "object",
        "x-module": abc_info["module"],
        "x-kind": "abstract_base_class",
        "x-methods": {}
    }

    for method in abc_info["methods"]:
        method_schema = {
            "description": method["docstring"],
            "x-abstract": method["is_abstract"],
            "parameters": {},
            "returns": {
                "type": method["return_type"],
                "description": method["return_description"]
            }
        }
        for param in method["params"]:
            param_entry = {
                "type": param["type"],
                "description": param["description"]
            }
            if param["default"] is not None:
                param_entry["default"] = param["default"]
            method_schema["parameters"][param["name"]] = param_entry

        schema["x-methods"][method["name"]] = method_schema

    return schema


# ─────────────────────────────────────────────
# Generación de Markdown
# ─────────────────────────────────────────────

def _generate_dataclass_markdown(name: str, pydantic_model: type[BaseModel], source_file: str) -> str:
    """Genera sección Markdown para un dataclass documentado vía Pydantic."""
    schema = pydantic_model.model_json_schema()
    lines = []
    lines.append(f"### `{name}`")
    lines.append(f"")
    lines.append(f"📦 **Tipo**: Data Class  ")
    lines.append(f"📁 **Módulo**: `{source_file}`")
    lines.append(f"")

    if schema.get("description"):
        lines.append(f"> {schema['description']}")
        lines.append(f"")

    # Tabla de campos
    props = schema.get("properties", {})
    required = set(schema.get("required", []))
    if props:
        lines.append(f"| Campo | Tipo | Requerido | Default | Descripción |")
        lines.append(f"|-------|------|-----------|---------|-------------|")
        for field_name, field_info in props.items():
            ftype = field_info.get("type", field_info.get("anyOf", "—"))
            if isinstance(ftype, list):
                ftype = " \\| ".join(str(t) for t in ftype)
            elif isinstance(ftype, dict):
                ftype = str(ftype)

            # Manejar anyOf para Optional types
            any_of = field_info.get("anyOf")
            if any_of:
                types = []
                for t in any_of:
                    if "type" in t:
                        types.append(f"`{t['type']}`")
                    elif t.get("type") == "null":
                        types.append("`null`")
                ftype = " \\| ".join(types) if types else str(any_of)
            else:
                ftype = f"`{ftype}`"

            is_required = "✅" if field_name in required else "❌"
            default = field_info.get("default", "—")
            if default is None:
                default = "`None`"
            elif default == "—":
                default = "—"
            else:
                default = f"`{default}`"
            desc = field_info.get("description", "—")
            lines.append(f"| `{field_name}` | {ftype} | {is_required} | {default} | {desc} |")
        lines.append("")

    # JSON Schema colapsable
    lines.append(f"<details>")
    lines.append(f"<summary>📋 JSON Schema completo</summary>")
    lines.append(f"")
    lines.append(f"```json")
    lines.append(json.dumps(schema, indent=2, ensure_ascii=False))
    lines.append(f"```")
    lines.append(f"</details>")
    lines.append(f"")

    return "\n".join(lines)


def _generate_abc_markdown(abc_info: Dict[str, Any], source_file: str) -> str:
    """Genera sección Markdown para una ABC."""
    lines = []
    lines.append(f"### `{abc_info['name']}`")
    lines.append(f"")
    lines.append(f"🔷 **Tipo**: Clase Base Abstracta (ABC)  ")
    lines.append(f"📁 **Módulo**: `{source_file}`")
    lines.append(f"")

    if abc_info["docstring"]:
        lines.append(f"> {abc_info['docstring']}")
        lines.append(f"")

    lines.append(f"#### Métodos")
    lines.append(f"")

    for method in abc_info["methods"]:
        # Firma del método
        params_str = ", ".join(
            f"{p['name']}: {p['type']}" + (f" = {p['default']}" if p['default'] else "")
            for p in method["params"]
        )
        abstract_badge = " 🔸 `@abstractmethod`" if method["is_abstract"] else ""
        lines.append(f"##### `{method['name']}({params_str}) → {method['return_type']}`{abstract_badge}")
        lines.append(f"")

        if method["docstring"]:
            lines.append(f"{method['docstring']}")
            lines.append(f"")

        # Tabla de parámetros
        if method["params"]:
            lines.append(f"| Parámetro | Tipo | Descripción |")
            lines.append(f"|-----------|------|-------------|")
            for p in method["params"]:
                lines.append(f"| `{p['name']}` | `{p['type']}` | {p['description'] or '—'} |")
            lines.append(f"")

        if method["return_description"]:
            lines.append(f"**Retorna**: {method['return_description']}")
            lines.append(f"")

    return "\n".join(lines)


def generate_full_markdown(documented_objects: List[Dict[str, Any]]) -> str:
    """Genera el documento Markdown completo con toda la documentación."""
    lines = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines.append(f"# 📖 Referencia de API — Jarvis")
    lines.append(f"")
    lines.append(f"> Documentación auto-generada el **{timestamp}**  ")
    lines.append(f"> Generada con Pydantic `model_json_schema()` + introspección de ABCs")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    # Índice
    lines.append(f"## Índice")
    lines.append(f"")
    for obj in documented_objects:
        emoji = "📦" if obj["kind"] == "dataclass" else "🔷"
        anchor = obj["name"].lower().replace(" ", "-")
        lines.append(f"- {emoji} [`{obj['name']}`](#{anchor})")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    # Sección: Data Classes
    dataclasses_objs = [o for o in documented_objects if o["kind"] == "dataclass"]
    if dataclasses_objs:
        lines.append(f"## 📦 Data Classes (Modelos de Datos)")
        lines.append(f"")
        lines.append(f"Objetos de datos con validación de tipos. Documentados mediante modelos Pydantic espejo.")
        lines.append(f"")
        for obj in dataclasses_objs:
            lines.append(obj["markdown"])
            lines.append(f"---")
            lines.append(f"")

    # Sección: ABCs
    abc_objs = [o for o in documented_objects if o["kind"] == "abc"]
    if abc_objs:
        lines.append(f"## 🔷 Clases Base Abstractas (Contratos)")
        lines.append(f"")
        lines.append(f"Interfaces que definen contratos obligatorios para las implementaciones concretas.")
        lines.append(f"")
        for obj in abc_objs:
            lines.append(obj["markdown"])
            lines.append(f"---")
            lines.append(f"")

    return "\n".join(lines)


# ─────────────────────────────────────────────
# Pipeline principal
# ─────────────────────────────────────────────

# Registro de objetos a documentar: (clase, ruta_relativa_fuente, tipo)
OBJECTS_TO_DOCUMENT = [
    (CommandResult,        "src/SL/command_handler/base_command.py",      "dataclass"),
    (IntentResult,         "src/NLU/intent_recognizer/base_recognizer.py", "dataclass"),
    (BaseCommand,          "src/SL/command_handler/base_command.py",      "abc"),
    (BaseAdapter,          "src/SL/os_engine/base_adapter.py",            "abc"),
    (BaseAppFinder,        "src/SL/app_finder/base_finder.py",            "abc"),
    (BaseIntentRecognizer, "src/NLU/intent_recognizer/base_recognizer.py", "abc"),
]


def main():
    print("🚀 Generando documentación de objetos base...\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    schemas_dir = OUTPUT_DIR / "schemas"
    schemas_dir.mkdir(exist_ok=True)

    documented = []

    for cls, source_file, kind in OBJECTS_TO_DOCUMENT:
        print(f"  📝 Procesando: {cls.__name__} ({kind})")

        if kind == "dataclass":
            pydantic_model = dataclass_to_pydantic(cls)
            schema = pydantic_model.model_json_schema()

            # Guardar JSON Schema
            schema_path = schemas_dir / f"{cls.__name__}.schema.json"
            with open(schema_path, "w", encoding="utf-8") as f:
                json.dump(schema, f, indent=2, ensure_ascii=False)
            print(f"    ✅ Schema JSON → {schema_path.relative_to(PROJECT_ROOT)}")

            md = _generate_dataclass_markdown(cls.__name__, pydantic_model, source_file)
            documented.append({
                "name": cls.__name__,
                "kind": kind,
                "markdown": md,
                "schema": schema
            })

        elif kind == "abc":
            abc_info = introspect_abc(cls)
            schema = generate_abc_json_schema(abc_info)

            # Guardar JSON Schema
            schema_path = schemas_dir / f"{cls.__name__}.schema.json"
            with open(schema_path, "w", encoding="utf-8") as f:
                json.dump(schema, f, indent=2, ensure_ascii=False)
            print(f"    ✅ Schema JSON → {schema_path.relative_to(PROJECT_ROOT)}")

            md = _generate_abc_markdown(abc_info, source_file)
            documented.append({
                "name": cls.__name__,
                "kind": kind,
                "markdown": md,
                "schema": schema
            })

    # Generar Markdown consolidado
    full_md = generate_full_markdown(documented)
    md_path = OUTPUT_DIR / "API_REFERENCE.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(full_md)
    print(f"\n  📄 Markdown completo → {md_path.relative_to(PROJECT_ROOT)}")

    print(f"\n✅ Documentación generada exitosamente en: {OUTPUT_DIR.relative_to(PROJECT_ROOT)}/")
    print(f"   - {len([d for d in documented if d['kind'] == 'dataclass'])} Data Classes documentados")
    print(f"   - {len([d for d in documented if d['kind'] == 'abc'])} ABCs documentadas")
    print(f"   - {len(documented)} JSON Schemas generados")


if __name__ == "__main__":
    main()
