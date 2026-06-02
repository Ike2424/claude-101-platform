// Resumen ejecutivo de cada módulo para generar PDF descargable.
// Estructura: título, takeaway en 1 línea, 5 conceptos clave (qué, por qué),
// cheatsheet práctico (qué hacer, qué evitar), y 1 ejemplo final.

const MODULE_PDFS = {
1: {
  title: 'Bienvenida y fundamentos',
  takeaway: 'Claude es un asistente de IA de Anthropic con tres principios — útil, honesto e inofensivo — y una familia de modelos para distintas tareas.',
  concepts: [
    { name: 'Qué es Claude', what: 'Asistente conversacional creado por Anthropic, fundada en 2021.', why: 'Saber con qué tipo de herramienta trabajas calibra expectativas y casos de uso.' },
    { name: 'Constitutional AI', what: 'Método de entrenamiento donde el modelo se autoevalúa contra principios escritos.', why: 'Explica por qué Claude razona en vez de bloquear y matiza en lugar de evadir.' },
    { name: 'La familia de modelos', what: 'Haiku (rápido), Sonnet (equilibrado), Opus (potente).', why: 'Elegir bien optimiza coste, velocidad y calidad. Regla: empieza por Sonnet.' },
    { name: 'Predicción de texto', what: 'Claude genera la continuación más probable basada en patrones aprendidos — no consulta base de datos.', why: 'Por eso puede alucinar y por eso el contexto importa tanto.' },
    { name: 'Ventana de contexto', what: 'Cantidad de texto que Claude puede tener "en mente" en una conversación.', why: 'Enorme pero finita. Conversaciones muy largas pierden el principio.' }
  ],
  cheatsheet: {
    do: [
      'Empieza por Sonnet por defecto',
      'Sube a Opus solo cuando la tarea pide razonamiento profundo',
      'Baja a Haiku para tareas simples a volumen',
      'Verifica datos factuales relevantes (cifras, fechas, fuentes)',
      'Dale contexto sobre quién eres y qué buscas'
    ],
    avoid: [
      'Usar Opus para todo "por si acaso" — caro y lento',
      'Tratar a Claude como buscador para info reciente sin búsqueda web',
      'Asumir que el tono seguro = veracidad',
      'Confiar en cifras precisas con decimales sin verificar',
      'Compartir datos sensibles de terceros sin necesidad'
    ]
  },
  example: 'Para clasificar 500 emails: Haiku. Para redactar el plan estratégico anual: Opus. Para el email del día a día: Sonnet.'
},
2: {
  title: 'Primeros pasos',
  takeaway: 'Cuatro vías de acceso a Claude (web, móvil, escritorio, API), una sola cuenta, y tres niveles de organización (conversaciones, proyectos, estilos).',
  concepts: [
    { name: 'Cuatro vías de acceso', what: 'Web (claude.ai), app móvil, app escritorio, API + Claude Code.', why: 'Misma cuenta sincronizada. Elige según contexto: navegador para empezar, escritorio para uso intensivo, API para dev.' },
    { name: 'Planes', what: 'Free (limitado), Pro (individual amplio), Team (corporativo).', why: 'Free para probar, Pro para uso diario profesional, Team cuando colaboras con equipo.' },
    { name: 'Conversación', what: 'Una sesión de chat independiente por defecto.', why: 'No comparte memoria con otras salvo que actives memoria o uses Proyectos.' },
    { name: 'Proyecto', what: 'Espacio que agrupa conversaciones que comparten archivos e instrucciones.', why: 'Ideal para clientes recurrentes, productos, o trabajo del mismo tema durante semanas.' },
    { name: 'Estilo personalizado', what: 'Configuración de tono, formato y restricciones aplicada a tus conversaciones.', why: 'Defines una vez "cómo quieres respuestas" y se aplica siempre. Ahorras repetir.' }
  ],
  cheatsheet: {
    do: [
      'Rellena tu perfil con rol, sector y preferencias',
      'Usa Proyectos para trabajo recurrente con archivos',
      'Crea Estilos para tu tono habitual',
      'Cambia de modelo en mitad de conversación si la tarea evoluciona',
      'Revisa el opt-out de entrenamiento si manejas datos sensibles'
    ],
    avoid: [
      'Tener "una conversación gigante para todo"',
      'Repetir tu tono y formato en cada prompt',
      'Subir el mismo PDF a cada conversación nueva',
      'Compartir datos sensibles en el perfil personal',
      'Asumir que Claude recuerda chats anteriores por defecto'
    ]
  },
  example: 'Cliente con 5 briefs y 20 conversaciones del mismo tema → un Proyecto. "Respuestas siempre en bullets, tono cercano, sin emojis" → un Estilo.'
},
3: {
  title: 'El arte del prompt',
  takeaway: 'Un buen prompt tiene 4 componentes (tarea, contexto, formato, restricciones), itera con feedback específico, y evita errores comunes (ambigüedad, multitarea, doble negación).',
  concepts: [
    { name: 'Anatomía del prompt', what: 'Cuatro partes mínimas útiles: Tarea + Contexto + Formato + Restricciones.', why: 'Cubrir las cuatro reduce el 80% de respuestas "no es lo que quería".' },
    { name: 'Contexto', what: 'Información sobre quién eres, quién lee, qué pasó antes, qué se sabe.', why: 'Sin contexto, Claude inventa el contexto que considera más probable. Una línea cambia la respuesta.' },
    { name: 'Especificidad', what: 'Restricciones concretas vs adjetivos vagos.', why: '"Máximo 100 palabras en 3 bullets" gana siempre a "que sea breve".' },
    { name: 'Iteración productiva', what: 'Dar feedback específico ("acorta, mantén el tono") en lugar de "haz otro".', why: 'Más eficiente que reset. Claude mantiene contexto y refina lo concreto.' },
    { name: 'Errores comunes', what: 'Ambigüedad, multitarea, doble negación, falta de contexto.', why: 'Conocerlos te ahorra iteraciones y mejora calidad sin necesidad de técnicas avanzadas.' }
  ],
  cheatsheet: {
    do: [
      'Especifica audiencia ("para mi CEO", "para clientes B2B")',
      'Da contexto de la situación en 1-2 líneas',
      'Pon restricciones numéricas ("max 100 palabras")',
      'Itera con feedback específico ("acorta el último párrafo")',
      'Una tarea por prompt — encadénalas si son varias'
    ],
    avoid: [
      'Adjetivos vagos como "breve", "profesional", "bueno"',
      'Doble negación ("no olvides no hacer X")',
      'Mezclar 5 tareas en el mismo prompt',
      'Pedir "haz otro" en lugar de feedback específico',
      'Empezar sin pensar el prompt — 5 min pensando = 30 min ahorrados'
    ]
  },
  example: '"Como CMO de pyme de Granada que vende sostenibilidad, redacta email a clientes inactivos para reactivar relación. Tono cercano profesional, máx 120 palabras, sin emojis."'
},
4: {
  title: 'Técnicas avanzadas',
  takeaway: 'Cuatro técnicas multiplican lo aprendido: Chain of Thought, Few-shot, etiquetas XML y roles específicos. Cada una resuelve un problema concreto.',
  concepts: [
    { name: 'Chain of Thought (CoT)', what: 'Pedir a Claude que razone paso a paso antes de responder.', why: 'Mejora notablemente la precisión en lógica, mates y problemas multipaso. No usar en creativo.' },
    { name: 'Few-shot', what: 'Dar 2-3 ejemplos de input → output esperado.', why: 'Calibra tono, formato y criterio mejor que mil adjetivos. Ideal para clasificación y consistencia.' },
    { name: 'Etiquetas XML', what: 'Tags como <contexto>, <ejemplo>, <tarea> que separan bloques.', why: 'En prompts complejos con múltiples partes, mejora drásticamente la precisión.' },
    { name: 'Roles / Personas', what: 'Asignar rol específico ("Actúa como editor senior").', why: 'Calibra criterio, vocabulario y prioridades implícitos sin enumerarlos.' },
    { name: 'Restricciones explícitas', what: 'Decir qué NO quieres ("sin emojis, sin jerga").', why: 'Tan importante como qué sí. Te ahorra iteraciones.' }
  ],
  cheatsheet: {
    do: [
      'CoT para lógica, mates, análisis multicriterio',
      'Few-shot cuando necesitas consistencia entre muchas peticiones',
      'XML para prompts >200 líneas con bloques diferenciados',
      'Rol muy específico ("ingeniero senior con 10 años en Python prod")',
      'Restricciones explícitas en lo que NO quieres'
    ],
    avoid: [
      'CoT en creativo (vuelve mecánico el flujo)',
      'Few-shot con 1 solo ejemplo (no captura patrón)',
      'XML en prompts cortos (añade ruido)',
      'Roles vagos como "experto" (no calibra nada)',
      'Combinar muchas técnicas a la vez sin necesidad'
    ]
  },
  example: 'Para clasificar 200 emails: few-shot con 1 ejemplo de cada categoría. Para razonar pros/contras de 3 estrategias: CoT explícito. Para refactor de módulo grande: rol "ingeniero senior + restricciones de estilo".'
},
5: {
  title: 'Capacidades y herramientas',
  takeaway: 'Más allá del chat: Artifacts para iterar documentos, búsqueda web para actualidad, archivos descargables (Excel/Word/PDF) y memoria entre conversaciones.',
  concepts: [
    { name: 'Artifacts', what: 'Output que aparece en panel lateral editable e iterable.', why: 'Permite refinar el mismo documento/código sin reescribir todo en cada mensaje.' },
    { name: 'Búsqueda web', what: 'Capacidad de consultar la web en tiempo real.', why: 'Vale para info posterior a la fecha de corte o datos cambiantes. No para conocimiento estable.' },
    { name: 'Creación de archivos', what: 'Claude genera XLSX, DOCX, PDF, PPTX con fórmulas reales.', why: 'Cuando el output final es un archivo entregable, pídelo así en lugar de pegarlo en chat.' },
    { name: 'Code Interpreter', what: 'Ejecución real de código (Python) en entorno seguro.', why: 'Cálculos precisos, análisis de CSVs, agregaciones. No estimaciones.' },
    { name: 'Memoria', what: 'Conversaciones independientes por defecto; Proyectos y memoria activa para persistencia.', why: 'Saber cuándo el contexto persiste y cuándo no evita malentendidos.' }
  ],
  cheatsheet: {
    do: [
      'Artifacts para documentos/código que vas a iterar',
      'Búsqueda web solo para eventos recientes o datos cambiantes',
      'Pide XLSX si el output será una hoja de cálculo',
      'Sube CSVs/PDFs como adjuntos (no copies texto)',
      'Usa Proyectos para mantener contexto entre conversaciones'
    ],
    avoid: [
      'Artifacts para respuestas cortas (no aporta)',
      'Búsqueda web para conocimiento estable (lento e innecesario)',
      'Copiar 5000 filas de CSV como texto al chat',
      'Pedir PDF cerrado cuando vas a iterar (mejor Word)',
      'Asumir que recuerda chats anteriores sin Proyecto/memoria'
    ]
  },
  example: 'Análisis de ventas trimestral → adjunta CSV, pide análisis temático + Excel resultante + Word con el análisis textual. Iterables ambos.'
},
6: {
  title: 'Casos de uso prácticos',
  takeaway: 'Cuatro áreas donde Claude transforma tu día: escritura profesional, programación, análisis de datos, brainstorming creativo. Mismo patrón: contexto + ejemplos > adjetivos.',
  concepts: [
    { name: 'Escritura profesional', what: 'Emails difíciles, posts, propuestas, resúmenes ejecutivos.', why: 'Da contexto del lector y objetivo. Para imitar tu voz: 2-3 textos tuyos como few-shot.' },
    { name: 'Programación', what: 'Debug, refactor, explicación de código heredado.', why: 'Dale código + error + lo que intentaste + contexto del proyecto. Pide diff antes de aplicar.' },
    { name: 'Análisis de datos', what: 'CSVs, PDFs largos, logs. Tendencias, segmentación, extracción.', why: 'Adjunta el archivo + da pregunta de negocio concreta. Code Interpreter para cómputo preciso.' },
    { name: 'Creatividad', what: 'Brainstorming, naming, storytelling, validación adversarial.', why: 'Pide 20 ideas (no 3), cambia de perspectiva, crítica desde rol escéptico.' },
    { name: 'Imitar tu voz', what: 'Few-shot con ejemplos tuyos.', why: '"Como tú" es ambiguo. 3 textos tuyos capturan tu voz con precisión.' }
  ],
  cheatsheet: {
    do: [
      'Para escritura: contexto del lector + objetivo + ejemplos',
      'Para código: stack + contexto del proyecto + tests existentes',
      'Para análisis: pregunta de negocio concreta',
      'Para creatividad: pedir cantidad (20), luego converger',
      'Crítica adversarial para validar ideas antes de publicar'
    ],
    avoid: [
      'Pedir "tono profesional" sin definir qué significa',
      'Pegar código sin contexto del proyecto',
      'Pedir "analiza este CSV" sin pregunta de negocio',
      'Pedir 3 ideas brillantes (mejor 20 y converger)',
      'Validar tu idea con "¿qué te parece?" (será amable y poco útil)'
    ]
  },
  example: 'Brainstorm naming: "25 nombres para cafetería en Granada, concepto especialidad de origen, target millennial profesional urbano, tono moderno-cálido, evitando clichés como Café/El Mirador."'
},
7: {
  title: 'Buenas prácticas y límites',
  takeaway: 'Usar Claude como profesional: anonimizar datos de terceros, verificar lo factual relevante, conocer límites (fecha de corte, alucinaciones, contexto finito) y declarar uso cuando proceda.',
  concepts: [
    { name: 'Privacidad', what: 'No compartir datos sensibles de terceros sin necesidad ni anonimización.', why: 'Cumplimiento RGPD + buenas prácticas. Minimiza siempre.' },
    { name: 'Verificación', what: 'Confirmar datos factuales relevantes externamente.', why: 'Cifras precisas, fechas, nombres propios y "fuentes citadas" son zonas de alta alucinación.' },
    { name: 'Fecha de corte', what: 'Punto en el tiempo más allá del cual Claude no tiene datos.', why: 'Para info reciente activa búsqueda web o dale el contexto tú.' },
    { name: 'Alucinaciones', what: 'Información falsa con tono convincente.', why: 'No es bug, es cómo funciona predicción. Verifica lo que importe.' },
    { name: 'Uso ético', what: 'Transparencia + criterio humano + respeto a otros.', why: 'Tú firmas el output. Eres responsable. La herramienta no asume responsabilidad.' }
  ],
  cheatsheet: {
    do: [
      'Anonimiza datos personales de terceros antes de subirlos',
      'Activa opt-out de entrenamiento en contextos sensibles',
      'Verifica cifras precisas, fechas y citas externamente',
      'Pide CoT explícito en problemas de lógica/mates',
      'Declara uso de IA en publicaciones significativas'
    ],
    avoid: [
      'Subir DNI, contraseñas, datos médicos, código propietario con secretos',
      'Confiar en cifras precisas con decimales sin verificar',
      'Aceptar fuentes citadas sin búsqueda externa',
      'Usar Claude para decisiones médicas/financieras sin profesional',
      'Asumir que el tono seguro implica precisión'
    ]
  },
  example: 'Análisis de base de clientes → sustituye nombres y emails por IDs si solo necesitas patrones. Para informes con cifras concretas: pídele fuente y verifica las 3-4 más importantes.'
},
8: {
  title: 'Siguiente nivel',
  takeaway: 'Más allá del chat: Claude Code (dev), conectores MCP (entre apps), recursos para seguir aprendiendo, y un proyecto final aplicado a una tarea tuya real.',
  concepts: [
    { name: 'Claude Code', what: 'CLI que ejecuta Claude en tu terminal con acceso a tu repo.', why: 'Lee código, propone diffs, ejecuta comandos. Cambia la velocidad de programar.' },
    { name: 'MCP', what: 'Estándar abierto para conectar Claude a herramientas y datos.', why: 'Cualquier servidor MCP es usable por cualquier cliente compatible. Drive, GitHub, Notion, Slack.' },
    { name: 'Recursos', what: 'Docs oficiales, comunidades, newsletters.', why: 'Docs como mapa, comunidades para casos reales, newsletters para curaduría.' },
    { name: 'Proyecto final', what: 'Aplicar lo aprendido a una tarea tuya real, repetitiva.', why: 'Práctica deliberada > leer más. Pequeño + hecho > grande + soñado.' },
    { name: 'Práctica continua', what: 'Uso diario en cosas reales.', why: 'Las habilidades vienen del uso, no de leer. Los recursos son apoyo, no atajo.' }
  ],
  cheatsheet: {
    do: [
      'Claude Code si programas a diario',
      'Conectores MCP para apps donde viven tus datos',
      'Identifica una tarea tuya repetitiva como proyecto final',
      'Empieza pequeño + termina + itera',
      'Revisa docs.claude.com cuando atasques'
    ],
    avoid: [
      'Empezar proyecto final ambicioso "para impresionar"',
      'Solo leer sobre Claude sin aplicar',
      'Conectar MCPs sin revisar permisos',
      'Esperar al "curso avanzado" en lugar de practicar',
      'Subestimar tareas repetitivas como candidatas'
    ]
  },
  example: 'Proyecto final pequeño y útil: plantilla + prompt para escribir tu resumen ejecutivo mensual con tono y estructura de tu empresa. Te ahorra 1-2h/semana.'
},
9: {
  title: 'Desarrollo avanzado (BONUS)',
  takeaway: 'Cómo se construye con Claude por dentro: Constitutional AI, markdown semántico, Skills para empaquetar capacidades, agentes para automatizar bucles, y MCP para conectar todo.',
  concepts: [
    { name: 'Constitutional AI', what: 'Método de entrenamiento basado en autoevaluación contra principios escritos.', why: 'Explica el "carácter" de Claude: razona en lugar de bloquear, matiza en lugar de inventar.' },
    { name: 'Markdown semántico', what: 'Estructurar prompts con headers, listas y bloques de código.', why: 'Claude entrenado con millones de docs en markdown — lo procesa como estructura jerárquica.' },
    { name: 'Skills', what: 'Carpetas con SKILL.md + auxiliares que definen una capacidad reutilizable.', why: 'Claude las activa automáticamente cuando detecta intención. Empaqueta flujos.' },
    { name: 'Agentes', what: 'Sistemas con bucle: planifica → ejecuta tools → evalúa → itera.', why: 'Un prompt es Q&A; un agente trabaja. Claude Agent SDK los construye en ~50 líneas.' },
    { name: 'MCP', what: 'Protocolo abierto que estandariza conexión entre modelos y herramientas externas.', why: 'Servidor expone tools, cliente los consume. Reusable entre apps.' }
  ],
  cheatsheet: {
    do: [
      'Markdown estructurado en prompts >200 líneas',
      'Skills para flujos que repites con estructura consistente',
      'Agente cuando hay bucle (planificar → ejecutar → evaluar)',
      'MCP server propio para datos internos de tu organización',
      'Empezar pequeño: una tarea repetitiva tuya'
    ],
    avoid: [
      'Construir agentes ambiciosos antes de tener prompts buenos',
      'Skills para tareas únicas (no repetitivas)',
      'Agentes con acciones financieras sin guardrails fuertes',
      'Conectar MCPs sin revisar permisos granulares',
      'Esperar al "framework definitivo" en lugar de iterar pequeño'
    ]
  },
  example: 'Skill personal para reportes mensuales (SKILL.md + plantilla.docx + ejemplos). Cuando le digas "haz el reporte de junio", Claude carga la skill y aplica plantilla con tu tono.'
}
};

if (typeof module !== 'undefined' && module.exports) module.exports = MODULE_PDFS;
