# Módulo 4 — Técnicas avanzadas de prompting
**Guion de producción de video · Claude 101**

---

## Ficha técnica

| Campo | Detalle |
|---|---|
| Duración objetivo | 7:00 (rango 6:30–7:30) |
| Audiencia | Mixta — esta lección es donde los usuarios "intermedios" salen del nivel principiante |
| Tono | Enseñante, paciente. Las técnicas requieren ver el "antes y después" para que valgan algo |
| Formato | Demo lado a lado, mucho énfasis en el resultado en pantalla |
| Cubre lecciones | 4.1 Cadenas de razonamiento · 4.2 Few-shot · 4.3 Etiquetas XML · 4.4 Roles y restricciones |

## Objetivo

Que el espectador domine 4 técnicas que **multiplican la calidad** de sus prompts y sepa cuándo usar cada una.

---

## Estructura del video

### 🎬 ESCENA 1 — Hook (0:00 – 0:25)

**Pantalla:**
- Mostrar un prompt típico del módulo 3 (ya bueno). Después, mostrar el mismo prompt con una técnica avanzada añadida. Las respuestas se muestran lado a lado.
- Overlay: *"Lo que separa un prompt bueno de uno que te ahorra una hora."*

**Narración:**
> "Si terminaste el módulo 3, ya escribes prompts decentes. Lo que vas a aprender ahora es lo que separa los prompts decentes de los que te ahorran horas reales de trabajo. Cuatro técnicas. Las cuatro las usan los profesionales que viven con Claude todos los días. No son complicadas — son disciplina."

**Title card:** *"Módulo 4 · Técnicas avanzadas de prompting"*

---

### 🎬 ESCENA 2 — Cadenas de razonamiento (0:25 – 2:00)

**Pantalla:**
- Setup: una conversación con un problema con varias capas. Sugerencia: analizar un fragmento de contrato.
- Primer intento — sin cadena: *"Analiza este contrato y dime si lo firmo."* → Claude da una respuesta corta, parece confiada, salta a la conclusión.
- Segundo intento — con cadena:

```
Analiza este contrato. Antes de darme tu conclusión, identifica
las cláusulas problemáticas una por una, explica por qué te preocupan,
y luego propón una recomendación final.
```

- Mostrar cómo la respuesta es ahora más larga, estructurada, y la conclusión final está mejor justificada. Marcar con highlights los pasos del razonamiento.

**Narración:**
> "**Primera técnica: cadenas de razonamiento.** En inglés se llama *chain-of-thought*. La idea es simple: en problemas con varias capas — matemáticas, lógica, análisis, planificación — pídele a Claude que **razone paso a paso antes de responder**. La calidad de la conclusión cambia radicalmente.
>
> Mira el ejemplo. Le pregunto sobre un contrato. La primera versión salta directo a una conclusión. La segunda — donde le pido que **primero identifique cláusulas problemáticas, después explique por qué le preocupan, y al final dé su recomendación** — produce un análisis mucho más sólido.
>
> Truco: cuando el problema tenga más de dos pasos lógicos, **pide explícitamente que separe etapas**. 'Primero haz X. Después Y. Por último Z, basándote en lo anterior.' Eso evita que se salte fases."

---

### 🎬 ESCENA 3 — Few-shot: enseñar con ejemplos (2:00 – 3:45)

**Pantalla:**
- Caso típico: convertir titulares neutros en versiones provocadoras (el ejemplo del curso).
- Sin few-shot: *"Hazme este titular más provocador: 'Guía para empezar a correr'."* → resultado mediocre.
- Con few-shot:

```
Convierte estos titulares en versiones más provocadoras:

Original: "Nuevo estudio sobre el sueño"
Provocador: "Lo que tu sueño dice de ti (y no querrás oírlo)"

Original: "Consejos para ahorrar"
Provocador: "Estás ahorrando mal. Esto es lo que nadie te cuenta."

Ahora hazlo con: "Guía para empezar a correr"
```

- Mostrar cómo el resultado ya hace lo que querías sin tener que describir un estilo abstracto.

**Narración:**
> "**Segunda técnica: few-shot prompting.** Mostrar es mejor que describir.
>
> Hay estilos y formatos que cuestan mucho describir con palabras. ¿Cómo le explicas a Claude el tono de tu marca? ¿O un formato de informe específico? Lo más rápido es darle dos o tres ejemplos del input y el output que esperas. Eso es few-shot.
>
> Mira: le pido un titular más provocador. Sin ejemplos, Claude adivina qué es 'provocador' para mí. Con dos ejemplos de cómo lo hago yo, Claude **infiere el patrón** y aplica mi estilo concreto.
>
> Dos avisos: con dos a cinco ejemplos suele bastar — más no mejora gran cosa. Y los ejemplos deben ser **consistentes entre sí**. Si los mezclas con estilos muy distintos, Claude se confunde y promedia."

---

### 🎬 ESCENA 4 — Etiquetas XML para estructurar (3:45 – 5:15)

**Pantalla:**
- Setup: un prompt largo (instrucciones + documento + ejemplos + estilo). Mostrar primero el prompt "todo seguido", con malos resultados — Claude se confunde sobre qué es instrucción y qué es contenido.
- Después, mostrar el mismo prompt con etiquetas XML:

```
<tarea>
Resume el siguiente documento en un párrafo.
</tarea>

<estilo>
Lenguaje claro, frases cortas, sin tecnicismos.
</estilo>

<documento>
[aquí el texto largo]
</documento>
```

- Mostrar cómo la respuesta es ahora mucho más precisa: respeta el estilo, no mezcla el contenido del documento con las instrucciones.

**Narración:**
> "**Tercera técnica: etiquetas XML.** Cuando tu prompt empieza a tener varias secciones, **separa los bloques con etiquetas**. Instrucciones, documento, estilo, ejemplos. Cada uno en su etiqueta. Claude distingue mucho mejor qué es qué.
>
> No es magia. Es claridad estructural. Y un detalle: no tienes que usar etiquetas estándar. **Invéntalas**. Lo que importa es que separen bloques con propósitos distintos. Mira."

**Pausa-frame (5:00):** Mostrar el prompt con etiquetas en pantalla durante 5 segundos para que el espectador lo lea.

**Narración (continuación):**
> "Esto se nota especialmente en prompts largos — los que usas para flujos complejos. Pasar de un párrafo confuso a este tipo de estructura cambia los resultados al instante."

---

### 🎬 ESCENA 5 — Roles, personas y restricciones (5:15 – 6:30)

**Pantalla:**
- Demo 1 — sin rol: *"Revisa mi artículo y dime qué partes mejorar."* → respuesta amable y poco crítica.
- Demo 2 — con rol:

```
Actúa como un editor de revista de divulgación científica
con 20 años de experiencia. Revisa mi artículo y dime,
sin filtros, qué partes son confusas para un lector general.
```

- Mostrar cómo cambia el tono — más exigente, más concreto, mejor "criterio editorial".

**Después en pantalla**, mostrar una lista de restricciones útiles con ejemplos cortos:

```
🔹 LONGITUD       "Máximo 200 palabras."
🔹 FORMATO        "Devuélvelo como tabla en Markdown."
🔹 VOCABULARIO    "No uses tecnicismos."
🔹 ESTRUCTURA     "Empieza con la conclusión y luego justifícala."
```

**Narración:**
> "**Cuarta técnica: roles y restricciones.**
>
> Pedirle a Claude que adopte un rol específico cambia el tono, el vocabulario y el enfoque. Es útil cuando quieres una perspectiva concreta. 'Actúa como editor de revista de divulgación científica con veinte años de experiencia.' La respuesta cambia. La crítica es más exigente, los comentarios son más concretos, el filtro se afina.
>
> Y junto al rol, las restricciones. Bien usadas no limitan — **enfocan**. Longitud máxima. Formato exacto. Prohibición de tecnicismos. Estructura: 'empieza con la conclusión y luego justifícala'. Cada restricción reduce la deriva. Cada restricción mejora el resultado."

---

### 🎬 ESCENA 6 — Combinación: el prompt "completo" (6:30 – 7:00)

**Pantalla:**
- Mostrar un prompt final que combina las cuatro técnicas. Resaltar cada técnica con un color distinto:

```
<rol>                                                           🔴 ROL
Actúa como editor senior de una revista de tecnología.
</rol>

<tarea>                                                         🟠 TAREA
Reescribe el siguiente artículo aplicando el estilo de los ejemplos.
</tarea>

<ejemplos>                                                      🟡 FEW-SHOT
[2 fragmentos cortos del estilo deseado]
</ejemplos>

<articulo>                                                      🟢 INPUT
[artículo a reescribir]
</articulo>

<reglas>                                                        🔵 RESTRICCIONES
- Máximo 600 palabras.
- Conservar todos los datos numéricos.
- Pensar paso a paso antes de reescribir y mostrar tu razonamiento al final entre <pensamiento></pensamiento>.
</reglas>
```

**Narración:**
> "Las cuatro técnicas se combinan. Mira este prompt: rol claro, tarea explícita, ejemplos del estilo deseado, restricciones precisas, y una instrucción de cadena de razonamiento al final. Esto no es exagerado — es lo que escribe la gente que vive con Claude. Y, créeme, el resultado lo justifica.
>
> En el próximo módulo dejamos el texto puro y entramos en lo que Claude puede crear: documentos vivos, archivos, búsqueda web. Nos vemos ahí."

---

## Prompts de demo (copiables)

**Demo 1 — Cadena de razonamiento (escena 2):**

Sin cadena:
```
Analiza este contrato y dime si lo firmo.
```

Con cadena:
```
Analiza este contrato. Antes de darme tu conclusión, identifica las cláusulas problemáticas una por una, explica por qué te preocupan, y luego propón una recomendación final.
```

(Para grabar: usa un fragmento de contrato ficticio de 1 página — cláusulas de no competencia, propiedad intelectual, etc.)

**Demo 2 — Few-shot (escena 3):**
```
Convierte estos titulares en versiones más provocadoras:

Original: "Nuevo estudio sobre el sueño"
Provocador: "Lo que tu sueño dice de ti (y no querrás oírlo)"

Original: "Consejos para ahorrar"
Provocador: "Estás ahorrando mal. Esto es lo que nadie te cuenta."

Ahora hazlo con: "Guía para empezar a correr"
```

**Demo 3 — XML (escena 4):**
```
<tarea>
Resume el siguiente documento en un párrafo.
</tarea>

<estilo>
Lenguaje claro, frases cortas, sin tecnicismos.
</estilo>

<documento>
[texto largo — usa una entrada de blog de prueba, 800 palabras aprox.]
</documento>
```

**Demo 4 — Rol (escena 5):**
```
Actúa como un editor de revista de divulgación científica con 20 años de experiencia. Revisa mi artículo y dime, sin filtros, qué partes son confusas para un lector general.

[pega aquí el artículo de prueba]
```

**Demo 5 — Prompt completo combinado (escena 6):**
```
<rol>Actúa como editor senior de una revista de tecnología.</rol>

<tarea>Reescribe el siguiente artículo aplicando el estilo de los ejemplos.</tarea>

<ejemplos>
Ejemplo 1: "El móvil no te distrae. Tú permites que te distraiga."
Ejemplo 2: "La IA no reemplaza el criterio. Lo expone."
</ejemplos>

<articulo>
[artículo a reescribir]
</articulo>

<reglas>
- Máximo 600 palabras.
- Conservar todos los datos numéricos.
- Piensa paso a paso antes de reescribir y muestra tu razonamiento al final entre <pensamiento></pensamiento>.
</reglas>
```

---

## Checklist de pre-producción

- [ ] Contrato ficticio (1 página) preparado
- [ ] Artículo ficticio (~800 palabras) preparado para escena 4 y 6
- [ ] Limpiar conversaciones previas — empezar cada demo desde cero para evitar contaminación de contexto

## Checklist de post-producción

- [ ] Highlights de colores por tipo de técnica (cadena=naranja, few-shot=amarillo, XML=verde, rol=rojo)
- [ ] Mostrar el prompt completo en escena 6 con animación de cada bloque apareciendo
- [ ] Este módulo se beneficia de subtítulos siempre visibles
