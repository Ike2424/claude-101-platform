# Módulo 6 — Casos de uso prácticos
**Guion de producción de video · Claude 101**

---

## Ficha técnica

| Campo | Detalle |
|---|---|
| Duración objetivo | 7:30 (rango 7:00–8:00) |
| Audiencia | Mixta — este módulo es donde la audiencia "se convierte" porque ve su propio trabajo |
| Tono | Concreto, casi vendedor. Mostrar resultados que ahorran tiempo real |
| Formato | 4 escenarios reales — uno por lección. Demos rápidas, ritmo alto |
| Cubre lecciones | 6.1 Escritura · 6.2 Programación · 6.3 Análisis de datos · 6.4 Creatividad |

## Objetivo

Que el espectador termine el video pensando *"esto lo puedo aplicar mañana en mi trabajo"* — viendo 4 flujos concretos resueltos en directo.

## Equipo y assets

- 1 PDF de informe técnico de ejemplo (5-10 páginas).
- 1 hoja Excel con datos reales-pero-anónimos (ventas mensuales o similar).
- 1 imagen con un gráfico (cualquier dashboard captured de internet).
- 1 fragmento de código JavaScript con un bug evidente para la demo de programación.
- Acceso a un editor de código visible (VS Code, Cursor) para la escena de devs.

---

## Estructura del video

### 🎬 ESCENA 1 — Hook (0:00 – 0:25)

**Pantalla:**
- Montaje rápido de 4 frames con texto sobre cada uno:
  - 📧 "Redactar un email cargado de mala uva — 8 min → 90s"
  - 💻 "Encontrar el bug en 30 líneas — 25 min → 2 min"
  - 📊 "Analizar una hoja de Excel de 12 hojas — 45 min → 5 min"
  - 🎨 "Bloqueo creativo — 1h → 10 min"

**Narración:**
> "Cuatro tareas reales. Cuatro categorías de trabajo. Y un patrón: lo que antes tardaba horas, con Claude tarda minutos — si sabes cómo pedirlo. Vamos a ver los cuatro casos de uso que más valor te van a dar de aquí en adelante."

**Title card:** *"Módulo 6 · Casos de uso prácticos"*

---

### 🎬 ESCENA 2 — Escritura y comunicación (0:25 – 2:25)

**Pantalla:**
- Setup: un email mal escrito a propósito. Ejemplo: respuesta a un cliente que pide algo difícil de entregar a tiempo. El borrador está cargado de irritación contenida.

**Borrador inicial (mostrar en pantalla):**
```
Hola Pedro,
Vale, lo que me pides es complicado porque no tengo
gente disponible y además llevamos semanas con esto
sin que tomes decisiones. Te lo intento sacar para
el viernes pero si no llega ya sabes por qué.
Un saludo,
```

- Subir a Claude (copiar y pegar el borrador en el chat) con este prompt:

```
Este es el borrador de un email que quiero mandar a un cliente
con el que estoy frustrado pero al que necesito mantener contento.
Reescríbelo: tono profesional y cálido, sin dejar de pedir
claridad para tomar decisiones. Máximo 5 frases. Termina
ofreciendo una llamada esta semana para desbloquear.
```

- Mostrar la respuesta — un email impecable.

**Narración:**
> "Empezamos por lo que más vas a usar: **escritura y comunicación**. Y el flujo correcto no es 'escríbeme un email desde cero'. Es este, en cuatro pasos:
>
> Uno: **tú haces un borrador rápido** — mal, sin pulir, con la idea esencial. Es lo que tú sabes y Claude no: la intención.
>
> Dos: **se lo das a Claude** con un encargo claro. 'Reescribe esto. Más conciso. Más cálido. Tono ejecutivo.' Lo que quieras.
>
> Tres: **iteras**. Una frase aquí, un párrafo allá.
>
> Cuatro: **el toque humano final**. Tú lo repasas, añades tus particularidades, envías.
>
> Este flujo vale para emails, informes, copy, posts de LinkedIn, mensajes delicados. Te ahorra el bloqueo de la página en blanco sin perder tu voz. Mira el ejemplo."

**Pause-frame en la respuesta de Claude (1:50 – 2:05):**
- Highlights verdes sobre las partes "humanas" — la oferta de llamada, el reconocimiento del trabajo de Pedro.

**Narración (continuación):**
> "Mismo mensaje. Mismo objetivo. Profesional sin ser frío. Y mantiene la pregunta crítica — pedir decisiones claras — sin sonar pasivo-agresivo. Eso es el flujo borrador-reescritura-iteración."

---

### 🎬 ESCENA 3 — Programación y análisis técnico (2:25 – 4:00)

**Pantalla:**
- Cut a VS Code (o Cursor). Mostrar un fragmento de JavaScript de 30 líneas con un bug evidente (ej: un `for` que no incrementa, o un `null` no manejado).
- Copiar el código + el mensaje de error.
- Pegar en Claude con este prompt:

```
Este código JavaScript me lanza este error en producción:
TypeError: Cannot read properties of null (reading 'name')

¿Qué está pasando y cómo lo arreglo? Explícame en una frase
y luego dame el fix con el código completo corregido.
```

- Mostrar la respuesta de Claude: diagnóstico breve + código corregido con cambios resaltados.

**Después**, segunda demo rápida — explicar código ajeno:

```
Tengo este pedazo de código que heredé de un compañero
que ya no está. ¿Puedes explicarme línea por línea qué
hace y si hay algo que mejorarías?

[pegar otro fragmento]
```

**Narración:**
> "**Programación y análisis técnico.** Si escribes código, Claude se convierte en tu colega senior de turno. Te enseño tres flujos en los que destaca.
>
> **Uno: depurar.** Le das el código y el mensaje de error. Te diagnostica en una frase y te da el fix. Mira."

**Pause para mostrar la respuesta (3:00 – 3:15):**

**Narración (continuación):**
> "**Dos: explicar código ajeno.** ¿Cuántas veces has heredado código de alguien que ya no está y has tardado dos horas en entenderlo? Pásalo a Claude. Línea por línea si hace falta.
>
> **Tres: convertir entre lenguajes.** Python a JavaScript. SQL a Pandas. Útil cuando estás migrando un sistema o aprendiendo un lenguaje nuevo.
>
> Y para devs que viven en el terminal: existe **Claude Code** — la herramienta de línea de comandos que permite a Claude trabajar directamente en tu base de código. Lee archivos, hace cambios, ejecuta comandos. Lo cubrimos en el módulo 8."

---

### 🎬 ESCENA 4 — Análisis de datos y documentos (4:00 – 5:45)

**Pantalla:**
- Subir el PDF de informe (5-10 páginas) a una conversación nueva.

```
Adjunto un informe de mercado. Hazme tres cosas:
1) Identifica las cinco conclusiones clave.
2) Cita los datos más fuertes (con la página donde aparecen).
3) Dime qué información falta o está poco respaldada.
```

- Mostrar la respuesta.

**Después**, subir el Excel con ventas y hacer:

```
Adjunto las ventas mensuales del último año. Hazme:
- Un resumen de tendencias (crecimiento, estacionalidad, anomalías).
- Las tres líneas de producto más rentables.
- Una recomendación de acción para el próximo trimestre.
Muéstrame los cálculos para que pueda verificarlos.
```

- Mostrar la respuesta con tablas y razonamiento.

**Después**, subir la imagen del dashboard / gráfico:

```
¿Qué te dice esta gráfica? ¿Qué patrones ves?
¿Qué pregunta de seguimiento harías?
```

**Narración:**
> "**Análisis de datos y documentos.** Cualquier cosa que se pueda subir, Claude la lee. PDFs, Excel, imágenes, txt. Y no es solo lectura — es análisis.
>
> Tres flujos que vas a usar.
>
> **Uno: PDFs largos.** Le subes un informe de 80 páginas y le pides las conclusiones, los datos más fuertes, lo que falta. Te ahorras una mañana de lectura.
>
> **Dos: Excel.** Le subes una hoja con ventas y le pides análisis — tendencias, anomalías, recomendaciones. Y el truco aquí: **pídele que muestre los cálculos**. En datos numéricos puede equivocarse, y verificarlo es trivial si los cálculos están delante.
>
> **Tres: imágenes y gráficos.** Adjunta una captura de pantalla de un dashboard y pregúntale qué le dice. Identifica patrones que a ti se te pasan."

**Callout (5:30 – 5:45):**
> ⚠️ *En documentos muy largos puede saltarse partes. Siempre verifica afirmaciones críticas.*

---

### 🎬 ESCENA 5 — Creatividad (5:45 – 7:00)

**Pantalla:**
- Mostrar un bloque creativo: una persona escribiendo un brief que se queda en blanco a mitad de párrafo.
- Cut a Claude. Escribir:

```
Estoy escribiendo un artículo sobre por qué los equipos
remotos necesitan rituales sincrónicos, pero estoy
bloqueado. No me des respuestas — hazme cinco preguntas
poderosas que me ayuden a desbloquear qué quiero
realmente decir.
```

- Mostrar las 5 preguntas. Una de ellas debería ser muy buena (Claude tiende a producir al menos una).

**Después**, demo de brainstorming amplio:

```
Necesito 30 ángulos posibles para un artículo sobre
"el final de las videollamadas". No filtres. Quiero
extremos, contraintuitivos, técnicos, emocionales,
estéticos. Lista numerada.
```

**Y después**, crítica constructiva:

```
Sé el editor más exigente del mundo. Lee este párrafo
y dime, sin filtros, qué está mal, qué sobra, qué falta.

[pegar un párrafo cualquiera]
```

**Narración:**
> "**Creatividad.** Y aquí va el matiz importante: Claude no es un sustituto de tu criterio creativo. **Es una pareja creativa.**
>
> Cuatro flujos que funcionan especialmente bien.
>
> **Brainstorming amplio.** 'Dame 30 ángulos posibles para este artículo.' No filtres. Después tú eliges. La cantidad genera la calidad.
>
> **Construcción de personajes** — perfiles, backstories, voces narrativas.
>
> **Variantes.** 'Dame 5 versiones de este eslogan con tonos distintos.'
>
> **Bloqueos creativos.** El truco aquí es contraintuitivo: **no le pidas respuestas, pídele preguntas.** 'Hazme cinco preguntas que me ayuden a desbloquear qué quiero decir.' Funciona.
>
> Y **crítica constructiva** — 'sé el editor más exigente del mundo y rompe este texto'. Para puntos ciegos.
>
> Donde no llega: Claude no vive en el mundo. No sabe lo que está de moda esta semana en tu ciudad ni qué va a emocionar a tu público concreto. **Tu criterio sigue siendo el filtro final.** Siempre."

---

### 🎬 ESCENA 6 — Cierre y puente al Módulo 7 (7:00 – 7:30)

**Pantalla:**
- Resumen de los 4 casos con un check verde al lado de cada uno.

**Narración:**
> "Cuatro casos. Cuatro flujos que puedes empezar a usar mañana. Pero antes de soltarte, necesitamos hablar de las cosas que Claude **no debería** hacer — privacidad, alucinaciones, límites éticos. Eso es el próximo módulo. Nos vemos ahí."

---

## Prompts de demo (copiables)

**Demo escritura — reescritura de email:**
```
Este es el borrador de un email que quiero mandar a un cliente con el que estoy frustrado pero al que necesito mantener contento. Reescríbelo: tono profesional y cálido, sin dejar de pedir claridad para tomar decisiones. Máximo 5 frases. Termina ofreciendo una llamada esta semana para desbloquear.

[Borrador a pegar:]
Hola Pedro,
Vale, lo que me pides es complicado porque no tengo gente disponible y además llevamos semanas con esto sin que tomes decisiones. Te lo intento sacar para el viernes pero si no llega ya sabes por qué.
Un saludo,
```

**Demo programación — debug:**
```
Este código JavaScript me lanza este error en producción:
TypeError: Cannot read properties of null (reading 'name')

¿Qué está pasando y cómo lo arreglo? Explícame en una frase y luego dame el fix con el código completo corregido.

[Fragmento de código con bug — preparar antes]
```

**Demo programación — explicar:**
```
Tengo este pedazo de código que heredé de un compañero que ya no está. ¿Puedes explicarme línea por línea qué hace y si hay algo que mejorarías?

[pegar fragmento]
```

**Demo análisis PDF:**
```
Adjunto un informe de mercado. Hazme tres cosas:
1) Identifica las cinco conclusiones clave.
2) Cita los datos más fuertes (con la página donde aparecen).
3) Dime qué información falta o está poco respaldada.
```

**Demo análisis Excel:**
```
Adjunto las ventas mensuales del último año. Hazme:
- Un resumen de tendencias (crecimiento, estacionalidad, anomalías).
- Las tres líneas de producto más rentables.
- Una recomendación de acción para el próximo trimestre.
Muéstrame los cálculos para que pueda verificarlos.
```

**Demo imagen / gráfico:**
```
¿Qué te dice esta gráfica? ¿Qué patrones ves? ¿Qué pregunta de seguimiento harías?
```

**Demo creatividad — preguntas para desbloquear:**
```
Estoy escribiendo un artículo sobre por qué los equipos remotos necesitan rituales sincrónicos, pero estoy bloqueado. No me des respuestas — hazme cinco preguntas poderosas que me ayuden a desbloquear qué quiero realmente decir.
```

**Demo creatividad — brainstorming amplio:**
```
Necesito 30 ángulos posibles para un artículo sobre "el final de las videollamadas". No filtres. Quiero extremos, contraintuitivos, técnicos, emocionales, estéticos. Lista numerada.
```

**Demo creatividad — crítica constructiva:**
```
Sé el editor más exigente del mundo. Lee este párrafo y dime, sin filtros, qué está mal, qué sobra, qué falta.

[pegar un párrafo]
```

---

## Checklist de pre-producción

- [ ] PDF de informe técnico de 5-10 páginas listo (anónimo o ficticio)
- [ ] Excel con datos ficticios pero realistas (preparar 12 meses de ventas con cierta estacionalidad)
- [ ] Imagen de dashboard descargada
- [ ] Fragmento de JavaScript con bug obvio preparado y probado (que Claude resuelva bien — testar antes)
- [ ] VS Code visible con tema claro o consistente

## Checklist de post-producción

- [ ] Pantalla partida para "antes / después" del email
- [ ] Highlights sobre las partes humanas del email reescrito
- [ ] Captura del .docx / .xlsx generado abierto en su app nativa para añadir como b-roll
- [ ] Subtítulos siempre activos
- [ ] Este módulo se puede romper en 4 micro-videos (1 por escena) para redes sociales
