# Asset · Informe de mercado ficticio
**Usar en:** M6 · Escena 4 (Análisis de datos y documentos)

---

## Contexto para el narrador

Informe de 5-7 páginas (cuando se convierta a PDF) sobre el mercado de la IA aplicada a productividad en pymes. Tiene datos plausibles pero ficticios. La idea es que Claude extraiga las 5 conclusiones clave, cite los datos más fuertes con número de página, e identifique qué información falta o está poco respaldada.

**Conversión a PDF:** abre este markdown en cualquier conversor (Pandoc, browser print, etc.) y exporta como PDF antes de grabar. Mantén numeración de página visible.

---

## Documento (markdown → PDF)

```markdown
# Estado del mercado: IA aplicada a productividad en pymes
## Informe de tendencias — Q1 2026

**Editor:** Observatorio Ficticio de Tecnologías Aplicadas
**Fecha:** Mayo 2026
**Páginas:** 7

---

## Resumen ejecutivo

El mercado de soluciones de inteligencia artificial dirigidas a
pequeñas y medianas empresas (pymes) ha experimentado un
crecimiento del **38% interanual** durante 2025, con un total
estimado de **2.4 millones de empresas** en Europa que han
incorporado al menos una herramienta de IA en sus operaciones.

A pesar del crecimiento, la **adopción profunda** — entendida
como uso diario por más del 50% del equipo — se mantiene en
torno al **12%**, lo que sugiere una brecha significativa entre
la prueba inicial y la integración sostenida.

---

## 1. Magnitud del mercado

El gasto agregado de pymes europeas en herramientas de IA
alcanzó los **3.200 millones de euros** en 2025, frente a los
**2.320 millones** del año anterior. España representa el
**11%** de ese gasto, por detrás de Alemania (24%), Reino
Unido (19%) y Francia (15%).

El segmento de mayor crecimiento ha sido el de **asistentes
generales tipo conversacional** (Claude, ChatGPT, Gemini),
con un avance del **52% interanual**. Las herramientas
verticales — analítica, marketing, RRHH — crecieron entre
un 25% y un 35%.

---

## 2. Patrones de adopción

Tres patrones identificados:

**Patrón A — adopción individual sin política corporativa**
(estimado en el 58% de los casos). Empleados que usan IA por
iniciativa propia, sin acuerdos formales con proveedores. Riesgo
elevado de filtración de datos. Documentado en encuestas a 340
empresas.

**Patrón B — adopción departamental** (28% de los casos).
Un equipo concreto — habitualmente marketing o atención al
cliente — formaliza el uso. Resto de la organización ajeno.

**Patrón C — adopción transversal con gobierno** (14%).
Empresas con políticas claras, formación interna, y métricas
de uso. Concentradas en sectores regulados (financiero,
sanitario).

---

## 3. Principales actores

Por cuota de mercado en el segmento pyme europeo:

- **Anthropic (Claude):** 28%
- **OpenAI (ChatGPT y derivados):** 41%
- **Google (Gemini):** 14%
- **Microsoft (Copilot):** 12%
- **Otros (Mistral, locales, etc.):** 5%

La cuota de Anthropic ha crecido **9 puntos** durante 2025,
ganando terreno especialmente en servicios profesionales y
sectores creativos.

---

## 4. Barreras a la adopción

Las cinco barreras más citadas por responsables de IT en pymes
(encuesta interna, n=420):

1. **Preocupación por privacidad de datos** — citada por el 67%.
2. **Falta de tiempo para evaluación** — 54%.
3. **Coste de licencias** — 49%.
4. **Dificultad de integración con sistemas existentes** — 38%.
5. **Resistencia interna del equipo** — 24%.

---

## 5. Casos de uso predominantes

Por frecuencia declarada:

- Redacción y revisión de textos: 78%
- Análisis de documentos: 52%
- Atención al cliente (chatbots): 41%
- Análisis de datos y reportes: 36%
- Generación de código: 29%
- Creación de imágenes y diseño: 22%

---

## 6. Conclusiones

1. El mercado crece a doble dígito pero la adopción profunda
   sigue siendo minoritaria.
2. Anthropic gana cuota en pymes europeas, especialmente en
   servicios profesionales.
3. La preocupación por privacidad sigue siendo la mayor
   barrera — más que el coste.
4. La adopción individual sin políticas corporativas representa
   un riesgo creciente de filtración.
5. Los sectores regulados lideran la adopción transversal.

---

## 7. Limitaciones del estudio

- Datos basados en muestras de 420 empresas (encuestas
  internas) y datos públicos de proveedores.
- No se ha podido medir el ROI real para las empresas
  encuestadas; las cifras son percepciones.
- Sectores agrícola y construcción están infrarrepresentados.
```

---

## Prompt a usar tras subirlo a Claude

```
Adjunto un informe de mercado. Hazme tres cosas:
1) Identifica las cinco conclusiones clave.
2) Cita los datos más fuertes (con la página donde aparecen).
3) Dime qué información falta o está poco respaldada.
```

---

## Conversión rápida a PDF (para grabar)

```bash
# Desde el terminal, dentro de la carpeta assets:
pandoc 08-informe-mercado.md -o 08-informe-mercado.pdf

# Alternativa sin pandoc:
# 1. Abrir el .md en Typora, MarkText, o VS Code con preview
# 2. Imprimir → Guardar como PDF
```
