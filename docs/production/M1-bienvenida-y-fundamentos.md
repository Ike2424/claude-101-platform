# Módulo 1 — Bienvenida y fundamentos
**Guion de producción de video · Claude 101**

---

## Ficha técnica

| Campo | Detalle |
|---|---|
| Duración objetivo | 6:30 (rango aceptable 6:00–7:30) |
| Audiencia | Mixta (no técnicos y devs en igual proporción) |
| Tono | Cercano, claro, sin tecnicismos innecesarios |
| Formato | Demo en pantalla narrada — voz en off + capturas reales de Claude.ai |
| Resolución | 1920×1080, 30fps |
| Cubre lecciones | 1.1 ¿Qué es Claude? · 1.2 La familia de modelos · 1.3 Cómo razona Claude · 1.4 Diferencias con otros asistentes |

## Objetivo de aprendizaje

Al final del video, el espectador entiende **qué es Claude, quién lo hace, qué modelos existen, cómo "piensa" y en qué se diferencia** de otros asistentes — sin asumir que es un buscador ni un oráculo.

## Equipo y assets necesarios

- Navegador Chrome/Arc en pantalla limpia (sin pestañas extra, sin extensiones visibles).
- Sesión activa en **claude.ai** con tema claro.
- Logo de Anthropic (claude.ai/favicon o página de Anthropic) para la intro.
- Captura del selector de modelos (Haiku / Sonnet / Opus).
- Música de fondo: instrumental calmado, BPM 80-100, sin letra. Sugerencia: Epidemic Sound → categoría "Calm Inspirational".
- Tipografía para callouts on-screen: **Geist** o **Inter** (coherente con el HTML del curso).

---

## Estructura del video (timecode + escenas)

### 🎬 ESCENA 1 — Hook (0:00 – 0:18)

**Acción en pantalla:**
- Pantalla negra → fade a screen recording de claude.ai en blanco con el cursor parpadeando.
- Mano (o cursor) escribe en la caja de mensaje: *"Hola Claude, ¿quién eres?"*
- ENTER. Aparece la respuesta animada token por token.

**Narración (voz en off):**
> "Antes de aprender a usarlo, conviene entender qué es. Esto es Claude — un asistente de inteligencia artificial. Pero la palabra 'asistente' se queda corta. En los próximos minutos vas a entender qué hace, cómo piensa, y por qué se parece más a un colega informado que a un buscador."

**Notas de edición:**
- Música entra suave a 0:08.
- Title card a 0:15: *"Módulo 1 · Bienvenida y fundamentos"* (Fraunces itálica, color #C8542B sobre fondo crema #F4EFE3 — paleta del curso).

---

### 🎬 ESCENA 2 — ¿Qué es Claude? (0:18 – 1:30)

**Acción en pantalla:**
- Cut a navegador en **anthropic.com**. Scroll lento por la página principal.
- Overlay con bullets aparece sobre la imagen (no narrarlos — son refuerzo visual):
  - "Anthropic · 2021"
  - "Útil · Honesto · Inofensivo"
- Cut back a claude.ai. Cursor pasa por la caja de mensaje y por los botones de adjuntar archivo / herramientas.

**Narración:**
> "Claude lo construye Anthropic, una empresa fundada en 2021 con una obsesión declarada: hacer IA que sea útil, honesta e inofensiva. No es una frase de marketing — esa tríada decide cómo responde, qué decide hacer y dónde pone el freno.
>
> ¿Y qué hace? Conversa, escribe, programa, analiza documentos, interpreta imágenes, razona problemas complejos y crea archivos. Pero lo importante no es la lista. Lo importante es esto: **funciona mejor cuando lo tratas como un colega informado, no como un buscador.**"

**Callout on-screen (1:05 – 1:18):**
> 💡 *Claude no es un buscador ni un oráculo. Es un colaborador.*

---

### 🎬 ESCENA 3 — Qué NO es Claude (1:30 – 2:15)

**Acción en pantalla:**
- Tres "tarjetas" deslizan en pantalla (estilo Apple Keynote, una a una):
  1. ❌ *No es infalible.*
  2. ❌ *No recuerda entre conversaciones por defecto.*
  3. ❌ *No actúa por iniciativa propia.*
- Mientras cada tarjeta aparece, b-roll detrás muestra Claude.ai respondiendo a una pregunta.

**Narración:**
> "Tres cosas importantes que Claude **no** es. Primero: no es infalible. Puede equivocarse, especialmente con datos muy recientes o cifras específicas. Segundo: no tiene memoria automática entre conversaciones a menos que tú la actives. Cada conversación empieza limpia. Y tercero: no actúa por iniciativa propia. Solo hace lo que le pides, en cada turno. No va a abrirte el correo ni a mandar mensajes mientras duermes."

---

### 🎬 ESCENA 4 — La familia de modelos (2:15 – 3:30)

**Acción en pantalla:**
- Cut a claude.ai. Cursor abre el **selector de modelo** (arriba en la caja de mensaje). Despliega.
- Aparecen los nombres: Haiku, Sonnet, Opus.
- Cada nombre se highlightea conforme se nombra en la narración.
- Overlay gráfico tipo "tabla" con los tres modelos y un slider visual de "velocidad vs. inteligencia":

```
          Velocidad   ←————————————→   Inteligencia
Haiku        ⬤
Sonnet               ⬤
Opus                         ⬤
```

**Narración:**
> "Claude no es uno solo. Es una familia. Tres modelos pensados para distintos equilibrios entre velocidad, coste e inteligencia.
>
> **Haiku** es el más rápido. Para tareas ligeras, respuestas instantáneas, trabajo en volumen.
>
> **Sonnet** es el equilibrio. Razonamiento sólido con tiempos razonables. Es el que vas a usar el 80% del tiempo.
>
> **Opus** es el más potente. Para problemas complejos, análisis profundo, escritura matizada.
>
> **Regla práctica:** empieza con Sonnet. Sube a Opus si necesitas pensar a fondo en algo difícil. Baja a Haiku si quieres velocidad para algo sencillo."

**Callout on-screen (3:15 – 3:28):**
> 📌 *Los modelos se actualizan. Revisa docs.claude.com para la versión más reciente.*

---

### 🎬 ESCENA 5 — Cómo razona Claude (3:30 – 4:50)

**Acción en pantalla:**
- Split screen:
  - Izquierda: animación de "puntos de probabilidad" siguiendo una frase ("El gato está sobre la ___" → mesa / silla / alfombra cayendo como sugerencias con porcentajes).
  - Derecha: claude.ai mostrando una respuesta real.
- Después, cut a una conversación nueva en Claude. Pegar este prompt y mostrar la respuesta:

**Prompt demo a usar (copiar tal cual al grabar):**
```
Tengo una conversación de 250 mensajes con un cliente difícil. ¿Cómo decides qué información del principio sigue siendo relevante cuando te pido un resumen al final?
```

**Narración:**
> "Hay un detalle importante sobre cómo Claude funciona. **No consulta una base de datos cuando responde.** Genera la respuesta más probable basándose en patrones que aprendió en el entrenamiento. Esto tiene dos consecuencias prácticas.
>
> Una: puede sonar muy seguro incluso cuando se equivoca. A eso se le llama *alucinación.*
>
> Dos: funciona mucho mejor cuanto más claro y específico es el contexto que le das. Por eso el siguiente módulo se llama 'El arte del prompt' — porque no es metáfora.
>
> Y una característica clave: los modelos modernos pueden **pensar antes de responder**. Dedican tiempo a razonar paso a paso en problemas complejos — matemáticas, lógica, código. Esto se nota."

**Visual de apoyo (4:30 – 4:50):**
- Mostrar la animación "Claude está pensando..." sobre la respuesta en tiempo real (si el modelo Opus está activo, esto se ve bien en pantalla).

---

### 🎬 ESCENA 6 — Ventana de contexto (4:50 – 5:25)

**Acción en pantalla:**
- Gráfico: una "ventana" rectangular que se va llenando con páginas mientras una flecha indica "Lo que Claude puede tener en la cabeza ahora mismo".
- Texto sobre el gráfico: *"Cientos de páginas... pero no infinitas."*

**Narración:**
> "Claude tiene una **ventana de contexto** — la cantidad de texto que puede tener 'en la cabeza' en una conversación. Es muy amplia, cientos de páginas, pero no infinita. En conversaciones muy largas o documentos enormes, puede empezar a olvidar el principio. Cuando notes que se está despistando, la solución suele ser abrir una conversación nueva con el contexto justo."

---

### 🎬 ESCENA 7 — Diferencias con otros asistentes (5:25 – 6:10)

**Acción en pantalla:**
- Cuatro tarjetas que aparecen en secuencia:
  1. ✍️ **Estilo de escritura** — texto natural, no formulaico.
  2. 🎯 **Honestidad calibrada** — reconoce sus límites.
  3. ⚖️ **Razonamiento ético matizado** — no bloquea de forma rígida.
  4. 📚 **Contextos largos** — coherencia con documentos extensos.

**Narración:**
> "Comparte muchas capacidades con ChatGPT, Gemini y otros. Pero hay cuatro cosas en las que Claude se distingue.
>
> Primero: el estilo de escritura. Tiende a producir texto más natural, menos formulaico, mejor estructurado para que un humano lo lea.
>
> Segundo: honestidad calibrada. Reconoce sus límites en lugar de afirmar con falsa seguridad.
>
> Tercero: razonamiento ético matizado. Aborda temas sensibles con criterio en lugar de bloquearlos en seco.
>
> Y cuarto: manejo de contextos largos. Sobresale en documentos extensos manteniendo coherencia.
>
> ¿Es 'el mejor'? Depende. La forma honesta de saberlo es probar el mismo prompt en varios asistentes y comparar. Lo que sí tiene Claude es **personalidad propia**: directa, reflexiva, con punto editorial."

---

### 🎬 ESCENA 8 — Cierre y puente al Módulo 2 (6:10 – 6:30)

**Acción en pantalla:**
- Fade a una pantalla con el siguiente mensaje:

```
En el próximo módulo:
Cómo acceder a Claude, anatomía
de la interfaz, proyectos y estilos.
```

- Logo del curso abajo. Música sube ligeramente.

**Narración:**
> "Eso es Claude en una imagen mental: un colaborador que predice texto, que tiene varias versiones según lo que necesites, y que funciona mejor cuanto mejor le hablas. En el próximo módulo vamos a abrir la app y entender qué hay dentro. Nos vemos ahí."

---

## Prompts de demo (listos para copiar en Claude durante la grabación)

**Demo 1 — Para la escena 1 (hook):**
```
Hola Claude, ¿quién eres?
```

**Demo 2 — Para la escena 5 (razonamiento):**
```
Tengo una conversación de 250 mensajes con un cliente difícil. ¿Cómo decides qué información del principio sigue siendo relevante cuando te pido un resumen al final?
```

**Demo 3 — B-roll opcional (para mostrar capacidades en escena 2):**
```
Resume este artículo en 3 viñetas para un equipo no técnico: [pegar cualquier artículo de prueba aquí]
```

---

## Checklist de pre-producción

- [ ] Tema claro en claude.ai
- [ ] Selector de modelo visible (no oculto en menú)
- [ ] Sesión limpia, sin proyectos antiguos a la vista en el sidebar
- [ ] Resolución 1920×1080 al grabar
- [ ] Audio: dB de narración a -16 LUFS aprox.
- [ ] Música a -24 LUFS (10dB por debajo de la voz)
- [ ] Mostrar el subtítulo en español por defecto
- [ ] Logo de Anthropic disponible en alta resolución
- [ ] Tipografía Fraunces y Geist instaladas para overlays

## Checklist de post-producción

- [ ] Color grading coherente con la paleta del HTML (#F4EFE3 / #C8542B / #4F5D38)
- [ ] Subtítulos quemados o en pista separada
- [ ] Versión 16:9 master
- [ ] Versión 9:16 (cortes de 60s para redes) — opcional
- [ ] Exportar como MP4 H.264 + WebM para web
- [ ] Subir a YouTube/Vimeo en modo "no listado"
- [ ] Copiar URL → pegarla en Claude 101 HTML (modo instructor → "Añadir vídeo" en lección 1.1)
