# Módulo 7 — Buenas prácticas y límites
**Guion de producción de video · Claude 101**

---

## Ficha técnica

| Campo | Detalle |
|---|---|
| Duración objetivo | 7:00 (rango 6:30–7:30) |
| Audiencia | Mixta — esta lección es ESENCIAL antes de soltar a la gente con Claude en producción |
| Tono | Serio pero no alarmista. Honesto sobre los límites |
| Formato | Ejemplos concretos de qué evitar + cómo verificar |
| Cubre lecciones | 7.1 Privacidad · 7.2 Verificación · 7.3 Limitaciones · 7.4 Uso responsable |

## Objetivo

Que el espectador termine sabiendo **qué NO compartir, cómo verificar lo que Claude dice, qué no puede hacer**, y los principios éticos básicos al usarlo en el trabajo.

---

## Estructura del video

### 🎬 ESCENA 1 — Hook (0:00 – 0:25)

**Pantalla:**
- Tres titulares de noticias reales (que existen) sobre incidentes con IA — sin sonar alarmista, mostrando que "esto pasa":
  1. *"Empleados copiando datos confidenciales en ChatGPT"*
  2. *"Abogado citó casos inventados por IA en un juicio"*
  3. *"Decisiones de RRHH basadas en IA bajo escrutinio"*
- Después, una pantalla con el texto: *"No por miedo. Por criterio."*

**Narración:**
> "Antes de soltarte con Claude en producción, necesitamos hablar de las cosas que no debes hacer. No por miedo. Por criterio. Hay errores frecuentes que generan problemas reales — y todos son evitables si los conoces. En siete minutos te cuento los cuatro grupos."

**Title card:** *"Módulo 7 · Buenas prácticas y límites"*

---

### 🎬 ESCENA 2 — Privacidad y datos sensibles (0:25 – 2:15)

**Pantalla:**
- Lista grande en pantalla, cada punto aparece con un sonido suave:

```
❌ Datos personales de terceros sin permiso
❌ Contraseñas, claves API, tokens
❌ Números de tarjeta, cuentas bancarias
❌ Información confidencial de empresa
   sin revisar política interna
```

- Después, ejemplo concreto: una persona "iba" a pegar datos de clientes (mostrar un Excel con nombres y emails de clientes) y se detiene. Cambio a una versión anonimizada (Cliente A, Cliente B, ratios).

**Narración:**
> "**Privacidad y datos sensibles.** Cuatro reglas claras.
>
> Uno: **no compartas datos personales de terceros** sin permiso. Clientes, empleados, contactos. No es solo legalmente arriesgado — es ética básica.
>
> Dos: **nunca introduzcas contraseñas, claves API, números de tarjeta o datos bancarios.** Aunque te parezca privado, no lo es del modo que crees.
>
> Tres: **cuidado con información confidencial de empresa.** Revisa la política interna. Algunas empresas tienen acuerdos comerciales con Anthropic que cambian las garantías; otras tienen política contraria al uso de IA externa.
>
> Cuatro: **anonimiza cuando sea posible**. Si solo necesitas que Claude trabaje sobre la estructura de un caso, cambia nombres reales por ficticios. 'Cliente A' funciona igual de bien que 'Carmen García' — y dejas de exponer datos.
>
> Y configura tu cuenta. En los planes consumer de Anthropic, por defecto tus conversaciones **no se usan para entrenar futuros modelos**. Pero sí se almacenan durante un tiempo. Conviene saber qué política aplica a tu plan."

---

### 🎬 ESCENA 3 — Alucinaciones y verificación (2:15 – 4:00)

**Pantalla:**
- Demo en vivo de una alucinación. Escribir:

```
Cítame tres libros de economía publicados en 1987
sobre el papel de las divisas en crisis financieras,
con autor, editorial y número de páginas.
```

- Claude responde con datos que parecen plausibles. Aquí está la trampa: algunos pueden ser inventados.
- En pantalla: googlear uno de los libros. Si no existe, mostrar el "no results" en la búsqueda.

**Después**, mostrar la versión correcta:

```
Cítame tres libros de economía publicados en 1987
sobre el papel de las divisas en crisis financieras,
con autor, editorial y número de páginas.
ACTIVA LA BÚSQUEDA WEB y cita las fuentes para
que pueda verificar.
```

- Mostrar que ahora Claude busca y trae datos reales con links.

**Narración:**
> "**Alucinaciones.** Claude puede generar información que parece correcta pero no lo es. Datos inventados, citas falsas, referencias a libros que no existen. Sucede menos que en otros modelos. Pero sucede.
>
> Mira esta demo. Le pido tres libros de economía de 1987. Me los da, con autor, editorial, número de páginas. Suena perfecto. **Y uno no existe.** Lo confirmamos en Google.
>
> Esto pasa porque Claude no consulta una base de datos — genera la respuesta más probable. Y a veces lo más probable es algo plausible que no existe.
>
> **¿Cuándo verificar siempre?** Cuatro situaciones.
>
> Uno: **cifras, estadísticas, datos concretos.**
> Dos: **citas, referencias bibliográficas, URLs.**
> Tres: **fechas y eventos históricos específicos.**
> Cuatro: **información legal, médica o financiera concreta.**
>
> Y la quinta, que es la más sutil: **hechos sobre personas reales.**
>
> ¿Cómo verificar? Tres maneras. **Activa la búsqueda web** y pídele que cite. **Contrasta con fuentes primarias.** Y una costumbre útil: preguntarle '¿estás seguro? ¿cómo lo sabes?'. A veces se rectifica."

---

### 🎬 ESCENA 4 — Limitaciones que debes conocer (4:00 – 5:30)

**Pantalla:**
- Lista visual en pantalla, cada punto con un icono:

```
🧮 Cálculo numérico preciso sin herramientas
⏰ Información en tiempo real sin búsqueda
🤖 Ejecutar acciones por ti sin integraciones
🧠 Recordar entre conversaciones sin memoria
📁 Acceder a archivos privados sin que se los des
🎲 Garantizar reproducibilidad
```

- Para cada punto, una breve demo o ilustración (5 seg cada una).

**Narración:**
> "**Limitaciones honestas.** El mapa de lo que Claude no puede hacer.
>
> **Cálculo numérico preciso** sin herramientas. Las multiplicaciones largas, divisiones complejas, estadística avanzada — son fallables. Para números importantes, pídele que muestre los pasos o que use una calculadora real.
>
> **Información en tiempo real** sin búsqueda web activada. Sin internet, su conocimiento tiene fecha de corte.
>
> **Ejecutar acciones por ti.** No puede mandar correos, hacer reservas, mover dinero ni tocar tus sistemas — salvo con integraciones específicas como conectores MCP.
>
> **Recordar entre conversaciones** salvo que actives la memoria. Cada chat empieza limpio por defecto.
>
> **Acceder a archivos privados.** No ve tu Drive, tu Dropbox, tu disco duro a menos que tú se lo subas o lo conectes explícitamente.
>
> Y la sutil: **reproducibilidad.** Dos veces el mismo prompt pueden dar respuestas distintas. Para flujos críticos donde necesitas el mismo output siempre, considera la API con parámetros fijos.
>
> Y una nota importante: **Claude no es un terapeuta, ni un médico, ni un abogado.** Puede ayudarte a entender, explorar, preparar preguntas. No sustituye a un profesional cuando el riesgo es real."

---

### 🎬 ESCENA 5 — Uso responsable y ético (5:30 – 6:40)

**Pantalla:**
- Tres tarjetas: **TRANSPARENCIA · SESGO · AUTORÍA**.
- Bajo cada una, un mini caso:
  - Transparencia: una persona publicando un artículo, dudando si declarar uso de IA.
  - Sesgo: una persona evaluando candidatos, dudando si Claude trata diferente a grupos distintos.
  - Autoría: una persona enviando un informe firmado con su nombre.

**Narración:**
> "Y tres principios que conviene tener clavados.
>
> **Transparencia.** Si publicas contenido generado o asistido por IA en contextos donde el lector lo esperaría saber — medios, académico, profesional — sé transparente. La regla simple: ¿se sentiría engañado el receptor si lo supiera? Si la respuesta es sí, declara.
>
> **Sesgo y representación.** Claude refleja sesgos presentes en sus datos de entrenamiento. Cuando lo uses para tomar decisiones sobre personas — RRHH, créditos, evaluaciones — aplica supervisión humana y considera cómo el sistema puede tratar distinto a grupos diferentes. La velocidad no compensa la injusticia.
>
> **Tu autoría sigue siendo tuya.** Que una herramienta te ayude no quita tu responsabilidad sobre el resultado final. Lo que publicas con tu nombre, lo respondes con tu nombre. Si Claude se equivoca en una cifra del informe que firmas, el problema es tuyo, no suyo."

**Callout (6:25 – 6:40):**
> 🧭 *Usa Claude para amplificar lo que tú haces bien, no para sustituir el pensamiento crítico, el criterio profesional y la responsabilidad.*

---

### 🎬 ESCENA 6 — Cierre y puente al Módulo 8 (6:40 – 7:00)

**Pantalla:**
- Resumen visual de los 4 grupos en una grilla 2×2: Privacidad / Verificación / Limitaciones / Ética.

**Narración:**
> "Privacidad, verificación, limitaciones, ética. Cuatro grupos. Cuatro disciplinas. Tener esto claro es lo que separa al usuario casual del profesional que sabe lo que hace. En el último módulo damos el salto al siguiente nivel: Claude Code, conectores MCP y dónde seguir aprendiendo. Nos vemos ahí."

---

## Prompts de demo (copiables)

**Demo alucinación (escena 3) — primera versión:**
```
Cítame tres libros de economía publicados en 1987 sobre el papel de las divisas en crisis financieras, con autor, editorial y número de páginas.
```

**Demo verificación — segunda versión:**
```
Cítame tres libros de economía publicados en 1987 sobre el papel de las divisas en crisis financieras, con autor, editorial y número de páginas. ACTIVA LA BÚSQUEDA WEB y cita las fuentes para que pueda verificar.
```

**Demo opcional — pregunta de control:**
```
¿Estás seguro de cada uno de estos datos? ¿Cómo los sabes? Si alguno no puedes verificarlo, dímelo claramente.
```

---

## Checklist de pre-producción

- [ ] Buscar previamente un caso de alucinación REAL que se pueda reproducir en pantalla
- [ ] Tener Excel ficticio con nombres reales aparentes (para escena de anonimización)
- [ ] Configurar la cuenta con búsqueda web activada para la segunda parte de escena 3
- [ ] Cuidado: no mostrar emails reales en pantalla aunque sea por accidente

## Checklist de post-producción

- [ ] Difuminar cualquier nombre/email real que aparezca por descuido
- [ ] Music slightly more subdued en este módulo (no épica, sí seria)
- [ ] El callout de cierre se puede exportar como tarjeta para redes
- [ ] Considerar añadir una "tarjeta de privacidad descargable" como link al final
