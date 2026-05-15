# Módulo 3 — El arte del prompt
**Guion de producción de video · Claude 101**

---

## Ficha técnica

| Campo | Detalle |
|---|---|
| Duración objetivo | 7:30 (rango 7:00–8:00) |
| Audiencia | Mixta — esta es la lección que MÁS impacto tiene para todos |
| Tono | Didáctico, casi de taller. Ritmo medio, sin prisa |
| Formato | Demo lado a lado: prompt débil vs. prompt sólido en pantalla partida |
| Cubre lecciones | 3.1 Anatomía · 3.2 Contexto, claridad, especificidad · 3.3 Antes y después · 3.4 Errores comunes |

## Objetivo

Que el espectador entienda **las 4 partes de un prompt** (tarea, contexto, formato, restricciones) y vea con sus propios ojos la diferencia de calidad entre un prompt débil y uno sólido — replicada en su propio trabajo.

## Equipo y assets

- claude.ai con dos ventanas o dos pestañas abiertas para hacer comparación lado a lado.
- Un proyecto demo con un cliente ficticio ("María González — proyecto Q3").
- Plantillas de subtítulos para etiquetar prompts: **TAREA · CONTEXTO · FORMATO · RESTRICCIONES** con colores distintos (sugerencia: naranja #C8542B / oliva #4F5D38 / dorado #B08436 / gris #756B5B).

---

## Estructura del video

### 🎬 ESCENA 1 — Hook (0:00 – 0:25)

**Pantalla:**
- Split screen 50/50.
- Lado izquierdo: prompt *"Escríbeme un email a un cliente."* → respuesta genérica y mediocre de Claude.
- Lado derecho: prompt detallado (el que sale en el curso) → respuesta excelente, con tono cálido y específico.
- Pausar ambos resultados en pantalla. Texto overlay: *"Mismo modelo. Misma persona. Resultado completamente distinto."*

**Narración:**
> "Misma versión de Claude. Misma persona escribiendo. Pero los resultados son irreconocibles. La diferencia no está en el modelo. Está en cómo le hablas. En los próximos siete minutos, aprendes a escribir prompts que te dan resultados que valen la pena."

**Title card (0:20):** *"Módulo 3 · El arte del prompt"*

---

### 🎬 ESCENA 2 — Las cuatro partes de un prompt (0:25 – 2:00)

**Pantalla:**
- Pantalla en blanco. Aparecen una por una las cuatro etiquetas, cada una con un color:
  - 🟠 **TAREA** — *"qué quieres que haga"*
  - 🟢 **CONTEXTO** — *"información de fondo"*
  - 🟡 **FORMATO** — *"cómo lo quieres recibir"*
  - ⚪ **RESTRICCIONES** — *"qué evitar / qué NO hacer"*
- Después, una versión "anatómica" del prompt sólido del curso, con cada parte coloreada según su tipo. Lo construimos en pantalla, frase por frase.

**Narración:**
> "Un buen prompt tiene cuatro partes. Y cuando las cuatro están claras, Claude no tiene espacio para malinterpretarte.
>
> **Uno: la tarea.** Qué quieres que haga, expresado con un verbo claro. Escribe, analiza, traduce, propón. Sin ambigüedad.
>
> **Dos: el contexto.** La información de fondo que Claude necesita. ¿Quién es el cliente? ¿Qué relación tienes con él? ¿Qué pasó antes?
>
> **Tres: el formato.** Cómo quieres recibir la respuesta. Longitud, estructura, tono.
>
> **Cuatro: las restricciones.** Lo que NO quieres, los límites, las cosas a evitar.
>
> Si una de las cuatro falta, los resultados se deterioran. Y aquí viene la parte interesante: no se trata de escribir prompts más largos. Se trata de escribirlos más **específicos**."

---

### 🎬 ESCENA 3 — Antes y después (en vivo) (2:00 – 3:30)

**Pantalla:**
- Cut a claude.ai.
- Escribir el prompt débil:

```
Escríbeme un email a un cliente.
```

- Enviar. Mostrar la respuesta genérica que sale. Highlights amarillos en pantalla sobre las partes vagas: *"Estimado cliente"*, *"En relación a nuestro proyecto"*, *"Quedo a su disposición"* — clichés.

- Cut a una nueva conversación. Escribir el prompt sólido. Lo escribimos delante de la cámara, con texto on-screen marcando cada parte conforme se teclea:

```
Escribe un email para María (cliente, lleva 3 años con nosotros)
anunciándole que el proyecto se retrasa 2 semanas por causa ajena
a nosotros (un proveedor falló). Tono cálido pero profesional.
Máximo 6 frases. No te excuses en exceso. Termina ofreciendo
una llamada esta semana.
```

- Enviar. Mostrar la respuesta. Highlights verdes sobre las partes específicas: nombre de la persona, tono que se nota, cierre con propuesta de llamada.

**Narración (mientras escribes):**
> "Mira la diferencia. El primer prompt — 'escríbeme un email a un cliente' — produce esto. Cliché. Genérico. Sin tono. Inservible.
>
> Ahora mira lo que pasa cuando aplicamos las cuatro partes. **Tarea:** escribir un email. **Contexto:** María, cliente de tres años, proyecto retrasado, culpa de un proveedor. **Formato:** máximo seis frases, tono cálido pero profesional. **Restricciones:** no excusarse en exceso, terminar ofreciendo una llamada.
>
> Mira el resultado ahora. Personalizado. Profesional sin ser frío. Con una acción concreta al final. Y la diferencia no es magia — es claridad."

---

### 🎬 ESCENA 4 — Las tres palancas que más mejoran (3:30 – 5:00)

**Pantalla:**
- Tres tarjetas grandes en sucesión: **CONTEXTO** / **CLARIDAD** / **ESPECIFICIDAD**.
- Bajo cada tarjeta, un mini ejemplo en vivo. Mostrar también el equivalente "vago" tachado.

**Narración:**
> "Hay tres palancas que más mejoran cualquier prompt. Vamos una a una.
>
> **Contexto:** Claude no conoce tu negocio, tu equipo, tu tono. Dáselos. Pero — y esto es importante — no es 'cuanta más información, mejor'. Es **la información relevante**. Mejor cinco datos útiles que cincuenta irrelevantes.
>
> **Claridad:** una idea por frase. Frases largas con cinco subordinadas confunden tanto a humanos como a máquinas. Divide. Usa listas si tienes varios requisitos. Lo que cuesta entender a un humano, también le cuesta a Claude."

**Pantalla (4:15):** Mostrar tabla en dos columnas:

| Vago | Específico |
|---|---|
| "Corto" | "Máximo 100 palabras" |
| "Profesional" | "Como hablaría un consultor a un CFO" |
| "Creativo" | "Usa al menos una metáfora visual inesperada" |

**Narración (continuación):**
> "**Especificidad:** las palabras vagas son trampas. 'Corto', 'profesional', 'creativo', 'interesante' — significan cosas distintas para distintas personas. Sé concreto. 'Corto' es 'máximo 100 palabras'. 'Profesional' es 'como hablaría un consultor a un director financiero'. 'Creativo' es 'usa al menos una metáfora visual inesperada'. Cuanto más concreto, mejor el resultado."

---

### 🎬 ESCENA 5 — Caso real: resumen de reunión (5:00 – 6:00)

**Pantalla:**
- Pegar una transcripción de reunión (puede ser ficticia, 1 página) en una conversación nueva.
- Primer intento: *"Resume esta reunión."* → respuesta genérica, sin estructura.
- Segundo intento (mismo input):

```
Resume esta transcripción de reunión en tres bloques:
1) Decisiones tomadas (con responsable)
2) Próximos pasos (con fecha)
3) Temas pendientes para la próxima reunión.
Usa viñetas. No más de 250 palabras en total.
```

- Mostrar el contraste de la respuesta.

**Narración:**
> "Caso real, uno que vas a usar tarde o temprano: resumir una reunión. Mira el resumen que genera un prompt vago. Versus el que genera un prompt específico con bloques claros, responsables, fechas y un límite de palabras. La transcripción es la misma. La diferencia es cómo le pedí el trabajo."

---

### 🎬 ESCENA 6 — Top 5 de errores (6:00 – 7:00)

**Pantalla:**
- Cuenta atrás de 5 a 1, cada error con un icono y un ejemplo de mal prompt tachado:

```
5. Asumir conocimiento.
4. No iterar.
3. Mezclar tareas.
2. Falta de contexto.
1. Prompts ambiguos.
```

**Narración:**
> "Cinco errores que vas a cometer si no estás atento — todos los he visto, todos los he cometido.
>
> **Cinco: asumir conocimiento.** Dar por hecho que Claude conoce tu empresa, tu cliente, el proyecto del que vienes. No te conoce. Cuéntale.
>
> **Cuatro: no iterar.** Conformarse con la primera respuesta. Casi siempre mejora con uno o dos ajustes. La primera versión es un punto de partida, no la final.
>
> **Tres: mezclar tareas.** 'Tradúceme esto, resume aquello y de paso escríbeme otro texto.' Hazlo en mensajes separados. Cada uno con su propio foco.
>
> **Dos: falta de contexto.** Pedir un email sin decir a quién va, ni qué relación tienes con esa persona, ni por qué le escribes.
>
> **Y uno, el más común: prompts ambiguos.** 'Hazlo mejor' sin decir qué significa 'mejor' para ti. **Si una persona inteligente sin contexto pudiera hacer la tarea con tu prompt, Claude también podrá. Si no, falta información.** Esa es la regla de oro."

---

### 🎬 ESCENA 7 — Cierre y puente al Módulo 4 (7:00 – 7:30)

**Pantalla:**
- Fade a un resumen final de las 4 partes con colores. Después aparece el texto: *"En el próximo módulo: técnicas avanzadas que multiplican esto."*

**Narración:**
> "Cuatro partes — tarea, contexto, formato, restricciones — y tres palancas: contexto, claridad, especificidad. Ya tienes el 80% de lo que necesitas para escribir prompts decentes. En el próximo módulo añadimos el 20% que separa los buenos prompts de los excelentes: cadenas de razonamiento, ejemplos, etiquetas. Nos vemos."

---

## Prompts de demo (copiables)

**Demo 1 — Prompt débil para escena 3:**
```
Escríbeme un email a un cliente.
```

**Demo 2 — Prompt sólido para escena 3:**
```
Escribe un email para María (cliente, lleva 3 años con nosotros) anunciándole que el proyecto se retrasa 2 semanas por causa ajena a nosotros (un proveedor falló). Tono cálido pero profesional. Máximo 6 frases. No te excuses en exceso. Termina ofreciendo una llamada esta semana.
```

**Demo 3 — Transcripción ficticia para escena 5 (preparar antes):**

```
Acta resumida — Reunión semanal de producto, 14 may 2026.

Asistentes: Laura (PM), Diego (Eng lead), Sofía (Diseño), Iván (Marketing).

- Laura propone retrasar la feature de notificaciones push a junio porque el equipo de backend tiene capacidad limitada hasta entonces. Diego confirma. Aprobado.
- Sofía presenta tres opciones del rediseño del onboarding. Se elige la opción B. Sofía entregará las pantallas finales el viernes 16.
- Iván pregunta si podemos lanzar la campaña con la versión actual del onboarding. Acuerdo: lanzar el 20 con la versión nueva.
- Tema sin resolver: precios para el plan Enterprise. Pendiente para la próxima reunión. Iván traerá un análisis comparativo.
- Iván se va de vacaciones del 25 al 1 de junio.
```

**Demo 4 — Prompt débil para escena 5:**
```
Resume esta reunión.
```

**Demo 5 — Prompt sólido para escena 5:**
```
Resume esta transcripción de reunión en tres bloques:
1) Decisiones tomadas (con responsable)
2) Próximos pasos (con fecha)
3) Temas pendientes para la próxima reunión.
Usa viñetas. No más de 250 palabras en total.
```

---

## Checklist de pre-producción

- [ ] Pestañas duplicadas listas para split screen
- [ ] Tres etiquetas de color definidas y consistentes
- [ ] Transcripción ficticia preparada (no usar reunión real bajo ningún concepto)
- [ ] Conversación demo nueva (sin historia previa) para evitar sesgo de memoria

## Checklist de post-producción

- [ ] Resaltar con highlights amarillos las partes "vagas" y verdes las "específicas"
- [ ] Animar las cuatro tarjetas TAREA/CONTEXTO/FORMATO/RESTRICCIONES
- [ ] Subtítulos siempre activos — este módulo se mira más en silencio (oficina)
- [ ] Versión vertical 9:16 RECOMENDADA aquí: este módulo funciona muy bien en redes sociales
