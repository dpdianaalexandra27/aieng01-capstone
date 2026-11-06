import json
import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("incidentes")
RUTA_DATOS = os.path.join(os.path.dirname(__file__), "datos", "incidentes.json")

def _cargar():
    with open(RUTA_DATOS, "r", encoding="utf-8") as f:
        return json.load(f)

@mcp.tool()
def obtener_ticket(id_ticket: str) -> str:
    """Busca un ticket tecnico por su codigo (por ejemplo INC-101)."""
    datos = _cargar()
    ticket = datos.get("tickets", {}).get(id_ticket)
    if not ticket:
        return f"Error: No existe el ticket '{id_ticket}'."
    return json.dumps(ticket, ensure_ascii=False)

if __name__ == "__main__":
    mcp.run()
