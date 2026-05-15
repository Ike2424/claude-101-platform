# Módulo 8 — Siguiente nivel
**Guion de producción de video · Claude 101**

---

## Ficha técnica

| Campo | Detalle |
|---|---|
| Duración objetivo | 7:30 (rango 7:00–8:00) |
| Audiencia | Mixta — pero la primera mitad es más dev y la segunda es para todos |
| Tono | Inspirador. Es el video de cierre. Que el espectador termine motivado a seguir |
| Formato | 50% demo (Claude Code + MCP) · 50% cierre y proyecto final |
| Cubre lecciones | 8.1 Claude Code · 8.2 Conectores MCP · 8.3 Recursos · 8.4 Proyecto final |

## Objetivo

Que el espectador tenga **una idea clara de los siguientes 90 días** — qué explorar después de Claude 101 — y que tenga un proyecto concreto para empezar mañana.

## Equipo y assets

- Terminal con Claude Code instalado.
- Un repo de código pequeño para demostrar Claude Code (puede ser cualquier proyecto open source o un repo de prueba).
- Cuenta de Claude.ai con al menos 2-3 conectores activados (Google Drive, GitHub, Slack si es posible).

---

## Estructura del video

### 🎬 ESCENA 1 — Hook (0:00 – 0:25)

**Pantalla:**
- Time-lapse: Terminal abriéndose con Claude Code, Claude.ai mostrando un conector de Drive, una persona enviando un mensaje a Slack desde Claude.

**Narración:**
> "Hasta aquí, todo lo que has aprendido vive dentro del chat. En este último módulo abrimos las puertas — Claude trabajando en tu terminal, Claude conectado a tus apps, y un proyecto final que va a convertir todo lo aprendido en algo que usarás todas las semanas. Empezamos."

**Title card:** *"Módulo 8 · Siguiente nivel"*

---

### 🎬 ESCENA 2 — Claude Code (0:25 – 2:45)

**Pantalla:**
- Cut a Terminal. Mostrar el comando de instalación:

```
npm install -g @anthropic-ai/claude-code
```

- Después, `claude --version` para confirmar.
- Entrar a un directorio de proyecto: `cd ~/proyectos/landing-page` y ejecutar `claude`.
- Pedirle dentro del terminal:

```
Mira esta base de código. Resume su estructura en 5 frases.
```

- Claude lee, contesta. Después:

```
En components/Header.tsx hay un botón que está pegado al
logo en mobile. Arréglalo respetando los breakpoints
existentes en tailwind.config.js. Hazme un diff antes
de aplicar cambios.
```

- Mostrar a Claude proponiendo un diff, el usuario aprobando, y los cambios aplicándose.

**Narración:**
> "**Claude Code.** Si escribes código, esto cambia tu trabajo.
>
> Claude Code es una herramienta de línea de comandos que trae las capacidades de Claude directamente al terminal. Permite que Claude **lea, escriba y edite archivos** en tu proyecto, ejecute comandos, y trabaje en tareas de programación con autonomía supervisada.
>
> Mira cómo funciona. Lo instalo con npm. Entro a un proyecto. Lanzo `claude`. Y ya está dentro.
>
> Le pido que me resuma la estructura. Lee, contesta. Le pido que me arregle un bug específico — un botón mal posicionado en mobile — respetando los breakpoints existentes. Me propone un diff. Yo lo apruebo. Los cambios se aplican.
>
> **¿Para qué sirve?** Refactorizar partes de una base de código. Crear features completas partiendo de una descripción. Generar tests, documentación, migraciones. Investigar problemas que cruzan varios archivos. Integrar con Git, CI/CD, y otras herramientas.
>
> No es un autocompletar. Es un colega senior que abre archivos, hace preguntas, y propone cambios. Si te dedicas a programar, dedícale dos tardes a aprender los flujos. Vuelve diferente."

---

### 🎬 ESCENA 3 — Conectores MCP (2:45 – 4:45)

**Pantalla:**
- Cut a claude.ai → Settings → Connectors. Mostrar la lista: Google Drive, GitHub, Slack, Asana, Linear, Jira, Salesforce, etc.
- Activar Google Drive si no lo está. Mostrar el flujo de OAuth (sin mostrar credenciales).
- Volver a una conversación. Escribir:

```
Mira en mi Google Drive si tengo el brief del proyecto
"Café Aurora" y resúmemelo en 5 viñetas.
```

- Mostrar a Claude buscando en Drive y devolviendo el resumen.

- Después, demostrar otra capacidad cross-app:

```
Crea una tarea en Asana para mi proyecto "Web Café Aurora"
con título "Revisar versión final del brief", descripción
basada en el resumen de arriba, asignada a mí, con vencimiento
el viernes.
```

**Narración:**
> "**Conectores MCP.** Si Claude Code abre el terminal, los conectores MCP abren tus apps.
>
> **MCP** — Model Context Protocol — es un estándar abierto que permite a Claude conectarse con apps externas. Google Drive, Notion, GitHub, Slack, Asana, Linear, Jira, Salesforce. Y la lista crece cada semana.
>
> Mira. Activo Drive. Le pido a Claude que busque un brief en mi Drive y me lo resuma. Lo encuentra, lo lee, me lo resume — sin que yo lo descargue ni lo pegue.
>
> Después: 'Crea una tarea en Asana basada en este resumen.' Lo crea. Lo veo aparecer en Asana en tiempo real.
>
> Esto es donde Claude deja de ser una conversación y se convierte en un **asistente integrado** en tu flujo. Los conectores se activan desde los ajustes. Cada conector pide los permisos necesarios. **Revisa siempre qué da acceso a qué antes de aprobar** — esto es importante por privacidad."

**Callout (4:30 – 4:45):**
> 🔌 *Cada conector da acceso a datos. Revisa permisos antes de aprobar.*

---

### 🎬 ESCENA 4 — Recursos para seguir (4:45 – 5:45)

**Pantalla:**
- Pantalla limpia con 3 bloques:

```
📘 docs.claude.com
📘 support.claude.com
📘 anthropic.com/news
```

- Después, otra pantalla:

```
💬 Reddit:  r/ClaudeAI
💬 Discord: comunidades de Claude / Anthropic
💬 X / Twitter:  buscar "Claude prompt engineering"
```

- Después, una tercera pantalla con un calendario marcado:

```
Semana 1   →   Tarea repetitiva A · Convertirla en flujo Claude
Semana 2   →   Iterar el flujo. Documentarlo.
Semana 3   →   Tarea B. Empezar de cero.
Semana 4   →   Compartir lo aprendido.
```

**Narración:**
> "**Recursos.** Te dejo el mapa para seguir.
>
> **Documentación oficial.** Tres direcciones que vale la pena tener guardadas: `docs.claude.com` para la API y los productos, `support.claude.com` para ayuda y guías de Claude.ai, y `anthropic.com/news` para los anuncios.
>
> **Comunidades.** Hay gente activa en Reddit, Discord y X. Si buscas 'Claude prompt engineering' encuentras hilos donde la gente comparte prompts, trucos, casos de uso reales. Las mejores ideas están ahí.
>
> Y la parte más importante: **práctica deliberada.** Mira esto."

**Pausa en la pantalla del calendario (5:25 – 5:45):**

**Narración (continuación):**
> "La mejor forma de mejorar: identifica una tarea repetitiva en tu trabajo. Conviértela en un flujo con Claude. Itera durante una semana. Después busca otra. En tres meses tendrás un repertorio personal de flujos que multiplican tu productividad. **Esto pasa de verdad si te disciplinas a hacerlo.**"

---

### 🎬 ESCENA 5 — Proyecto final (5:45 – 7:15)

**Pantalla:**
- Una "ficha" del proyecto final con las 6 etapas, animada:

```
Proyecto final · Tu reto

1️⃣  Tarea elegida
2️⃣  Diseño del prompt
3️⃣  Primera prueba
4️⃣  Iteraciones (2-3)
5️⃣  Versión final
6️⃣  Reflexión
```

- Después, un ejemplo concreto. Mostrar a alguien (o solo en pantalla) eligiendo "redactar respuestas a candidatos de RRHH" como tarea, diseñando el prompt, iterando, llegando a una versión final.

**Narración:**
> "**El proyecto final.** Tu reto: elegir una tarea recurrente — semanal o más frecuente — y diseñar un flujo completo con Claude. Documentarlo. **Reutilizable.**
>
> Seis pasos.
>
> **Uno: tarea elegida.** Describe qué haces, cuánto te lleva, qué la hace pesada. Sé honesto contigo mismo. No es 'la tarea sexy' — es 'la tarea que pasa todas las semanas y odias'.
>
> **Dos: diseño del prompt.** Aplica las cuatro partes que vimos en el módulo 3: tarea, contexto, formato, restricciones.
>
> **Tres: primera prueba.** El resultado inicial. Qué funcionó, qué no.
>
> **Cuatro: iteraciones.** Dos o tres ajustes documentados, con el razonamiento detrás de cada uno. Esto vale oro cuando dentro de un mes quieras entender por qué tu prompt es como es.
>
> **Cinco: versión final.** El prompt definitivo. Listo para reutilizar. Cópialo, pégalo en un proyecto, dale título.
>
> **Seis: reflexión.** Tiempo ahorrado. Calidad. Próximos pasos. Esto último es importante: ¿qué tarea vas a abordar después?
>
> **Entregable:** dos o tres páginas con todo. Pero lo importante no es la longitud. Es que el prompt sea reutilizable y la documentación clara para que dentro de seis meses tú o un compañero podáis abrirlo y usarlo sin contexto."

---

### 🎬 ESCENA 6 — Cierre del curso (7:15 – 7:30)

**Pantalla:**
- Pantalla final con un mensaje grande, tipografía Fraunces:

```
Has terminado Claude 101.

Ahora viene la parte que importa:
usarlo.
```

- Logo del curso. Música sube un poco. Fade out.

**Narración:**
> "Has terminado Claude 101. Conoces los fundamentos. Las técnicas de prompting. Las capacidades. Los límites. Y tienes un proyecto concreto para empezar mañana.
>
> Lo que queda es lo importante: práctica. Usa Claude todos los días en cosas reales. En tres semanas, vas a sentir la diferencia. En tres meses, vas a haber convertido tu manera de trabajar.
>
> Suerte. Y empieza ahora."

---

## Prompts de demo (copiables)

**Demo Claude Code — resumen:**
```
Mira esta base de código. Resume su estructura en 5 frases.
```

**Demo Claude Code — fix:**
```
En components/Header.tsx hay un botón que está pegado al logo en mobile. Arréglalo respetando los breakpoints existentes en tailwind.config.js. Hazme un diff antes de aplicar cambios.
```

**Demo MCP — Drive search:**
```
Mira en mi Google Drive si tengo el brief del proyecto "Café Aurora" y resúmemelo en 5 viñetas.
```

**Demo MCP — Asana:**
```
Crea una tarea en Asana para mi proyecto "Web Café Aurora" con título "Revisar versión final del brief", descripción basada en el resumen de arriba, asignada a mí, con vencimiento el viernes.
```

---

## Checklist de pre-producción

- [ ] Claude Code instalado y funcionando (probar antes de grabar — si falla la primera vez, mal)
- [ ] Repo de prueba con un bug de CSS real para resolver
- [ ] Conectores MCP de Google Drive y Asana (o equivalente) ya autenticados
- [ ] Brief ficticio "Café Aurora" subido a Drive con antelación
- [ ] No grabar nombres reales del equipo en ningún Drive/Asana visible

## Checklist de post-producción

- [ ] Acelerar (1.5x o 2x) las partes del terminal donde Claude Code está "escribiendo"
- [ ] Highlight visual cuando aparece la tarea en Asana — "creado en tiempo real"
- [ ] Tarjeta final con el mensaje del curso completado — sólida, sin distracciones
- [ ] El video completo debe terminar con SUBE/LIKE/COMPARTE solo si vais a publicarlo en YouTube; si va embebido en el curso, omitir
- [ ] Considerar grabar una versión "extra" de 30 segundos solo con el cierre como tarjeta motivacional para redes
