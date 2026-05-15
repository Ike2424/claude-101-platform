# Claude 101 · Paquete de producción de videos

8 guiones listos para grabar — uno por módulo del curso `claude-101.html`.

Cada `.md` es un paquete completo de producción que incluye:
- Ficha técnica (duración, audiencia, tono, formato)
- Estructura escena por escena con timecodes
- Narración exacta (lista para leer en off)
- Acciones en pantalla detalladas
- Prompts de demo listos para copiar en Claude
- Checklist de pre y post-producción

---

## Índice

| # | Archivo | Módulo | Duración objetivo |
|---|---|---|---|
| 1 | `M1-bienvenida-y-fundamentos.md` | Bienvenida y fundamentos | 6:30 |
| 2 | `M2-primeros-pasos.md` | Primeros pasos | 7:00 |
| 3 | `M3-el-arte-del-prompt.md` | El arte del prompt | 7:30 |
| 4 | `M4-tecnicas-avanzadas-prompting.md` | Técnicas avanzadas de prompting | 7:00 |
| 5 | `M5-capacidades-y-herramientas.md` | Capacidades y herramientas | 7:30 |
| 6 | `M6-casos-de-uso-practicos.md` | Casos de uso prácticos | 7:30 |
| 7 | `M7-buenas-practicas-y-limites.md` | Buenas prácticas y límites | 7:00 |
| 8 | `M8-siguiente-nivel.md` | Siguiente nivel | 7:30 |

**Total estimado:** ~58 minutos de contenido final · ~5h de grabación + ~15h de edición.

---

## Cómo usar este paquete

### 1 · Preparación (antes de grabar nada)

1. Lee los 8 guiones de un tirón para tener visión de conjunto.
2. Decide quién narra. Recomendación: una sola voz para los 8 — da coherencia.
3. Define la **identidad visual** que se mantendrá en los 8 videos:
   - Paleta del curso: `#F4EFE3` (crema), `#C8542B` (naranja), `#4F5D38` (oliva), `#1C1A16` (tinta).
   - Tipografías: **Fraunces** (títulos) y **Geist** / **Inter** (subtítulos y callouts).
   - Música: una sola pista o una micro-biblioteca de 2-3 cortes.
4. Crea una **cuenta demo limpia** en Claude.ai para todas las grabaciones (no usar tu cuenta personal — evita exponer datos).
5. Prepara los **assets ficticios** que aparecen en varios módulos:
   - Cliente ficticio "Café Aurora" (M5, M8).
   - PDF de informe técnico (M5, M6, M7).
   - Excel con ventas mensuales ficticias (M6).
   - Fragmento de JS con bug (M6).
   - Repo con bug de CSS (M8).

### 2 · Orden de grabación recomendado

No grabes en orden 1→8. Optimiza por configuración:

**Bloque A — Demos con Claude.ai puro** (1 sesión):
- M1 · M2 · M3 · M4

**Bloque B — Capacidades avanzadas** (1 sesión, con búsqueda web y archivos activados):
- M5 · M6

**Bloque C — Sensibilidades** (1 sesión, ojo con datos en pantalla):
- M7

**Bloque D — Terminal + conectores** (1 sesión, requiere Claude Code y MCP):
- M8

### 3 · Configuración técnica común

| Parámetro | Valor |
|---|---|
| Resolución | 1920×1080 a 30fps (máster) |
| Resolución web | 1280×720 para embed en HTML |
| Audio voz | -16 LUFS, mono, 48 kHz |
| Música | -24 LUFS (10dB bajo la voz) |
| Codec final | H.264 MP4 + WebM como fallback |
| Subtítulos | SRT + quemados como segunda versión |

### 4 · Edición — patrones que se repiten en los 8 videos

- **Title cards:** mismo tipo en todos — Fraunces itálica, color #C8542B sobre fondo crema.
- **Callouts:** caja con borde fino, fondo translúcido, icono al principio (💡 idea · ⚠️ aviso · 📌 nota · 🧭 principio).
- **Highlights:** amarillo sobre partes "vagas" o "problemáticas", verde sobre "bien hecho".
- **Transiciones:** cruces simples (~250ms), no efectos vistosos.
- **Outro:** mismos 3 segundos al final de los 8 con el logo del curso.

### 5 · Cómo embeber el video en el HTML del curso

El HTML `claude-101.html` ya tiene infraestructura de video por lección. Para añadir un video:

1. Abre `claude-101.html` en el navegador.
2. Activa el **modo instructor** (pulsa la combinación de teclas o el botón si está visible — revisa el código para el atajo exacto).
3. Entra a la lección correspondiente.
4. Pulsa **"Añadir vídeo"**.
5. Pega la URL de YouTube/Vimeo o el MP4 directo.
6. El player se renderiza automáticamente. El indicador "tiene vídeo" se activa en el sidebar.

**Atención:** el HTML guarda los videos en `localStorage` del navegador. Si quieres que TODOS los alumnos vean los videos automáticamente, edita el array `COURSE` en el `<script>` del HTML y añade un campo `videoUrl` a cada lección — o alternativamente añade lógica para precargar `state.videos` con las URLs definitivas.

**Estrategia recomendada:** un video por **módulo** (no por lección) → asignar la URL del video del módulo a la primera lección de cada módulo (l1-1, l2-1, l3-1, etc.) y dejar las demás sin video — o repetir el mismo embed en las cuatro lecciones si quieres que aparezca en todas.

---

## Checklist global

### Antes de empezar
- [ ] Leídos los 8 guiones
- [ ] Cuenta demo de Claude.ai creada
- [ ] Assets ficticios preparados
- [ ] Identidad visual definida (paleta + tipografías + música)
- [ ] Voz seleccionada (narrador/a)

### Durante la grabación
- [ ] Tema claro consistente en Claude.ai
- [ ] Idioma de la app en español
- [ ] Sin notificaciones del sistema activas
- [ ] Resolución 1920×1080 al grabar pantalla
- [ ] Audio de voz monitorizado (auriculares cerrados)

### Después de grabar (por módulo)
- [ ] Color grading aplicado y consistente con el resto
- [ ] Subtítulos generados y revisados
- [ ] Versión web 720p exportada
- [ ] Versión vertical 9:16 (opcional, para redes)
- [ ] Datos personales difuminados si aparece alguno por accidente

### Distribución
- [ ] Subir cada video a YouTube/Vimeo (no listado o privado según política)
- [ ] Pegar URL en la lección correspondiente del HTML
- [ ] Probar que el embed funciona en distintos navegadores
- [ ] Versionar el HTML cuando se hayan añadido todos los videos

---

## Mapeo guion → lección del HTML

Cada guion cubre las 4 lecciones de su módulo en un solo video. La URL del video se pega en la lección "índice" del módulo (la primera de cada uno):

| Guion | URL se pega en lección |
|---|---|
| M1 | `l1-1` (¿Qué es Claude?) |
| M2 | `l2-1` (Cómo acceder a Claude) |
| M3 | `l3-1` (Anatomía de un buen prompt) |
| M4 | `l4-1` (Cadenas de razonamiento) |
| M5 | `l5-1` (Artifacts) |
| M6 | `l6-1` (Escritura y comunicación) |
| M7 | `l7-1` (Privacidad y datos sensibles) |
| M8 | `l8-1` (Claude Code) |

Alternativa: copiar la misma URL en las 4 lecciones del módulo para que el video aparezca en todas.

---

## Si grabar todos los videos no es viable ahora mismo

Recomendación de **prioridad por impacto** si quieres empezar con menos:

1. **M3 · El arte del prompt** — el módulo con más retorno para el alumno.
2. **M6 · Casos de uso prácticos** — el que más "convierte" porque la audiencia ve su propio trabajo.
3. **M5 · Capacidades y herramientas** — visualmente el más espectacular, gran demo.
4. **M1 · Bienvenida y fundamentos** — abre el curso, marca el tono.
5. **M2 · Primeros pasos** — útil pero algo de él envejece rápido con cada update de la UI.
6. **M4 · Técnicas avanzadas** — depende del público.
7. **M7 · Buenas prácticas** — importante pero menos "vendedor".
8. **M8 · Siguiente nivel** — cierre, se puede grabar el último.

---

## Contacto y próximos pasos

Si después de revisar los guiones quieres ajustes — duración distinta, otro tono, eliminar/añadir escenas — pídelos y los actualizo. También puedo:

- Generar capturas de pantalla reales de cada demo usando una sesión de Claude en vivo.
- Convertir uno de los guiones a un **video animado HTML/SVG** embebible directo en el HTML del curso (sin necesidad de grabar voz).
- Producir las **versiones en inglés** de los guiones si vas a localizar el curso.
- Crear los **subtítulos SRT** una vez tengas el audio grabado.
