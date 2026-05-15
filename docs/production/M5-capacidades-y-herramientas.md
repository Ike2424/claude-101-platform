# Módulo 5 — Capacidades y herramientas
**Guion de producción de video · Claude 101**

---

## Ficha técnica

| Campo | Detalle |
|---|---|
| Duración objetivo | 7:30 (rango 7:00–8:00) |
| Audiencia | Mixta — este módulo "vende" las capacidades visualmente |
| Tono | Demostrativo, ritmo dinámico. Mostrar resultados rápido |
| Formato | Demo en vivo de cada capacidad — el espectador necesita VER los outputs |
| Cubre lecciones | 5.1 Artifacts · 5.2 Búsqueda web · 5.3 Creación de archivos · 5.4 Memoria |

## Objetivo

Que el espectador vea con sus propios ojos las **4 capacidades nucleares** de Claude más allá del texto plano: artifacts, búsqueda web, archivos y memoria.

## Equipo y assets

- Claude.ai con búsqueda web activada y creación de archivos habilitada.
- 1 documento PDF largo para subir en escena de búsqueda (un research report sobre un tema actual).
- Visor de archivos para abrir el .docx/.xlsx generados durante la grabación.

---

## Estructura del video

### 🎬 ESCENA 1 — Hook (0:00 – 0:25)

**Pantalla:**
- Montaje rápido (cortes de 1-2 segundos): un artifact interactivo apareciendo · una respuesta con citas web · un archivo .xlsx descargándose · una conversación recordando algo de la semana pasada.

**Narración:**
> "Hasta ahora Claude ha sido texto que entra, texto que sale. Esto cambia ahora. En este módulo ves cómo Claude crea documentos vivos, busca en internet, genera archivos en Word, Excel y PowerPoint, y recuerda entre conversaciones. Quédate hasta el final, porque la cuarta capacidad — la memoria — cambia tu flujo si la sabes usar."

**Title card:** *"Módulo 5 · Capacidades y herramientas"*

---

### 🎬 ESCENA 2 — Artifacts: documentos vivos (0:25 – 2:30)

**Pantalla:**
- Cut a claude.ai. Escribir:

```
Créame una calculadora simple de retorno sobre inversión
para evaluar campañas de marketing. Que tenga campos para
inversión, ingresos, número de leads y conversión. Que muestre
el ROI y el coste por lead. Que sea bonita y use mi paleta:
naranja #C8542B, crema #F4EFE3, oliva #4F5D38.
```

- Enviar. Mostrar cómo se abre el artifact en panel derecho — código + preview interactivo. Probar la calculadora en pantalla (introducir números, ver resultados).

- Después, iterar:

```
Añade un campo para CAC (coste de adquisición) y muestra
la rentabilidad como semáforo: verde si ROI > 300%, ámbar
entre 100-300%, rojo si menor de 100%.
```

- Mostrar cómo el artifact se actualiza en vivo, sin reempezar.

**Narración:**
> "Empezamos por **Artifacts** — la función más espectacular cuando la ves la primera vez.
>
> Un artifact es un bloque de contenido sustancial que aparece en un panel aparte de la conversación. Sirve para código, documentos largos, componentes interactivos, visualizaciones, juegos, prototipos web. Cualquier cosa que sea útil ver fuera del hilo del chat.
>
> Le voy a pedir una calculadora de retorno sobre inversión para campañas de marketing. Mira lo que pasa."

**Pausa para mostrar la generación en vivo (1:15).**

**Narración (continuación):**
> "El artifact aparece a la derecha. Es **funcional** — puedo meter números y calcular. Y aquí viene lo potente: puedo iterar. 'Añade un campo de coste de adquisición. Muestra la rentabilidad como semáforo verde, ámbar, rojo.' Mira cómo se actualiza sin reempezar desde cero.
>
> **Cuándo usar Artifacts:** cuando quieres prototipar una idea visual rápido. Describe lo que quieres, itera tres o cuatro veces, y tienes una versión funcional. Te ahorra horas de mock-ups."

---

### 🎬 ESCENA 3 — Búsqueda web e investigación (2:30 – 4:15)

**Pantalla:**
- Cut a una conversación nueva. Mostrar el botón "Web search" o el toggle de búsqueda. Activarlo.
- Escribir:

```
¿Cuáles son las tres novedades más importantes de Claude
anunciadas en los últimos 30 días? Cita fuentes.
```

- Enviar. Mostrar:
  1. Los pasos de búsqueda apareciendo (icono de globo girando).
  2. La respuesta final con citas y links a fuentes.
- Highlights amarillos sobre las citas para que el espectador note que están ahí.

**Después**, mostrar el **modo de investigación profunda** (research mode). Escribir:

```
Hazme un informe sobre el estado del mercado de IA aplicada
a productividad en pymes — adopción, principales players,
barreras y oportunidades. Cita fuentes primarias.
```

- Enviar y mostrar el proceso (puede tomar 2-5 minutos en realidad — en post-producción, time-lapse). Mostrar el informe final estructurado.

**Narración:**
> "**Segunda capacidad: búsqueda web e investigación.** Claude por defecto te responde con lo que aprendió en el entrenamiento — y tiene fecha de corte. Si pregunto qué pasó la semana pasada, no puede saberlo. Pero le puedo activar la búsqueda web.
>
> Mira — le pregunto por las novedades de Claude del último mes. Activa el toggle, lanzo la pregunta. Claude busca, lee, sintetiza y me responde con **citas a las fuentes**. Eso es clave: siempre que uses búsqueda, **pídele que cite**.
>
> ¿Cuándo activar búsqueda? Información posterior al corte de conocimiento. Datos que cambian rápido — precios, cotizaciones, noticias. Verificación de hechos. Investigación sobre empresas, productos o personas actuales.
>
> Y para algo más serio, existe el **modo de investigación profunda**. Dedica más tiempo, hace múltiples búsquedas, produce un informe estructurado con citas. Lo uso para análisis de mercado, due diligence, estudios temáticos. Tarda más — minutos en lugar de segundos — pero la calidad sube mucho."

**Callout (4:00 – 4:15):**
> ⚠️ *La web también tiene desinformación. Verifica los datos críticos siempre.*

---

### 🎬 ESCENA 4 — Creación de archivos (4:15 – 6:00)

**Pantalla:**
- Nueva conversación. Activar la función "Create file" / "Generate file".

**Demo 1 — Word:**
```
Créame una propuesta comercial en Word para un cliente
ficticio "Café Aurora, cadena de cafeterías". Servicio:
diseño de identidad visual. Presupuesto: 8.500€.
Plazo: 6 semanas. Estructura: portada, índice,
3 secciones (entendimiento del cliente, propuesta de
trabajo, plan de entrega), tabla de precios al final.
```

- Mostrar el archivo .docx descargándose. Abrirlo en pantalla. Hacer scroll lento mostrando que tiene portada, índice automático, secciones, tabla.

**Demo 2 — Excel:**
```
Créame un modelo de previsión de tesorería en Excel
para los próximos 12 meses. Una pestaña con ingresos
mensuales por línea de producto, otra con gastos
operativos, otra con el resumen. Que use fórmulas
reales, no valores estáticos.
```

- Mostrar el archivo .xlsx descargándose. Abrirlo. Hacer clic en una celda con fórmula para mostrar que sí, es una fórmula real.

**Narración:**
> "**Tercera capacidad: creación de archivos.** Claude no solo te entrega texto en el chat. Puede generar el archivo directamente — Word, Excel, PowerPoint, PDF, código.
>
> Mira una propuesta comercial. Le doy estructura: portada, índice, tres secciones, tabla de precios. Y me genera un .docx real, con formato. No es texto que tengo que copiar y pegar — es el archivo, listo.
>
> Y mejor todavía: modelos de Excel **con fórmulas**, no con valores estáticos. Esto cambia tu trabajo si haces presupuestos, forecasts o análisis financieros.
>
> Consejo: **sé específico con la estructura**. Cuanto más describas — secciones, columnas, formato — mejor sale. 'Hazme una propuesta' produce algo genérico. 'Hazme una propuesta con portada, índice, tres secciones de tales nombres, y tabla de precios al final' produce lo que querías."

---

### 🎬 ESCENA 5 — Memoria y conversaciones pasadas (6:00 – 7:10)

**Pantalla:**
- Ir a Settings → Features → activar "Memory".
- Abrir una conversación nueva. Escribir:

```
Acabo de empezar un proyecto nuevo: lanzar una newsletter
quincenal sobre IA para profesionales de marketing. Audiencia
objetivo 5.000 suscriptores en 12 meses. Recuerda esto.
```

- Cerrar la conversación. Abrir otra nueva. Escribir:

```
¿En qué proyecto estoy trabajando ahora mismo?
```

- Mostrar que Claude responde con la info que se le dio antes.

- Después, demostrar **búsqueda en historial**:

```
¿De qué hablamos la semana pasada sobre los modelos de Anthropic?
```

- Claude busca en conversaciones pasadas y resume.

**Narración:**
> "**Cuarta capacidad: memoria.** Dos tipos.
>
> El primero, **memoria automática**. Si la activas en ajustes, Claude guarda automáticamente datos relevantes — tu nombre, tus preferencias, los proyectos en los que trabajas — y los usa en futuras conversaciones. Como mi colega que no necesita que le explique cada vez quién soy.
>
> El segundo, **búsqueda en el historial**. Permite que Claude consulte conversaciones pasadas cuando lo pidas. '¿De qué hablamos la semana pasada sobre el lanzamiento?' — y te lo trae.
>
> Atención: la memoria es útil **pero también puede contaminar** conversaciones nuevas con contexto antiguo irrelevante. En la configuración puedes ver qué recuerda, editar o borrar. Si vas a hacer una tarea muy distinta a las habituales, considera empezar limpio."

---

### 🎬 ESCENA 6 — Cierre y puente al Módulo 6 (7:10 – 7:30)

**Pantalla:**
- Cuatro iconos resumiendo lo visto: 🧩 Artifacts · 🌐 Web · 📄 Archivos · 🧠 Memoria.

**Narración:**
> "Cuatro capacidades que multiplican lo que puedes hacer. Artifacts para prototipar visualmente. Búsqueda web para información actual. Creación de archivos para no copiar y pegar. Memoria para que tu Claude conozca tu contexto. En el próximo módulo entramos a los casos de uso reales — los flujos concretos donde todo esto se aplica a tu trabajo diario."

---

## Prompts de demo (copiables)

**Demo Artifacts:**
```
Créame una calculadora simple de retorno sobre inversión para evaluar campañas de marketing. Que tenga campos para inversión, ingresos, número de leads y conversión. Que muestre el ROI y el coste por lead. Que sea bonita y use mi paleta: naranja #C8542B, crema #F4EFE3, oliva #4F5D38.
```

Iteración 1:
```
Añade un campo para CAC (coste de adquisición) y muestra la rentabilidad como semáforo: verde si ROI > 300%, ámbar entre 100-300%, rojo si menor de 100%.
```

**Demo Web search:**
```
¿Cuáles son las tres novedades más importantes de Claude anunciadas en los últimos 30 días? Cita fuentes.
```

**Demo Research:**
```
Hazme un informe sobre el estado del mercado de IA aplicada a productividad en pymes — adopción, principales players, barreras y oportunidades. Cita fuentes primarias.
```

**Demo Word:**
```
Créame una propuesta comercial en Word para un cliente ficticio "Café Aurora, cadena de cafeterías". Servicio: diseño de identidad visual. Presupuesto: 8.500€. Plazo: 6 semanas. Estructura: portada, índice, 3 secciones (entendimiento del cliente, propuesta de trabajo, plan de entrega), tabla de precios al final.
```

**Demo Excel:**
```
Créame un modelo de previsión de tesorería en Excel para los próximos 12 meses. Una pestaña con ingresos mensuales por línea de producto, otra con gastos operativos, otra con el resumen. Que use fórmulas reales, no valores estáticos.
```

**Demo Memoria — setup:**
```
Acabo de empezar un proyecto nuevo: lanzar una newsletter quincenal sobre IA para profesionales de marketing. Audiencia objetivo 5.000 suscriptores en 12 meses. Recuerda esto.
```

**Demo Memoria — recall (conversación nueva):**
```
¿En qué proyecto estoy trabajando ahora mismo?
```

---

## Checklist de pre-producción

- [ ] Búsqueda web ACTIVADA en ajustes
- [ ] Creación de archivos ACTIVADA en ajustes
- [ ] Memoria ACTIVADA en ajustes
- [ ] Reservar al menos 10 minutos extra de grabación para esperar al modo Research
- [ ] Visor de archivos preparado (Word, Excel) para abrir los outputs en pantalla
- [ ] Borrar memorias previas (Settings → Memory → Clear) para que la demo empiece limpia

## Checklist de post-producción

- [ ] Time-lapse del modo Research (de 3 min reales a 15 segundos en pantalla)
- [ ] Highlight amarillo sobre las citas web cuando aparecen
- [ ] Animar la apertura del artifact (panel derecho deslizándose)
- [ ] Captura del archivo Word/Excel abierto en su app nativa (b-roll)
- [ ] El bloque de memoria es perfecto como teaser para redes sociales — exportar como clip aparte
