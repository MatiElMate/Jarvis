import unicodedata
import re

def text_normalizer(text:str) -> str:
    """
    Normaliza y limpia la cadena de texto de entrada:
    - Convierte a minúsculas.
    - Remueve signos de acentuación/diacríticos (ej. 'canción' -> 'cancion').
    - Remueve signos de puntuación (ej. '¿', '?', '!', ',', etc.).
    - Colapsa espacios múltiples en uno solo y recorta bordes.

    :param text: Texto de entrada del usuario.
    :return: Texto limpio y listo para procesamiento por RegEx o NLP.
    """
    
    if not text or not text.strip():
        return ""

    cleaned = unicodedata.normalize('NFD',text)
    cleaned = "".join(char for char in cleaned if unicodedata.category(char) != 'Mn')


    cleaned = re.sub(r':(?!\/\/)|[?¿!¡,;\"\']', '', cleaned)


    cleaned = re.sub(r"\s", " ", cleaned).strip()

    return cleaned