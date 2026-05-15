# Módulo 2 — Primeros pasos
**Guion de producción de video · Claude 101**

---

## Ficha técnica

| Campo | Detalle |
|---|---|
| Duración objetivo | 7:00 (rango 6:30–8:00) |
| Audiencia | Mixta — pero más útil para no técnicos en este módulo |
| Tono | Práctico, "ven y mira" |
| Formato | Tour de producto en vivo + capturas de la app móvil y desktop |
| Cubre lecciones | 2.1 Cómo acceder · 2.2 Anatomía de la interfaz · 2.3 Conversaciones, proyectos y estilos · 2.4 Configuración esencial |

## Objetivo

Que el espectador termine con Claude **instalado, configurado y listo para usar** — sabiendo qué plan elegir, dónde está cada cosa en la interfaz, y qué ajustes activar de entrada.

## Equipo y assets

- Mac/PC con navegador en pantalla principal.
- iPhone o Android disponible para grabar la app móvil (overlay de la pantalla del móvil sobre el video).
- Sesión limpia de claude.ai (puede ser una cuenta de demo nueva para evitar mostrar conversaciones reales).
- 1 documento PDF de prueba para subirlo a un proyecto durante la demo (algo neutro: una hoja de ruta, un manual corto).

---

## Estructura del video

### 🎬 ESCENA 1 — Hook (0:00 – 0:20)

**Pantalla:**
- Time-lapse rápido: claude.ai abriéndose, app móvil arrancando, app de escritorio cargando, terminal con un comando ejecutándose. Cuatro pantallas en mosaico, 3 segundos cada una.

**Narración:**
> "Cuatro maneras distintas de abrir Claude. Cuatro experiencias diferentes. En los próximos siete minutos vamos a entrar a la app, entender qué hay dentro, montar tu primer proyecto, y dejar la configuración bien hecha — para que no te tengas que preocupar después."

**Title card (0:15):** *"Módulo 2 · Primeros pasos"*

---

### 🎬 ESCENA 2 — Las cuatro puertas de entrada (0:20 – 1:40)

**Pantalla:**
- Tour visual de las cuatro vías. Una tras otra:
  1. **claude.ai** en Chrome (mostrar URL en barra).
  2. **App móvil** (grabación picture-in-picture del iPhone abriendo Claude).
  3. **App de escritorio** (icono en Dock, abrirla).
  4. **Terminal** con `claude --version` y luego `claude` arrancando — solo unos segundos.

**Narración:**
> "Empecemos por lo más básico: ¿cómo entras?
>
> Hay cuatro puertas. La primera, **claude.ai** — la web pública. Abres el navegador, inicias sesión, y a chatear.
>
> Segunda, la **app móvil** — iOS y Android. Misma experiencia, optimizada para pantalla pequeña. Útil cuando estás en el metro y quieres aprovechar.
>
> Tercera, la **app de escritorio**. Para Mac y Windows. Si vas a usar Claude todos los días, esta es la mejor — tiene atajos de teclado, acceso rápido, e integraciones con tu sistema.
>
> Y cuarta, para desarrolladores: la **API y Claude Code** — para integrar Claude en tus propios productos o trabajar desde el terminal. De esto hablaremos en el módulo 8."

---

### 🎬 ESCENA 3 — Planes y cuál elegir (1:40 – 2:25)

**Pantalla:**
- Cut a la página de planes de claude.ai (`/upgrade`). Mostrar las tarjetas: Free, Pro, Team, Enterprise.
- Mover el cursor lentamente sobre cada una. Detenerse en Pro.

**Narración:**
> "Cuatro planes: gratuito, Pro, Team y Enterprise. El gratuito tiene límites de uso pero te deja probar todo. Pro es el que tiene sentido si lo vas a usar a diario — desbloquea más capacidad, acceso prioritario a los modelos más potentes, y funciones extra.
>
> **Consejo de quien lo usa todos los días:** si vas a tocar Claude más de tres veces al día, Pro se paga solo. Si lo usas puntualmente, el gratuito alcanza."

**Callout (2:10 – 2:22):**
> 💳 *Plan Pro · Pensado para uso diario intenso*

---

### 🎬 ESCENA 4 — Anatomía de la interfaz (2:25 – 4:00)

**Pantalla:**
- Cut a claude.ai limpio. Cursor inicia un tour numerado. Cada elemento se "señaliza" con un círculo animado y un overlay:

```
1️⃣ Caja de mensaje
2️⃣ Selector de modelo
3️⃣ Historial
4️⃣ Proyectos
5️⃣ Configuración
```

**Narración:**
> "Vamos a abrir Claude y nombrar cada cosa. Cinco elementos que vas a usar todos los días.
>
> **Uno: la caja de mensaje.** Donde escribes. Pero atención — no solo texto. Puedes adjuntar imágenes, PDFs, hojas de cálculo, código. Mira."

**Acción en pantalla (2:55):**
- Click en el icono de adjuntar. Subir un PDF de prueba. Mostrar la miniatura adjunta. Escribir: *"Resúmemelo en 3 viñetas."* Enviar. Se ve la respuesta.

**Narración (continuación):**
> "**Dos: el selector de modelo.** Arriba — eliges entre Sonnet, Opus, Haiku según la tarea. Lo cubrimos en el módulo 1.
>
> **Tres: el historial.** En el sidebar izquierdo. Todas tus conversaciones, ordenadas por fecha.
>
> **Cuatro: los proyectos.** También en el sidebar. Esto es importante y lo vemos en un segundo.
>
> **Cinco: la configuración.** Tu avatar, abajo a la izquierda. Ahí está todo lo que vamos a tunear al final del video.
>
> Y un extra: dentro de la caja de mensaje hay **funciones contextuales** — búsqueda web, modo de investigación profunda, generación de archivos. Cada función cambia cómo se comporta Claude. Iremos viendo cuál se usa cuándo."

---

### 🎬 ESCENA 5 — Conversaciones, proyectos y estilos (4:00 – 5:30)

**Pantalla:**
- Demostración en vivo:
  1. Crear una conversación nueva. Escribir algo. *"De qué hablábamos en este mensaje hace un rato"* → Claude recuerda dentro del hilo.
  2. Click en "Proyectos" → "Nuevo proyecto" → nombrarlo *"Cliente Demo S.A."*
  3. Subir un PDF de referencia al proyecto (el mismo o uno nuevo). Mostrar que queda fijado.
  4. Crear conversación dentro del proyecto. Hacer una pregunta sobre el documento sin re-adjuntarlo.
  5. Click en "Estilos" → mostrar el menú → elegir uno por defecto.

**Narración:**
> "Tres conceptos que se confunden todo el rato, pero que cambian tu productividad cuando los entiendes.
>
> **La conversación** es la unidad básica. Un hilo donde Claude recuerda todo lo dicho. Si cambias de tema, abre uno nuevo. **No mezcles tareas distintas en el mismo hilo** — la memoria se ensucia y empieza a confundirse.
>
> **El proyecto** es una carpeta con contexto propio. Subes documentos de referencia — un libro de marca, un código fuente, una guía de estilo — y todas las conversaciones del proyecto los tienen disponibles. Mira esto."

**Pause-frame en pantalla (4:45):** Mostrar la sidebar con el documento adjunto al proyecto.

**Narración (continuación):**
> "Acabo de subir un PDF al proyecto. Ahora cualquier conversación nueva dentro de este proyecto puede consultarlo sin que yo lo re-adjunte. Útil para trabajos largos con un cliente, un libro que estás escribiendo, un producto sobre el que trabajas semana tras semana.
>
> **Truco:** crea un proyecto por cliente o por tema recurrente. Subes los documentos clave una sola vez y te olvidas de pegar contexto en cada conversación.
>
> Y los **estilos** — esto cambia el tono con el que Claude te responde. Formal, directo, divertido, con o sin emojis. Puedes crear el tuyo a partir de un texto de ejemplo."

---

### 🎬 ESCENA 6 — Configuración esencial (5:30 – 6:40)

**Pantalla:**
- Click en avatar → "Settings". Tour por las tres secciones:
  1. **Personalization / Preferences** — escribir un par de líneas: *"Soy responsable de marketing en una startup B2B. Prefiero respuestas concisas, en español, sin listas largas a menos que las pida."*
  2. **Privacy** — mostrar el toggle de "use for training". Por defecto está apagado en planes consumer. Mostrar opciones de retención.
  3. **Features** — toggles de búsqueda web, memoria, creación de archivos, conectores.

**Narración:**
> "Tres ajustes que conviene hacer antes de ponerse a trabajar en serio.
>
> Primero, **preferencias de usuario**. Aquí guardas información persistente sobre ti: cómo te llamas, a qué te dedicas, cómo prefieres que te respondan. Lo que escribas aquí Claude lo tendrá en cuenta en todas tus conversaciones. Yo te recomiendo dedicarle dos minutos — tu Claude va a sonar mejor inmediatamente.
>
> Segundo, **privacidad y datos**. En los planes consumer de Anthropic, por defecto, tus conversaciones no se usan para entrenar futuros modelos. Pero revisa los ajustes de retención del historial. Y si trabajas con datos delicados, mira con atención qué política aplica a tu plan.
>
> Tercero, **funciones que se activan o desactivan**. Búsqueda web. Memoria. Creación de archivos. Conectores con apps externas como Drive o Slack. Mi consejo: empieza con lo básico, activa el resto a medida que lo necesites. Activar todo desde el día uno es ruido."

---

### 🎬 ESCENA 7 — Cierre y puente al Módulo 3 (6:40 – 7:00)

**Pantalla:**
- Fade a una pantalla que muestra: una conversación, un proyecto, y un estilo personalizado abiertos uno tras otro como cards.

**Narración:**
> "Tienes Claude abierto, sabes dónde está cada cosa, tienes un proyecto con tu contexto, y la configuración hecha. Lo que falta es lo más importante: cómo hablarle. En el próximo módulo entramos al arte del prompt — la habilidad que multiplica todo lo demás. Te veo ahí."

---

## Prompts de demo (copiables)

**Demo 1 — Para escena 4 (caja de mensaje + adjuntar):**
```
Resume el documento adjunto en 3 viñetas. Audiencia: equipo no técnico.
```

**Demo 2 — Para escena 5 (proyecto con contexto):**
```
Según el documento que tenemos en este proyecto, ¿cuáles son las tres decisiones más importantes que toma?
```

**Demo 3 — Para escena 6 (preferencias):**
```
Soy responsable de marketing en una startup B2B. Trabajo en español. Prefiero respuestas concisas, sin listas largas a menos que las pida. Cuando me ayudes con texto, escribe en frases cortas y directas.
```
(Esto NO se manda en la conversación — se pega en el campo *Personal Preferences* de los ajustes.)

---

## Checklist de pre-producción

- [ ] Cuenta demo con planes visibles (no mostrar planes pagados de la cuenta personal)
- [ ] PDF de prueba listo (no contenga datos sensibles reales)
- [ ] iPhone/Android cargado para overlay móvil
- [ ] Limpiar el historial de conversaciones de la cuenta demo (no debe verse contenido real)
- [ ] Tema claro en la app
- [ ] Idioma de la app: español (revisar antes de grabar)

## Checklist de post-producción

- [ ] Difuminar/borrar cualquier dato personal en pantalla (email, nombre real)
- [ ] Overlays con números 1-5 en escena 4
- [ ] Picture-in-picture para la grabación del móvil en escena 2
- [ ] Color grading consistente con M1
- [ ] Exportar y subir → pegar URL en lección 2.1 del HTML
