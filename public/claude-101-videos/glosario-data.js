// Glosario interactivo cruzado del curso Claude 101.
// Cada término: definición concisa + lecciones donde aparece + categoría.

const GLOSSARY = [
  {
    term: 'Anthropic',
    category: 'Empresa',
    definition: 'Empresa fundada en 2021 que crea Claude. Su misión: construir sistemas de IA útiles, honestos e inofensivos.',
    lessons: ['l1-1', 'l9-1']
  },
  {
    term: 'Constitutional AI',
    category: 'Entrenamiento',
    definition: 'Método de entrenamiento de Claude: el modelo se autoevalúa contra una "constitución" escrita de principios y se autorefuerza. Produce respuestas razonadas en lugar de bloqueos rígidos.',
    lessons: ['l9-1']
  },
  {
    term: 'Haiku',
    category: 'Modelos',
    definition: 'El modelo más rápido y barato de la familia Claude. Ideal para tareas ligeras, alta frecuencia o procesamiento en volumen.',
    lessons: ['l1-2', 'l9-1']
  },
  {
    term: 'Sonnet',
    category: 'Modelos',
    definition: 'El modelo equilibrado de Claude. Razonamiento sólido + velocidad razonable. La elección por defecto el 80% del tiempo.',
    lessons: ['l1-2', 'l9-1']
  },
  {
    term: 'Opus',
    category: 'Modelos',
    definition: 'El modelo más potente de Claude. Razonamiento profundo, análisis matizado, problemas multipaso. Más caro y lento — vale la pena cuando la calidad importa.',
    lessons: ['l1-2', 'l9-1']
  },
  {
    term: 'Ventana de contexto',
    category: 'Cómo funciona',
    definition: 'La cantidad de texto que Claude puede tener "en la cabeza" durante una conversación. Enorme (cientos de páginas) pero finita.',
    lessons: ['l1-3']
  },
  {
    term: 'Alucinación',
    category: 'Cómo funciona',
    definition: 'Cuando Claude genera información falsa con tono convincente (cifras inventadas, fuentes inexistentes). No es un bug, es consecuencia de cómo funciona la predicción de texto.',
    lessons: ['l1-3', 'l7-2', 'l7-3']
  },
  {
    term: 'Predicción de texto',
    category: 'Cómo funciona',
    definition: 'Mecanismo central de cómo responde Claude: genera la continuación más probable basándose en patrones aprendidos durante su entrenamiento.',
    lessons: ['l1-3']
  },
  {
    term: 'Fecha de corte',
    category: 'Cómo funciona',
    definition: 'Punto en el tiempo más allá del cual Claude no tiene información. Eventos o datos posteriores requieren búsqueda web o que tú se los proporciones.',
    lessons: ['l7-3', 'l5-2']
  },
  {
    term: 'Claude.ai',
    category: 'Plataformas',
    definition: 'La web pública de Claude. Punto de entrada habitual: navegador, login, chat. Tu cuenta sincroniza con la app móvil y de escritorio.',
    lessons: ['l2-1']
  },
  {
    term: 'API',
    category: 'Plataformas',
    definition: 'Interfaz para desarrolladores que permite integrar Claude en aplicaciones propias. Requiere una clave API y conocimientos de programación.',
    lessons: ['l2-1']
  },
  {
    term: 'Claude Code',
    category: 'Plataformas',
    definition: 'CLI que ejecuta Claude en tu terminal con acceso a tu repositorio. Lee código, propone cambios como diffs, ejecuta comandos. Para desarrolladores.',
    lessons: ['l8-1']
  },
  {
    term: 'Plan Free',
    category: 'Planes',
    definition: 'Plan gratuito de Claude con mensajes limitados y acceso prioritario a Sonnet (no a Opus).',
    lessons: ['l2-1']
  },
  {
    term: 'Plan Pro',
    category: 'Planes',
    definition: 'Plan de pago individual: acceso amplio a Opus, archivos, funciones avanzadas. Para uso diario profesional.',
    lessons: ['l2-1']
  },
  {
    term: 'Plan Team',
    category: 'Planes',
    definition: 'Plan corporativo: cuentas con dominio compartido, workspace separado, billing único. Para equipos.',
    lessons: ['l2-1']
  },
  {
    term: 'Conversación',
    category: 'Organización',
    definition: 'Una sesión de chat con Claude. Independiente por defecto — no comparte memoria con otras salvo que uses Proyectos.',
    lessons: ['l2-3', 'l5-4']
  },
  {
    term: 'Proyecto',
    category: 'Organización',
    definition: 'Espacio donde agrupas conversaciones que comparten archivos, instrucciones y contexto. Útil para clientes recurrentes, productos, asignaturas.',
    lessons: ['l2-3', 'l5-4']
  },
  {
    term: 'Estilo personalizado',
    category: 'Organización',
    definition: 'Define el tono, formato y restricciones que Claude aplica a todas tus conversaciones. Configurado una vez, se aplica siempre.',
    lessons: ['l2-3']
  },
  {
    term: 'Memoria activa',
    category: 'Organización',
    definition: 'Función que va aprendiendo cosas sobre ti entre conversaciones. Útil para preferencias personales. Revisable y borrable.',
    lessons: ['l5-4']
  },
  {
    term: 'Prompt',
    category: 'Prompting',
    definition: 'La instrucción que le das a Claude. Sus 4 componentes mínimos útiles: tarea + contexto + formato + restricciones.',
    lessons: ['l3-1']
  },
  {
    term: 'Tarea',
    category: 'Prompting',
    definition: 'Componente del prompt: la instrucción concreta que quieres que Claude ejecute. Verbo en imperativo + objeto. "Resume el informe".',
    lessons: ['l3-1']
  },
  {
    term: 'Contexto',
    category: 'Prompting',
    definition: 'Información de fondo que Claude necesita para responder bien: quién eres, quién lee, qué pasó antes, qué se sabe. Cambia drásticamente la respuesta.',
    lessons: ['l3-1', 'l3-2']
  },
  {
    term: 'Formato',
    category: 'Prompting',
    definition: 'Componente del prompt: cómo quieres recibir el output. Lista vs prosa, longitud, tono, tabla, código. Sin especificarlo, decide Claude.',
    lessons: ['l3-1']
  },
  {
    term: 'Restricciones',
    category: 'Prompting',
    definition: 'Componente del prompt: qué NO quieres. Sin emojis, sin jerga, máx X palabras, evita tal tema. Lo "no" es tan importante como el "sí".',
    lessons: ['l3-1']
  },
  {
    term: 'Iteración',
    category: 'Prompting',
    definition: 'Refinar la respuesta dando feedback específico ("me gusta el tono, acorta a 3 párrafos"). Más eficiente que pedir "haz otro".',
    lessons: ['l3-3']
  },
  {
    term: 'Chain of Thought (CoT)',
    category: 'Técnicas avanzadas',
    definition: 'Pedirle a Claude que razone paso a paso antes de responder. Mejora notablemente la precisión en lógica, matemáticas y problemas multipaso.',
    lessons: ['l4-1']
  },
  {
    term: 'Few-shot',
    category: 'Técnicas avanzadas',
    definition: 'Dar a Claude 2-3 ejemplos de input → output esperado. Captura el patrón y lo aplica al siguiente input. Ideal para clasificación, formato y tono.',
    lessons: ['l4-2']
  },
  {
    term: 'Etiquetas XML',
    category: 'Técnicas avanzadas',
    definition: 'Usar tags como <contexto>, <ejemplo>, <tarea> dentro del prompt para separar bloques. Mejora la precisión en prompts complejos con múltiples partes.',
    lessons: ['l4-3', 'l9-2']
  },
  {
    term: 'Rol / Persona',
    category: 'Técnicas avanzadas',
    definition: 'Asignar a Claude un rol específico ("Actúa como editor senior de revista cultural"). Calibra tono, vocabulario y criterio implícitos sin tener que enumerarlos.',
    lessons: ['l4-4']
  },
  {
    term: 'Artifact',
    category: 'Capacidades',
    definition: 'Output que aparece en un panel lateral editable e iterable. Para código, documentos largos o mini-apps. Permite refinar sin reescribir todo en cada mensaje.',
    lessons: ['l5-1']
  },
  {
    term: 'Búsqueda web',
    category: 'Capacidades',
    definition: 'Capacidad de Claude para consultar la web en tiempo real. Vale para eventos recientes y datos cambiantes; no para conocimiento estable.',
    lessons: ['l5-2']
  },
  {
    term: 'Code Interpreter',
    category: 'Capacidades',
    definition: 'Cuando Claude ejecuta código real (Python normalmente) en un entorno seguro para hacer cálculos, análisis de CSVs, etc. Da resultados precisos, no estimaciones.',
    lessons: ['l5-3', 'l6-3', 'l7-3']
  },
  {
    term: 'Markdown',
    category: 'Input estructurado',
    definition: 'Lenguaje ligero de formateo (headers con #, listas con -, código en bloques ```). Estructurar tu prompt con markdown mejora la comprensión de Claude.',
    lessons: ['l9-2']
  },
  {
    term: 'Skills',
    category: 'Avanzado',
    definition: 'Carpetas con SKILL.md + archivos auxiliares que definen una capacidad. Claude las carga automáticamente cuando detecta que las necesita. Empaquetan flujos reutilizables.',
    lessons: ['l9-3']
  },
  {
    term: 'Agente',
    category: 'Avanzado',
    definition: 'Sistema que planifica → ejecuta tools → evalúa → itera hasta completar un objetivo. Un prompt es Q&A; un agente trabaja.',
    lessons: ['l9-4']
  },
  {
    term: 'Claude Agent SDK',
    category: 'Avanzado',
    definition: 'Librería en Python o TypeScript para construir agentes en pocas líneas. Defines tools y system prompt, y el SDK gestiona el bucle.',
    lessons: ['l9-4']
  },
  {
    term: 'MCP (Model Context Protocol)',
    category: 'Avanzado',
    definition: 'Estándar abierto que conecta Claude (y otros modelos) a herramientas y datos externos. Un servidor MCP es usable por cualquier cliente compatible.',
    lessons: ['l8-2', 'l9-5']
  },
  {
    term: 'Conector MCP',
    category: 'Avanzado',
    definition: 'Servidor MCP específico para una app (Drive, GitHub, Notion, Slack). Permite que Claude opere sobre los datos de esa app sin reescribir nada.',
    lessons: ['l8-2', 'l9-5']
  },
  {
    term: 'Anonimización',
    category: 'Privacidad',
    definition: 'Sustituir datos personales por IDs o categorías genéricas antes de compartirlos con Claude. Cumple con la minimización del RGPD.',
    lessons: ['l7-1']
  },
  {
    term: 'Opt-out de entrenamiento',
    category: 'Privacidad',
    definition: 'Configuración para que tus conversaciones no se usen para mejorar el modelo. Recomendado en contextos con datos sensibles o de terceros.',
    lessons: ['l2-4', 'l7-1']
  },
  {
    term: 'RGPD',
    category: 'Privacidad',
    definition: 'Reglamento europeo de protección de datos. Si manejas datos de terceros (clientes, empleados, pacientes), te obliga a minimizar y proteger.',
    lessons: ['l7-1']
  },
  {
    term: 'Crítica adversarial',
    category: 'Creatividad',
    definition: 'Técnica para validar ideas: pedirle a Claude que critique tu propuesta desde el rol de un escéptico hostil. Encuentra debilidades antes que el mercado.',
    lessons: ['l6-4']
  },
  {
    term: 'Brainstorming divergente/convergente',
    category: 'Creatividad',
    definition: 'Pedir muchas ideas primero (divergir), luego converger eligiendo y refinando. Más eficaz que pedir "las 3 mejores ideas".',
    lessons: ['l6-4']
  },
  {
    term: 'Refactor',
    category: 'Programación',
    definition: 'Reescribir código existente para mejorar legibilidad, estructura o rendimiento sin cambiar su funcionalidad. Tarea donde Claude brilla.',
    lessons: ['l6-2']
  },
  {
    term: 'Debugging',
    category: 'Programación',
    definition: 'Identificar y arreglar errores en código. Para que Claude ayude bien: dale código + error + lo que intentaste + contexto del proyecto.',
    lessons: ['l6-2']
  },
  {
    term: 'Análisis temático',
    category: 'Análisis',
    definition: 'Extraer temas recurrentes de un conjunto de textos (reseñas, encuestas, tickets). Claude lo hace bien si le das la pregunta de negocio.',
    lessons: ['l6-3']
  },
  {
    term: 'Pensamiento crítico',
    category: 'Buenas prácticas',
    definition: 'Verificar lo que Claude dice cuando hay decisiones importantes basadas en datos factuales. Cifras, fechas, nombres propios y "fuentes citadas" son las señales de alerta.',
    lessons: ['l7-2']
  },
  {
    term: 'Transparencia',
    category: 'Ética',
    definition: 'Declarar el uso de IA cuando publicas algo significativo. No siempre obligatorio, pero gana confianza en contextos profesionales.',
    lessons: ['l7-4']
  },
  {
    term: 'Proyecto final',
    category: 'Práctica',
    definition: 'Aplicar lo aprendido a una tarea tuya real, repetitiva, que te consume tiempo. Pequeño + hecho > grande + soñado.',
    lessons: ['l8-4']
  }
];

if (typeof module !== 'undefined' && module.exports) module.exports = GLOSSARY;
