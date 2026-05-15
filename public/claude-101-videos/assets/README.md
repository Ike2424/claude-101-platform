# Assets de demo · Claude 101 videos

Carpeta de **insumos ficticios** que los guiones referencian. Antes de grabar cada módulo, ten estos archivos preparados (subidos a Claude o abiertos en pantalla según corresponda).

---

## Inventario

| # | Archivo | Usado en | Tipo | Para qué sirve |
|---|---|---|---|---|
| 01 | `01-email-borrador-frustrado.md` | M6 esc. 2 | Texto | Borrador "malo" para que Claude reescriba |
| 02 | `02-codigo-con-bug.js` | M6 esc. 3 | JS | Bug de `null` para demo de debug |
| 03 | `03-codigo-heredado.py` | M6 esc. 3 | Python | Código sin comentarios para "explica este código" |
| 04 | `04-contrato-ficticio.md` | M4 esc. 2 | Texto | Contrato con 3 cláusulas problemáticas |
| 05 | `05-brief-cafe-aurora.md` | M2, M5, M8 | Texto | Brief del cliente recurrente "Café Aurora" |
| 06 | `06-ventas-mensuales.csv` | M6 esc. 4 | CSV | 12 meses × 5 líneas de producto para análisis |
| 07 | `07-articulo-para-reescribir.md` | M4 esc. 5, 6 | Texto | Artículo malo para reescritura por rol/few-shot |
| 08 | `08-informe-mercado.md` | M6 esc. 4 | Markdown → PDF | Informe de 7 pp. para extracción de conclusiones |
| 09 | `09-transcripcion-reunion.md` | M3 esc. 5 | Texto | Acta de reunión para demo de prompt sólido vs. débil |

---

## Preparación antes de grabar

### Convertir a los formatos que pide cada demo

| Asset | Conversión necesaria |
|---|---|
| `06-ventas-mensuales.csv` | Abrir en Excel y guardar como `.xlsx` (más visual en la grabación) |
| `08-informe-mercado.md` | Convertir a `.pdf` (ver instrucciones en el propio archivo) |
| El resto | Se copian y pegan directamente en el chat |

### Subir a Drive (para M8 — demo MCP)

Antes de grabar M8, sube a una carpeta llamada **"Café Aurora"** en tu Google Drive de la cuenta demo:
- `05-brief-cafe-aurora.md` (preferiblemente convertido a Google Doc o .docx).

Eso permite que la demo `"Mira en mi Google Drive si tengo el brief..."` funcione.

### Crear el repo de prueba (para M8 — demo Claude Code)

Para la demo de Claude Code, necesitas un repo pequeño con un bug de CSS:
- Clona cualquier landing page open source (o crea una con `npm create vite@latest`).
- Introduce un bug evidente: un botón pegado al logo en mobile, sin respetar `tailwind.config.js`.
- Anota el path del archivo afectado (sugerido: `components/Header.tsx`).

---

## Privacidad

Todos los nombres, empresas, números y casos son **ficticios**. Aun así:

- **No sustituyas** los datos ficticios por datos reales de tus clientes o tu empresa antes de grabar.
- Si grabas con tu propia cuenta de Claude (no la demo), borra el historial antes de grabar para que no aparezcan conversaciones reales en el sidebar.
- Para la demo de MCP en M8: usa una cuenta demo de Google con un Drive limpio.

---

## Ampliaciones opcionales

Si tras grabar quieres reforzar algún módulo:

- **M4 ejemplos extra de few-shot:** se pueden añadir 2-3 pares más al ejemplo de titulares.
- **M6 imagen de dashboard:** descarga una captura de un dashboard de demo (Stripe, Mixpanel, etc.) y úsala para la demo de análisis de gráficos.
- **M5 prompt visual de Artifacts:** se puede preparar un brief más elaborado para generar una landing page completa en lugar de una calculadora.
