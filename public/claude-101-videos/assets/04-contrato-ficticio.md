# Asset · Fragmento de contrato ficticio
**Usar en:** M4 · Escena 2 (Cadenas de razonamiento)

---

## Contexto para el narrador

Contrato de servicios profesionales con tres cláusulas problemáticas:
1. **No competencia** demasiado amplia (geografía global, sin límite temporal).
2. **Propiedad intelectual** que cede TODO el trabajo previo y futuro.
3. **Penalización** desproporcionada (50% del valor del contrato por retraso de 1 día).

La idea es que Claude, con la cadena de razonamiento, identifique las tres cláusulas, explique por qué cada una es problemática, y dé una recomendación final.

---

## Texto del contrato a copiar

```
CONTRATO DE PRESTACIÓN DE SERVICIOS PROFESIONALES

Entre LA EMPRESA (en adelante "el Cliente") y LA CONSULTORA
(en adelante "la Prestadora"), se acuerda lo siguiente:

CLÁUSULA 3 — OBJETO Y ALCANCE
La Prestadora ejecutará trabajos de consultoría estratégica
para el Cliente durante un periodo de seis (6) meses, con
posibilidad de prórroga por mutuo acuerdo.

CLÁUSULA 7 — CONFIDENCIALIDAD Y NO COMPETENCIA
La Prestadora se compromete a no prestar servicios, ya sea
de manera directa o indirecta, a ninguna empresa que opere
en cualquier sector relacionado con la actividad del Cliente,
en cualquier jurisdicción del mundo, durante la vigencia del
presente contrato y de manera indefinida tras su finalización.
El incumplimiento de esta cláusula dará derecho al Cliente a
reclamar daños y perjuicios sin necesidad de probarlos.

CLÁUSULA 12 — PROPIEDAD INTELECTUAL
Toda la propiedad intelectual generada por la Prestadora,
así como aquella desarrollada con anterioridad a este contrato
y aquella que la Prestadora desarrolle durante el periodo de
vigencia para cualquier cliente, será cedida en exclusiva al
Cliente, incluyendo derechos morales en la medida en que la
ley lo permita.

CLÁUSULA 18 — PLAZOS Y PENALIZACIONES
Los entregables tienen fecha límite estricta. Cualquier
retraso, incluso de un (1) día, conllevará una penalización
del cincuenta por ciento (50%) sobre el valor total del
contrato, deducible de los pagos pendientes. Esta penalización
es acumulativa por cada día de retraso.

CLÁUSULA 23 — JURISDICCIÓN
Para cualquier controversia, las partes se someten a los
juzgados y tribunales de la ciudad sede del Cliente.
```

## Prompt a usar

Versión SIN cadena (para el "antes"):
```
Analiza este contrato y dime si lo firmo.
```

Versión CON cadena (para el "después"):
```
Analiza este contrato. Antes de darme tu conclusión, identifica
las cláusulas problemáticas una por una, explica por qué te
preocupan, y luego propón una recomendación final.
```
