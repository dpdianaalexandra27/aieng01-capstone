import re
from collections import namedtuple

Decision = namedtuple("Decision", ["permitir", "motivo", "texto"])

PATRONES_INYECCION = [
    r"ignora\s+(tus|las)?\s*instrucciones",
    r"borra\s+todos?\s+los?\s*tickets?",
    r"password|contrase[ñn]a",
    r"token|secret|api[_-]?key",
]

def revisar_entrada(pregunta: str) -> Decision:
    """Valida la entrada detectando inyecciones y terminos prohibidos."""
    pregunta_baja = pregunta.lower()
    for patron in PATRONES_INYECCION:
        if re.search(patron, pregunta_baja):
            return Decision(
                permitir=False,
                motivo="Bloqueado por guardrail: contenido no permitido o fuera de alcance.",
                texto=pregunta
            )
    return Decision(permitir=True, motivo="OK", texto=pregunta)

def revisar_salida(respuesta: str, contexto: str = "") -> Decision:
    """Valida y enmascara posibles secretos en la salida antes de entregarla."""
    limpia = re.sub(r"(?i)(password|secret|token)\s*[:=]\s*\S+", r"\1: [REDACTED]", respuesta)
    return Decision(permitir=True, motivo="OK", texto=limpia)
