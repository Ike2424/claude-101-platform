# Asset · Transcripción de reunión ficticia
**Usar en:** M3 · Escena 5 (Caso real: resumen de reunión)

---

## Contexto

Transcripción intencionalmente "real": tiene digresiones, comentarios off-topic, decisiones poco claras y un par de temas que se quedan colgando. Ideal para que Claude resuma con la estructura que pide el prompt sólido.

---

## Transcripción a copiar

```
Reunión semanal de producto — 14 mayo 2026
Asistentes: Laura (PM), Diego (Eng lead), Sofía (Diseño), Iván (Marketing).
Duración: 47 minutos.

Laura: Hola, ¿estamos todos? Sofía dijo que llegaba tarde
pero ya está.

Sofía: Sí, perdón, vengo del médico.

Laura: Nada, no te preocupes. Vamos al lío. Primer tema:
la feature de notificaciones push. Diego, ¿cómo lo veis?

Diego: Mirad, tenemos el backend hasta arriba con la migración
de la base de datos. Si os digo la verdad, hasta mediados de
junio no creo que podamos abordarlo. Sé que está prometido para
finales de mayo pero no puedo prometer algo que no vamos a entregar.

Laura: Vale, entonces lo movemos. Junio. ¿De acuerdo todos?
Marketing, ¿esto os rompe algo?

Iván: A ver, la campaña la teníamos pensada para finales de mayo,
pero si las notis llegan en junio... podemos retrasar la campaña
o lanzarla con la versión actual. Yo digo de retrasarla, no tiene
sentido lanzar a medias.

Laura: ¿Cuánto la retrasamos?

Iván: Si las notis llegan el 10 de junio, podríamos lanzar el 20.

Laura: Apuntado. Lanzamiento campaña: 20 de junio. ¿Quién es
responsable de coordinar la actualización con tu equipo?

Iván: Yo lo hago. Aunque del 25 al 1 de junio estoy de vacaciones.

Laura: Bueno, te lo apunto para el 22 entonces. Siguiente tema:
el rediseño del onboarding. Sofía.

Sofía: He preparado tres opciones. La A es más conservadora,
mantiene la estructura actual y solo cambia tono. La B es la
intermedia, reorganiza los pasos. La C es la más rompedora,
introduce un asistente conversacional.

Diego: ¿La C la podemos hacer con los recursos actuales?

Sofía: Para Q3 sí, para antes no.

Laura: Yo voto B.

Iván: B.

Diego: B.

Sofía: Vale, B entonces. Os mando las pantallas finales el viernes.

Laura: ¿Este viernes el 16?

Sofía: Sí, el 16.

Laura: Genial. Siguiente. Lo del plan Enterprise.

Iván: A ver, esto es complicado. Yo creo que necesitamos un
precio más segmentado pero no tengo análisis comparativo todavía.
Os lo traigo para la semana que viene.

Laura: ¿Puedes para el lunes 19?

Iván: Mejor el miércoles 21.

Laura: Vale, el 21. Pendiente: precios Enterprise. Responsable: Iván.

[ruido]

Sofía: Una cosa. ¿Alguien sabe qué pasó con el bug del export a CSV?
Llevo viendo tickets desde hace dos semanas.

Diego: Ah, sí, está en el sprint pero como prioridad 3.

Sofía: Hay clientes pidiéndolo.

Diego: Vale, lo subo a prioridad 1 esta semana.

Laura: Bien. ¿Algo más? ¿No? Nos vemos la próxima semana.
```

---

## Prompt débil (para mostrar el "antes")

```
Resume esta reunión.
```

## Prompt sólido (para mostrar el "después")

```
Resume esta transcripción de reunión en tres bloques:
1) Decisiones tomadas (con responsable)
2) Próximos pasos (con fecha)
3) Temas pendientes para la próxima reunión.
Usa viñetas. No más de 250 palabras en total.
```
