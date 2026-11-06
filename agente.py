import sys
from claude_agent_sdk import ClaudeAgentOptions, AgentDefinition

SYSTEM = """Eres un asistente de soporte tecnico L1 y gestion de incidentes de TI.
Tu trabajo es atender consultas sobre fallas en servidores y bases de datos.
Usa tu herramienta mcp__incidentes__obtener_ticket para consultar la informacion del ticket.

Regla obligatoria de proceso:
Para tickets criticos (P1 o P2), antes de dar tu conclusion final, consulta al subagente 'auditor_sla' para que valide el impacto y la urgencia del escalamiento."""

SERVIDORES = {
    "incidentes": {
        "command": "python",
        "args": ["server.py"]
    }
}

HERRAMIENTAS = [
    "mcp__incidentes__obtener_ticket"
]

AGENTES = {
    "auditor_sla": AgentDefinition(
        description="Auditor especializado en SLAs e impacto critico. Valida si un incidente debe escalarse inmediatamente.",
        prompt=(
            "Eres el auditor de incidentes criticos. Revisa el ticket consultado y responde unicamente con: "
            "'ESCALAR_INMEDIATO: <motivo>' o 'SLA_BAJO_CONTROL: <motivo>'."
        ),
        tools=["mcp__incidentes__obtener_ticket"],
        model="inherit",
    ),
}

def opciones():
    return ClaudeAgentOptions(
        system_prompt=SYSTEM,
        mcp_servers=SERVIDORES,
        agents=AGENTES,
        tools=["Agent"],
        allowed_tools=HERRAMIENTAS + ["Agent"],
    )
