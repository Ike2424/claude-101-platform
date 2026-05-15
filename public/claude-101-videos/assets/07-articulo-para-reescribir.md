# Asset · Artículo para reescritura
**Usar en:** M4 · Escena 6 (prompt completo combinado) y M4 · Escena 5 (rol de editor)

---

## Contexto para el narrador

Artículo intencionalmente mediocre: lleno de tópicos, frases largas, jerga corporativa, conclusiones obvias. El objetivo es que Claude — actuando como editor exigente o aplicando el estilo "afilado" definido por few-shot — lo transforme en algo legible.

Mantener los datos numéricos (el modelo debe respetarlos según las restricciones del prompt).

---

## Artículo a copiar

```
LA REVOLUCIÓN DE LA INTELIGENCIA ARTIFICIAL EN EL ENTORNO LABORAL

En el actual contexto de transformación digital sin precedentes,
la inteligencia artificial se está posicionando como uno de los
pilares fundamentales de la innovación empresarial. Cada vez son
más las organizaciones que están apostando decididamente por
incorporar estas tecnologías punteras a sus flujos de trabajo,
con el objetivo de impulsar la eficiencia operativa y maximizar
el valor entregado a sus stakeholders.

Según un estudio reciente publicado en mayo de 2026 por una
prestigiosa consultora internacional, el 67% de las empresas a
nivel global han implementado al menos una solución basada en
IA en alguno de sus departamentos durante el último año. Este
dato, sin lugar a dudas, refleja la velocidad vertiginosa con
la que esta tecnología está siendo adoptada de manera masiva y
generalizada en todos los sectores de la economía mundial.

No obstante, no es oro todo lo que reluce. Existen numerosos
retos y desafíos que las empresas deben abordar con la máxima
seriedad y diligencia para asegurar una implementación exitosa
y sostenible en el tiempo. Entre estos desafíos, cabe destacar
de manera especialmente relevante: la formación adecuada del
personal, la integración con los sistemas legacy preexistentes,
y la necesidad imperiosa de establecer marcos éticos sólidos
que guíen la utilización responsable de estas herramientas.

En conclusión, podemos afirmar sin temor a equivocarnos que la
inteligencia artificial no es una moda pasajera ni una tendencia
efímera, sino una transformación profunda que ha llegado para
quedarse y que sin duda va a redefinir el futuro del trabajo
tal y como lo conocemos hoy en día. Las empresas que sepan
adaptarse de forma proactiva a este nuevo paradigma serán las
que liderarán los mercados del mañana, mientras que aquellas
que se resistan al cambio corren el riesgo de quedarse atrás
en una carrera donde los rezagados raramente tienen una segunda
oportunidad de subirse al tren.
```

## Datos numéricos a preservar tras la reescritura

- 67% de las empresas
- Estudio de mayo de 2026
- "Durante el último año"

## Prompt completo combinado (M4 · escena 6)

```
<rol>Actúa como editor senior de una revista de tecnología.</rol>

<tarea>Reescribe el siguiente artículo aplicando el estilo de los ejemplos.</tarea>

<ejemplos>
Ejemplo 1: "El móvil no te distrae. Tú permites que te distraiga."
Ejemplo 2: "La IA no reemplaza el criterio. Lo expone."
</ejemplos>

<articulo>
[pegar aquí el artículo de arriba]
</articulo>

<reglas>
- Máximo 600 palabras.
- Conservar todos los datos numéricos.
- Piensa paso a paso antes de reescribir y muestra tu razonamiento al final entre <pensamiento></pensamiento>.
</reglas>
```
