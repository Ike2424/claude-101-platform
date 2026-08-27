# Prompts del caso García

> **Material de ejemplo del libro «IA para Abogados».** Todo es ficticio y con
> fines educativos. No es asesoramiento jurídico. Anonimiza siempre los datos
> reales de tus clientes antes de usar cualquier herramienta de IA.

El Sr. García es comercial, con siete años de antigüedad, despedido por carta
alegando un bajo rendimiento que la empresa no acredita. Estos son los prompts
que acompañan su caso a lo largo del libro.

---

## 1. El prompt genérico — lo que NO funciona

```
¿Este despido es válido?
```

Respuesta genérica de manual: te suelta la teoría del despido disciplinario, sin
tu contexto, sin tu criterio y sin mirar los papeles. Inservible para el asunto.

---

## 2. El prompt jurídico — el del Sr. García (capítulo 4)

```
ROL
Actúa como abogado laboralista español con experiencia en despido disciplinario.

CONTEXTO
- Cliente: comercial, 7 años de antigüedad.
- Despido disciplinario comunicado por carta.
- Causa alegada: bajo rendimiento continuado.
- La empresa NO aporta datos objetivos que acrediten ese bajo rendimiento.
- Te adjunto la carta de despido (documento adjunto).

TAREA
Analiza la carta y localiza:
  a) Defectos de forma (fechas, hechos concretos, firma, puesta a disposición…).
  b) Debilidades de fondo (falta de acreditación del bajo rendimiento).
  c) Argumentos para solicitar la improcedencia.

FORMATO
Devuélvelo en una tabla con columnas: [Punto | Por qué | Riesgo para la empresa].

VERIFICACIÓN
No des por cierto ningún dato que no aparezca en la carta. Al final, indícame
qué debo comprobar yo antes de dar un paso (convenio aplicable, plazos, etc.).
```

Misma IA, mismo caso: la diferencia en la calidad de la respuesta es radical,
porque ahora sabe exactamente lo que necesitas.

---

## 3. Prompts por fase del caso

**Entrega II — Proyecto «García. Despido» (capítulo 5).**
Instrucciones permanentes del proyecto:
```
Este proyecto es el asunto «García. Despido». Trabaja siempre como abogado
laboralista español. Usa un tono sobrio y de escrito judicial. Cíñete a los
documentos del proyecto. Si te falta un dato, pídemelo; no lo inventes.
```

**Entrega III — OCR y anonimización en local (capítulo 6).**
```
Te paso el texto ya extraído (OCR) del burofax escaneado. Está anonimizado.
Normalízalo a Markdown limpio, respeta fechas y numeración, y márcame en
[CORCHETES] cualquier dato personal que se haya podido colar sin anonimizar.
```

**Entrega IV — Recordatorios de plazos (capítulo 7).**
```
A partir de la fecha de la papeleta de conciliación, calcula el plazo de la
demanda por despido y créame un recordatorio con DOS avisos previos. Dame las
fechas exactas y qué debo tener listo en cada aviso.
```

**Entrega V — Reparto entre varios agentes (capítulo 8).**
```
Reparte el análisis del asunto (anonimizado) entre tus mejores capacidades:
uno resume el expediente, otro localiza defectos de forma, otro redacta el
borrador de hechos de la demanda. Devuélveme cada parte por separado.
```
