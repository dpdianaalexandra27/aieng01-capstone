# TriageOps - Agente de Triage y Diagnóstico de Incidentes de TI

## El caso
- **Quién lo usa:** Ingenieros de soporte L1 y personal de operaciones de TI.
- **Qué le pide:** Diagnosticar fallas técnicas en servidores y bases de datos a partir del código de ticket (ej. INC-101), auditar el impacto en SLAs y sugerir remediación.
- **Cómo se sabe que lo resolvió:** El agente obtiene los detalles exactos del incidente vía MCP y delega en el subagente para emitir la recomendación formal de escalamiento.

## Arquitectura
Entrada -> Guardrail de Entrada -> Orquestador (ClaudeAgentSDK) -> Servidor MCP (FastMCP) / Subagente (auditor_sla) -> Guardrail de Salida -> Respuesta

**Por qué un subagente aquí:**
Aísla la lógica estricta de evaluación de tiempos y criticidad de SLAs sin contaminar el prompt del orquestador, garantizando dictámenes consistentes sobre incidentes P1 y P2.

## Cómo correrlo
python adaptador.py "¿Cuál es el estado del ticket INC-101 y debemos escalarlo según el auditor?"
python evals.py --etiqueta despues
python evals.py --comparar antes despues

## Evaluación
- **Golden set:** 8 casos de prueba estructurados (6 funcionales/borde y 2 adversariales).
- **Resultado antes -> después:** 8/8 -> 8/8 casos aprobados satisfactoriamente.
- **Análisis:** Bloqueo íntegro de solicitudes adversariales y extracción correcta de datos técnicos sin alucinación.

## Guardrails
- **Entrada:** Filtro regex contra inyecciones de prompt, órdenes destructivas y solicitudes de contraseñas o tokens.
- **Salida:** Enmascaramiento automático de secretos o credenciales expuestas hacia [REDACTED].

## Costo
- **Costo base por corrida:** ~USD 0.088 por lote completo de evaluación (~USD 0.011 por consulta compleja).
- **Palanca de ahorro:** Reducción de herramientas innecesarias en el subagente y límites estrictos de contexto. Proyección: ~USD 11.00 por cada 1.000 consultas.

## Límites
Opera sobre datos locales simulados en JSON. En una siguiente iteración se conectará a APIs en vivo de Datadog y AWS CloudWatch con remediación automatizada.
