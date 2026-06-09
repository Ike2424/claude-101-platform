#!/usr/bin/env python3
"""
Claude 101 — HTML Lesson Generator
Generates 38 professional interactive HTML slides for the Claude 101 course.
Each lesson is self-contained with CSS, JS, and all assets inline.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple

# ============================================================================
# LESSON DATA - All 38 lessons organized by module
# ============================================================================

LESSONS_DATA = {
    "M1": {
        "title": "Bienvenida y fundamentos",
        "description": "Descubre qué es Claude, cómo funciona y qué lo diferencia",
        "color_primary": "#2563EB",
        "color_secondary": "#F97316",
        "icon": "🚀",
        "lessons": [
            {
                "id": "L1-1",
                "title": "¿Qué es Claude?",
                "concepts": [
                    ("Claude es un asistente de IA", "Creado por Anthropic en 2021 con enfoque en ser útil, honesto e inofensivo"),
                    ("No es un buscador", "No consulta internet en tiempo real. Genera respuestas basadas en patrones aprendidos"),
                    ("Funciona mejor con claridad", "Quanto mejor le expliques qué necesitas, mejor es su respuesta"),
                ],
                "quiz_questions": [
                    ("¿Quién creó Claude?", ["Anthropic", "OpenAI", "Google"], 0),
                    ("¿Es Claude un buscador?", ["No", "Sí", "Parcialmente"], 0),
                    ("¿Qué es lo más importante para obtener buenas respuestas?", ["Ser claro en el prompt", "Usar muchas palabras", "Hacer preguntas en inglés"], 0),
                ]
            },
            {
                "id": "L1-2",
                "title": "La familia de modelos",
                "concepts": [
                    ("Haiku", "Rápido y eficiente. Ideal para tareas sencillas y respuestas instantáneas"),
                    ("Sonnet", "Equilibrio perfecto. Razonamiento sólido con velocidad aceptable. El que usarás el 80% del tiempo"),
                    ("Opus", "Más potente. Para problemas complejos, análisis profundo y escritura matizada"),
                ],
                "quiz_questions": [
                    ("¿Cuál es el modelo más rápido?", ["Haiku", "Sonnet", "Opus"], 0),
                    ("¿Cuál es el equilibrio recomendado?", ["Haiku", "Sonnet", "Opus"], 1),
                    ("¿Para qué sirve Opus?", ["Tareas ligeras", "Problemas complejos", "Velocidad máxima"], 1),
                ]
            },
            {
                "id": "L1-3",
                "title": "Cómo razona Claude",
                "concepts": [
                    ("Genera probabilidades", "Predice el texto más probable basado en patrones del entrenamiento"),
                    ("Puede alucinar", "A veces está tan seguro que suena falso. Siempre verifica datos críticos"),
                    ("Puede pensar paso a paso", "En problemas complejos dedica tiempo a razonar antes de responder"),
                ],
                "quiz_questions": [
                    ("¿Cómo genera Claude sus respuestas?", ["Consultando una base de datos", "Prediciendo probabilidades", "Buscando en internet"], 1),
                    ("¿Qué es 'alucinar' en IA?", ["Error de conexión", "Respuesta segura pero falsa", "Falta de contexto"], 1),
                    ("¿En qué es especialmente bueno Claude?", ["Búsquedas rápidas", "Razonamiento paso a paso", "Memoria a largo plazo"], 1),
                ]
            },
            {
                "id": "L1-4",
                "title": "Diferencias con otros asistentes",
                "concepts": [
                    ("Estilo natural", "Texto más natural y menos formulaico que otros asistentes"),
                    ("Honestidad calibrada", "Reconoce sus límites en lugar de afirmar con falsa seguridad"),
                    ("Contextos largos", "Sobresale en documentos extensos manteniendo coherencia perfecta"),
                ],
                "quiz_questions": [
                    ("¿Cuál es una ventaja de Claude sobre otros asistentes?", ["Es gratis", "Estilo de escritura más natural", "Tiene conexión a internet"], 1),
                    ("¿Cómo maneja Claude los límites?", ["Los ignora", "Reconoce honestamente qué no puede hacer", "Intenta siempre"], 1),
                    ("¿En qué destacan especialmente los contextos largos de Claude?", ["Velocidad", "Coherencia en documentos extensos", "Privacidad"], 1),
                ]
            },
        ]
    },
    "M2": {
        "title": "Primeros pasos",
        "description": "Accede a Claude, configura tu cuenta y domina la interfaz",
        "color_primary": "#10B981",
        "color_secondary": "#FBBF24",
        "icon": "⚙️",
        "lessons": [
            {
                "id": "L2-1",
                "title": "Cómo acceder a Claude",
                "concepts": [
                    ("Web: claude.ai", "La opción más simple. Solo necesitas un navegador y login"),
                    ("Apps móviles", "iOS y Android con sincronización automática. Perfecto para estar en movimiento"),
                    ("App de escritorio", "Mac y Windows. Atajos de teclado y acceso rápido desde cualquier parte"),
                ],
                "quiz_questions": [
                    ("¿Cuál es la forma más simple de acceder a Claude?", ["App de escritorio", "claude.ai en navegador", "Terminal"], 1),
                    ("¿En cuántas plataformas puedes usar Claude?", ["2", "3", "4"], 2),
                    ("¿Cuál es la ventaja de la app de escritorio?", ["Es más barata", "Tiene atajos de teclado", "Funciona offline"], 1),
                ]
            },
            {
                "id": "L2-2",
                "title": "La interfaz explicada",
                "concepts": [
                    ("Caja de mensaje", "Escribe aquí. Puedes adjuntar imágenes, PDFs, código y más"),
                    ("Selector de modelo", "Elige entre Haiku, Sonnet u Opus según tu necesidad"),
                    ("Historial", "Todas tus conversaciones guardadas automáticamente. Accesible en cualquier momento"),
                ],
                "quiz_questions": [
                    ("¿Qué tipos de archivos puedes adjuntar?", ["Solo texto", "Imágenes, PDFs, código", "Cualquier cosa"], 1),
                    ("¿Dónde cambias de modelo?", ["Panel izquierdo", "Selector en la caja de mensaje", "Configuración"], 1),
                    ("¿Se guardan automáticamente tus conversaciones?", ["No", "Solo si las marcas", "Sí, siempre"], 2),
                ]
            },
            {
                "id": "L2-3",
                "title": "Conversaciones, proyectos y estilos",
                "concepts": [
                    ("Conversaciones", "Chats independientes. Cada uno es un contexto nuevo sin memoria de otros"),
                    ("Proyectos", "Agrupa conversaciones relacionadas con context compartido e instrucciones"),
                    ("Estilos de respuesta", "Configura cómo Claude habla: formal, casual, conciso, detallado"),
                ],
                "quiz_questions": [
                    ("¿Qué es un Proyecto en Claude?", ["Una conversación individual", "Grupo de chats con contexto compartido", "Un archivo guardado"], 1),
                    ("¿Recuerdan las conversaciones el contexto entre sí?", ["Sí, siempre", "No por defecto", "Solo en proyectos"], 2),
                    ("¿Para qué sirven los estilos de respuesta?", ["Cambiar el idioma", "Configurar tono y nivel de detalle", "Filtrar contenido"], 1),
                ]
            },
            {
                "id": "L2-4",
                "title": "Planes y configuración",
                "concepts": [
                    ("Plan Gratuito", "Límites de uso pero acceso a todas las funciones. Perfecto para probar"),
                    ("Plan Pro", "Uso ilimitado, acceso prioritario, más funciones. Ideal para uso diario"),
                    ("Team & Enterprise", "Para equipos con seguridad y controles avanzados"),
                ],
                "quiz_questions": [
                    ("¿Qué plan es mejor si usas Claude +3 veces al día?", ["Gratuito", "Pro", "Team"], 1),
                    ("¿El plan gratuito tiene acceso a todas las funciones?", ["Sí, pero con límites", "No, está muy restringido", "Solo a Haiku"], 0),
                    ("¿Cuál es la ventaja principal de Pro?", ["Es más barato", "Uso ilimitado y prioritario", "Funciones exclusivas"], 1),
                ]
            },
        ]
    },
    "M3": {
        "title": "El arte del prompt",
        "description": "Aprende a escribir prompts que obtengan exactamente lo que quieres",
        "color_primary": "#A855F7",
        "color_secondary": "#EC4899",
        "icon": "✨",
        "lessons": [
            {
                "id": "L3-1",
                "title": "Estructura de un buen prompt",
                "concepts": [
                    ("Claridad", "Sé explícito sobre qué necesitas. Evita ambigüedades"),
                    ("Contexto", "Proporciona el máximo contexto relevante. Más contexto = mejores respuestas"),
                    ("Formato esperado", "Especifica cómo quieres la respuesta: JSON, markdown, tabla, código, etc"),
                ],
                "quiz_questions": [
                    ("¿Cuál es el factor más importante en un prompt?", ["Longitud", "Claridad", "Idioma"], 1),
                    ("¿Cómo mejora más el contexto las respuestas?", ["Haciendo prompts más largos", "Siendo más específico", "Usando palabras clave"], 1),
                    ("¿Debería especificar el formato de salida?", ["No, Claude lo adivina", "Sí, siempre ayuda", "Solo en código"], 1),
                ]
            },
            {
                "id": "L3-2",
                "title": "Few-shot prompting",
                "concepts": [
                    ("Mostrar ejemplos", "Proporciona 2-3 ejemplos de lo que esperas. Claude aprenderá el patrón"),
                    ("Consistencia", "Los ejemplos deben ser consistentes con tu caso real"),
                    ("Evitar sobreentrenamiento", "Más ejemplos no siempre es mejor. 2-3 bien escogidos son suficientes"),
                ],
                "quiz_questions": [
                    ("¿Cuántos ejemplos es ideal en few-shot?", ["1", "2-3", "10+"], 1),
                    ("¿Para qué sirven los ejemplos?", ["Llenar espacio", "Mostrar el patrón esperado", "Limitar respuestas"], 1),
                    ("¿Qué pasa si los ejemplos no son consistentes?", ["Nada", "Claude se confunde", "Mejora las respuestas"], 1),
                ]
            },
            {
                "id": "L3-3",
                "title": "Chain-of-thought",
                "concepts": [
                    ("Pensar paso a paso", "Pide a Claude que muestre su razonamiento antes de la respuesta final"),
                    ("Mejora la precisión", "Especialmente en problemas complejos como matemáticas y lógica"),
                    ("Debugging", "Puedes ver dónde Claude se equivoca en su razonamiento"),
                ],
                "quiz_questions": [
                    ("¿Qué es chain-of-thought?", ["Una conversación larga", "Mostrar el razonamiento paso a paso", "Múltiples intentos"], 1),
                    ("¿En qué tipo de problemas funciona mejor?", ["Preguntas simples", "Problemas complejos con lógica", "Búsquedas"], 1),
                    ("¿Cuál es la ventaja de ver el razonamiento?", ["Entretener", "Debuggear errores", "Nada especial"], 1),
                ]
            },
            {
                "id": "L3-4",
                "title": "System prompts e instrucciones",
                "concepts": [
                    ("System prompt", "Instrucciones permanentes que definen la personalidad de Claude en esa conversación"),
                    ("Nivel de detalle", "Especifica en el system prompt cuán detalladas deben ser las respuestas"),
                    ("Rol play", "Puedes definir un rol: 'Actúa como experto en X' en el system prompt"),
                ],
                "quiz_questions": [
                    ("¿Qué es un system prompt?", ["Un error del sistema", "Instrucciones permanentes para la conversación", "Una pregunta inicial"], 1),
                    ("¿Cuándo se aplica el system prompt?", ["Solo en el primer mensaje", "En todos los mensajes", "Nunca"], 1),
                    ("¿Puedes cambiar la personalidad de Claude con system prompts?", ["No", "Sí, mediante instrucciones claras", "Solo en API"], 1),
                ]
            },
        ]
    },
    "M4": {
        "title": "Técnicas avanzadas de prompting",
        "description": "Domina patrones complejos para extraer máximo valor",
        "color_primary": "#4F46E5",
        "color_secondary": "#06B6D4",
        "icon": "🎯",
        "lessons": [
            {
                "id": "L4-1",
                "title": "Temperatura y configuración",
                "concepts": [
                    ("Temperatura 0", "Determinista. Misma entrada = misma salida. Para tareas críticas"),
                    ("Temperatura 1+", "Creativo. Más variación. Ideal para brainstorming y contenido"),
                    ("Top P", "Controla diversidad de tokens. Deja que Claude escoja entre opciones probables"),
                ],
                "quiz_questions": [
                    ("¿Cuándo usar temperatura 0?", ["Siempre", "En tareas críticas donde consistencia importa", "Nunca"], 1),
                    ("¿Para qué es mejor temperatura alta?", ["Análisis de datos", "Brainstorming creativo", "Código"], 1),
                    ("¿Qué es Top P?", ["Precisión", "Diversidad de respuestas", "Velocidad"], 1),
                ]
            },
            {
                "id": "L4-2",
                "title": "Structured output y JSON",
                "concepts": [
                    ("JSON Schema", "Define exactamente la estructura de respuesta que esperas"),
                    ("Parsing automático", "Claude genera JSON válido que puedes parsear directamente"),
                    ("Casos de uso", "APIs, bases de datos, integraciones automatizadas"),
                ],
                "quiz_questions": [
                    ("¿Por qué usar JSON Schema?", ["Por estética", "Para garantizar estructura consistente", "Para velocidad"], 1),
                    ("¿Qué ventaja tiene JSON sobre texto libre?", ["Nada", "Es parseable automáticamente", "Es más corto"], 1),
                    ("¿Cuándo deberías pedir JSON?", ["Siempre", "Cuando necesites parsear automáticamente", "Nunca"], 1),
                ]
            },
            {
                "id": "L4-3",
                "title": "Batching y procesamiento en masa",
                "concepts": [
                    ("Procesar múltiples items", "Envía listas de elementos a procesar. Más eficiente que uno por uno"),
                    ("Costos reducidos", "Fewer API calls = menos costo y latencia"),
                    ("Consistencia", "Mismo modelo procesa todo, mejorando consistencia entre respuestas"),
                ],
                "quiz_questions": [
                    ("¿Cuál es la ventaja de batching?", ["Más rápido", "Más barato", "Ambas"], 2),
                    ("¿Cómo se ve un batch?", ["Un array JSON", "Una lista separada por comas", "Múltiples prompts"], 0),
                    ("¿Qué mejora con batching?", ["Velocidad y consistencia", "Solo velocidad", "Nada especial"], 0),
                ]
            },
            {
                "id": "L4-4",
                "title": "Vision & multimodal",
                "concepts": [
                    ("Procesar imágenes", "Claude analiza imágenes para OCR, análisis visual, descripciones"),
                    ("Múltiples imágenes", "Una conversación puede incluir varias imágenes. Perfecto para comparativas"),
                    ("Documentos visuales", "PDFs, screenshots, diagramas. Todo es procesable"),
                ],
                "quiz_questions": [
                    ("¿Qué puede hacer Claude con imágenes?", ["Describirlas", "Hacer OCR", "Ambas"], 2),
                    ("¿Cuántas imágenes puedo incluir en un prompt?", ["Solo 1", "Varias", "Depende del modelo"], 1),
                    ("¿Claude puede leer PDFs visualmente?", ["No", "Sí, procesando las imágenes", "Solo si los conviertes a texto"], 1),
                ]
            },
        ]
    },
    "M5": {
        "title": "Capacidades y herramientas",
        "description": "Descubre todo lo que Claude puede hacer con tus archivos",
        "color_primary": "#14B8A6",
        "color_secondary": "#84CC16",
        "icon": "🛠️",
        "lessons": [
            {
                "id": "L5-1",
                "title": "Análisis de documentos",
                "concepts": [
                    ("Procesar PDFs", "Sube documentos extensos. Claude extrae información, resume, analiza"),
                    ("Mantiene contexto", "Incluso con documentos muy largos, Claude mantiene coherencia"),
                    ("Extracción de datos", "Saca información estructurada: tablas, hechos clave, referencias"),
                ],
                "quiz_questions": [
                    ("¿Qué puede hacer Claude con un PDF?", ["Solo verlo", "Extraer, analizar, resumir", "Solo copiar texto"], 1),
                    ("¿Hay límite de tamaño para documentos?", ["Sí, muy restrictivo", "Sí, pero bastante amplio", "No hay límite"], 1),
                    ("¿Puede Claude mantener coherencia en documentos extensos?", ["A veces", "Sí, muy bien", "No"], 1),
                ]
            },
            {
                "id": "L5-2",
                "title": "Análisis de imágenes",
                "concepts": [
                    ("OCR automático", "Lee texto en imágenes, diagramas, fotos de documentos"),
                    ("Descripción visual", "Analiza composición, objetos, contexto de una imagen"),
                    ("Comparación", "Compara imágenes lado a lado para encontrar diferencias"),
                ],
                "quiz_questions": [
                    ("¿Qué es OCR en el contexto de Claude?", ["Una herramienta externa", "Lectura automática de texto en imágenes", "Un tipo de prompt"], 1),
                    ("¿Puede Claude comparar dos imágenes?", ["No", "Sí", "Solo si están juntas"], 1),
                    ("¿Claude analiza la composición visual?", ["No", "Sí", "Solo si la pides"], 1),
                ]
            },
            {
                "id": "L5-3",
                "title": "Generación de código",
                "concepts": [
                    ("Múltiples lenguajes", "Python, JavaScript, SQL, HTML, CSS, Go, Rust, etc."),
                    ("Debugging", "Pega código roto. Claude identifica y corrige errores"),
                    ("Explicación", "Claude explica código línea por línea o a alto nivel"),
                ],
                "quiz_questions": [
                    ("¿Cuántos lenguajes de programación entiende Claude?", ["2-3", "Muchos", "Todos"], 1),
                    ("¿Puede Claude debuggear código?", ["No", "Sí, con prompts claros", "Solo en Python"], 1),
                    ("¿Qué tipo de explicación puedo pedir?", ["Solo general", "General o línea por línea", "Ninguna"], 1),
                ]
            },
            {
                "id": "L5-4",
                "title": "Escritura y edición",
                "concepts": [
                    ("Redacción original", "Escribe desde cero: artículos, reportes, correos, copys"),
                    ("Edición y reescritura", "Mejora claridad, tono, gramática, concisión de textos existentes"),
                    ("Adaptación de voz", "Adopta la voz: formal, casual, técnica, creativa"),
                ],
                "quiz_questions": [
                    ("¿Puede Claude escribir contenido original?", ["Solo resumir", "Sí, desde cero", "No"], 1),
                    ("¿Qué tipo de reescrituras puede hacer?", ["Solo gramática", "Tono, claridad, concisión", "Nada"], 1),
                    ("¿Claude mantiene voces de diferentes estilos?", ["No", "Sí, si la instruyes", "Solo formal"], 1),
                ]
            },
        ]
    },
    "M6": {
        "title": "Casos de uso prácticos",
        "description": "Aplicaciones reales: marketing, código, análisis, creatividad",
        "color_primary": "#7C3AED",
        "color_secondary": "#F472B6",
        "icon": "💡",
        "lessons": [
            {
                "id": "L6-1",
                "title": "Marketing y content",
                "concepts": [
                    ("Generación de copys", "Títulos, descripciones, emails, posts para redes sociales"),
                    ("A/B testing", "Genera múltiples versiones. Compara tonos y enfoques"),
                    ("SEO", "Optimiza textos para búsqueda sin sonar robótico"),
                ],
                "quiz_questions": [
                    ("¿Puede Claude generar copys de marketing?", ["No", "Sí, múltiples versiones", "Solo títulos"], 1),
                    ("¿Cómo optimiza Claude para SEO?", ["Repitiendo keywords", "Combinando legibilidad y keywords", "No lo hace"], 1),
                    ("¿Puede generar A/B tests?", ["No", "Sí, varias variantes", "Solo textos cortos"], 1),
                ]
            },
            {
                "id": "L6-2",
                "title": "Análisis y research",
                "concepts": [
                    ("Síntesis de información", "Resume documentos complejos sin perder detalles clave"),
                    ("Identificar patrones", "Analiza datos, conversaciones, métricas para encontrar tendencias"),
                    ("Preguntas críticas", "Genera preguntas para evaluación y due diligence"),
                ],
                "quiz_questions": [
                    ("¿Qué puede hacer Claude con datos complejos?", ["Nada", "Sintetizar y analizar", "Solo visualizar"], 1),
                    ("¿Puede identificar patrones Claude?", ["No", "Sí", "Solo en código"], 1),
                    ("¿Genera preguntas relevantes para análisis?", ["No", "Sí, preguntas críticas", "Solo confirmación"], 1),
                ]
            },
            {
                "id": "L6-3",
                "title": "Desarrollo y arquitectura",
                "concepts": [
                    ("Diseño de sistemas", "Ayuda a planificar arquitectura, bases de datos, flujos"),
                    ("Código de producción", "Genera código listo para usar, no solo ejemplos"),
                    ("DevOps", "Scripts, configuraciones Docker, CI/CD, infraestructura"),
                ],
                "quiz_questions": [
                    ("¿Claude puede ayudar con arquitectura de sistemas?", ["No", "Sí, flujos y diseño", "Solo base de datos"], 1),
                    ("¿Es el código de Claude listo para producción?", ["Nunca", "Con revisión sí", "Siempre"], 1),
                    ("¿Puede generar configuraciones DevOps?", ["No", "Sí, scripts y config", "Solo Docker"], 1),
                ]
            },
            {
                "id": "L6-4",
                "title": "Creatividad y educación",
                "concepts": [
                    ("Brainstorming", "Genera ideas, nombres, conceptos para proyectos"),
                    ("Tutoría personalizada", "Explica conceptos adaptos al nivel del alumno"),
                    ("Escritura creativa", "Historias, poemas, diálogos. Con coherencia y estilo"),
                ],
                "quiz_questions": [
                    ("¿Para qué sirve Claude en brainstorming?", ["Nada", "Generar muchas ideas", "Solo validar"], 1),
                    ("¿Puede actuar como tutor?", ["No", "Sí, adaptando explicaciones", "Solo en inglés"], 1),
                    ("¿Puede escribir ficción?", ["No", "Sí, con coherencia", "Solo poesía"], 1),
                ]
            },
        ]
    },
    "M7": {
        "title": "Buenas prácticas y límites",
        "description": "Usa Claude responsablemente conociendo sus límites",
        "color_primary": "#64748B",
        "color_secondary": "#F59E0B",
        "icon": "⚖️",
        "lessons": [
            {
                "id": "L7-1",
                "title": "Qué Claude hace bien",
                "concepts": [
                    ("Razonamiento", "Análisis lógico, comparaciones, identificación de patrones"),
                    ("Síntesis", "Resumir, extraer info clave, conectar conceptos"),
                    ("Generación", "Código, escritura, ideas, estructuras documentos"),
                ],
                "quiz_questions": [
                    ("¿En qué destaca Claude?", ["Búsquedas rápidas", "Razonamiento y síntesis", "Información en tiempo real"], 1),
                    ("¿Puede extraer patrones de datos?", ["No", "Sí", "Solo en tablas"], 1),
                    ("¿Es confiable para generar código?", ["Nunca", "Sí, pero requiere revisión", "Siempre"], 1),
                ]
            },
            {
                "id": "L7-2",
                "title": "Limitaciones a conocer",
                "concepts": [
                    ("Sin acceso a internet", "No busca información en tiempo real. Su conocimiento tiene fecha de corte"),
                    ("Puede alucinar", "Especialmente con datos muy específicos o números exactos"),
                    ("Sin memoria automática", "Olvida conversaciones anteriores a menos que las incluyas en el contexto"),
                ],
                "quiz_questions": [
                    ("¿Tiene Claude acceso a internet?", ["Sí", "No por defecto", "Solo en premium"], 1),
                    ("¿Cuándo puede Claude alucinar?", ["Nunca", "En casos específicos", "Siempre"], 1),
                    ("¿Recuerda conversaciones anteriores?", ["Sí siempre", "No automáticamente", "Solo en Pro"], 1),
                ]
            },
            {
                "id": "L7-3",
                "title": "Privacidad y seguridad",
                "concepts": [
                    ("Lo que compartes", "Tus prompts son datos tuyos. Lee la política de privacidad"),
                    ("No incluyas credenciales", "Nunca pases API keys, contraseñas, tokens en prompts"),
                    ("Datos sensibles", "Ten cuidado con PII (info personal identificable)"),
                ],
                "quiz_questions": [
                    ("¿Qué es PII en privacidad?", ["Personal Information Interface", "Información personalmente identificable", "Private Internal ID"], 1),
                    ("¿Puedo pasar credenciales a Claude?", ["Sí, es seguro", "No, nunca", "Solo contraseñas"], 1),
                    ("¿Quién es dueño de tus prompts?", ["Anthropic", "Tú", "Nadie"], 1),
                ]
            },
            {
                "id": "L7-4",
                "title": "Guía ética y responsabilidad",
                "concepts": [
                    ("Verificar outputs", "Siempre verificas datos críticos, especialmente en profesionales"),
                    ("Transparencia", "Avisa cuando usas IA en algo que afecta a otros"),
                    ("Bias y sesgos", "Claude puede tener sesgos. Sé crítico y diverso en fuentes"),
                ],
                "quiz_questions": [
                    ("¿Deberías verificar outputs de Claude?", ["No", "Siempre en datos críticos", "Solo en código"], 1),
                    ("¿Debes ser transparente sobre usar IA?", ["No", "Sí, especialmente en contexto profesional", "Solo en API"], 1),
                    ("¿Pueden los modelos tener sesgos?", ["No", "Sí, del entrenamiento", "Raramente"], 1),
                ]
            },
        ]
    },
    "M8": {
        "title": "Siguiente nivel: Desarrolladores",
        "description": "API, integración en tus productos, automatización",
        "color_primary": "#3F3F46",
        "color_secondary": "#FB7185",
        "icon": "💻",
        "lessons": [
            {
                "id": "L8-1",
                "title": "API y autenticación",
                "concepts": [
                    ("API REST", "Endpoint para llamar Claude desde tu código. JSON request/response"),
                    ("SDK oficial", "Python, Node.js, Go con helpers para manejo automático"),
                    ("Modelos disponibles", "claude-opus, claude-sonnet, claude-haiku con versionado"),
                ],
                "quiz_questions": [
                    ("¿Qué es API REST en Claude?", ["Una página web", "Endpoint para llamar Claude", "Un tipo de modelo"], 1),
                    ("¿Hay SDKs oficiales?", ["No", "Sí, Python, Node.js, Go", "Solo Python"], 1),
                    ("¿Cuántas versiones de modelos hay?", ["1", "Varias", "Cambia constantemente"], 1),
                ]
            },
            {
                "id": "L8-2",
                "title": "Streaming y async",
                "concepts": [
                    ("Streaming", "Recibe respuesta token por token. Para UX fluida en tiempo real"),
                    ("Async", "Llamadas no bloqueantes. Procesa múltiples requests en paralelo"),
                    ("Webhook", "Aviso cuando una tarea larga termina"),
                ],
                "quiz_questions": [
                    ("¿Para qué sirve streaming?", ["Ahorrar datos", "UX fluida, recibir tokens real-time", "Seguridad"], 1),
                    ("¿Qué permite async?", ["Ir más rápido", "Procesar múltiples requests paralela", "Nada especial"], 1),
                    ("¿Qué es un webhook?", ["Un tipo de API", "Notificación cuando tarea termina", "Seguridad"], 1),
                ]
            },
            {
                "id": "L8-3",
                "title": "Costos y optimización",
                "concepts": [
                    ("Pay per token", "Pagas por input y output. Precios diferentes por modelo"),
                    ("Context window", "Más tokens en contexto = más caro. Optimiza qué envías"),
                    ("Caching", "Reutiliza contexto similar para reducir costos y latencia"),
                ],
                "quiz_questions": [
                    ("¿Cómo se cobra la API?", ["Suscripción", "Por tokens usados", "Flat rate"], 1),
                    ("¿Afecta el tamaño de context al costo?", ["No", "Sí, más tokens = más caro", "Solo input"], 1),
                    ("¿Qué es caching de contexto?", ["Cache de navegador", "Reutilizar context para reducir costo", "Nada"], 1),
                ]
            },
            {
                "id": "L8-4",
                "title": "Casos avanzados",
                "concepts": [
                    ("Agents", "Claude toma decisiones y ejecuta acciones iterativamente"),
                    ("RAG (Retrieval-Augmented Generation)", "Busca documentos relevantes y Claude los analiza"),
                    ("Fine-tuning", "Personaliza el modelo para tu caso de uso específico"),
                ],
                "quiz_questions": [
                    ("¿Qué es un agent?", ["Una persona", "Claude tomando decisiones iterativas", "Un servicio"], 1),
                    ("¿Para qué sirve RAG?", ["Acelerar", "Darle acceso a documentos específicos", "Privacidad"], 1),
                    ("¿Qué es fine-tuning?", ["Cambiar parámetros básicos", "Personalizar modelo para tu caso", "Nada"], 1),
                ]
            },
        ]
    },
    "M9": {
        "title": "Tu primer proyecto real",
        "description": "Planifica, construye y lanza un proyecto end-to-end con Claude",
        "color_primary": "#D97706",
        "color_secondary": "#D1D5DB",
        "icon": "🚀",
        "lessons": [
            {
                "id": "L9-1",
                "title": "Planificación del proyecto",
                "concepts": [
                    ("Define el scope", "¿Qué problema resuelve? ¿A quién? ¿En cuánto tiempo?"),
                    ("Features MVP", "Mínimo viable. Qué es esencial vs. nice-to-have"),
                    ("Arquitectura básica", "Diagrama de componentes. Cómo se conectan"),
                ],
                "quiz_questions": [
                    ("¿Cuál es lo primero en planificación?", ["Código", "Definir scope claro", "Presupuesto"], 1),
                    ("¿Qué es MVP?", ["Máximo viable", "Mínimo viable", "Marco visual"], 1),
                    ("¿Debería planificar arquitectura?", ["No", "Sí, básica al menos", "Imposible sin código"], 1),
                ]
            },
            {
                "id": "L9-2",
                "title": "Arquitectura y diseño",
                "concepts": [
                    ("Tech stack", "Elige tecnologías: lenguaje, BD, frontend, hosting"),
                    ("Diagrama de flujo", "Cómo fluyen los datos entre componentes"),
                    ("Seguridad desde el inicio", "Autenticación, autorización, validación de inputs"),
                ],
                "quiz_questions": [
                    ("¿Qué es tech stack?", ["Dinero disponible", "Tecnologías que usarás", "Un tipo de código"], 1),
                    ("¿Cuándo pensar en seguridad?", ["Al final", "Desde el inicio", "Nunca en MVP"], 1),
                    ("¿Por qué un diagrama de flujo?", ["Estetica", "Entender flujo de datos", "No ayuda"], 1),
                ]
            },
            {
                "id": "L9-3",
                "title": "Implementación parte 1",
                "concepts": [
                    ("Core features", "Empieza con lo esencial. Features que resuelven el problema central"),
                    ("Iteración rápida", "Versión funcional pequeña es mejor que perfecta después"),
                    ("Scaffolding", "Estructura base. API skeleton, BD schema, UI componentes básicos"),
                ],
                "quiz_questions": [
                    ("¿Por dónde empezar a codificar?", ["Interfaz", "Features esenciales del core", "Optimizaciones"], 1),
                    ("¿Debería ser perfecta la V1?", ["Sí", "No, iterar es mejor", "Depende"], 1),
                    ("¿Qué es scaffolding?", ["Decoración", "Estructura base del proyecto", "Herramientas"], 1),
                ]
            },
            {
                "id": "L9-4",
                "title": "Implementación parte 2",
                "concepts": [
                    ("Integraciones", "Conecta con APIs externas. Stripe, Slack, etc según necesidad"),
                    ("Testing", "Unit tests, integration tests. Automatizar validación"),
                    ("Documentación", "README claro, comentarios en código crítico, API docs"),
                ],
                "quiz_questions": [
                    ("¿Cuándo integrar APIs externas?", ["Inmediatamente", "Cuando el core funcione", "Nunca"], 1),
                    ("¿Debería testear?", ["No, perder tiempo", "Sí, especialmente core logic", "Solo producción"], 1),
                    ("¿Qué documentar?", ["Todo obsesivamente", "Claro + crítico", "Nada"], 1),
                ]
            },
            {
                "id": "L9-5",
                "title": "Testing y QA",
                "concepts": [
                    ("Estrategia de testing", "Unit, integration, end-to-end. Piramide de tests"),
                    ("Bug reports", "Reproducibilidad. Paso a paso, expected vs. actual"),
                    ("Regresión", "Asegurar que cambios nuevos no rompan lo viejo"),
                ],
                "quiz_questions": [
                    ("¿Cuál es la estructura correcta de tests?", ["E2E principalmente", "Pirámide: units + integration + E2E", "Solo manuales"], 1),
                    ("¿Cómo reportar un bug bien?", ["'No funciona'", "Pasos reproducibles + contexto", "Esperanza"], 1),
                    ("¿Qué es regresión?", ["Ir atrás", "Que cambios nuevos rompan viejo", "Estadística"], 1),
                ]
            },
            {
                "id": "L9-6",
                "title": "Deploy y mantenimiento",
                "concepts": [
                    ("Ambientes", "Dev, staging, producción. Cada uno con su config"),
                    ("CI/CD", "Automatizar deploy. Push → test → deploy automático"),
                    ("Monitoring", "Logs, métricas, alertas. Saber si algo va mal"),
                ],
                "quiz_questions": [
                    ("¿Cuántos ambientes necesitas?", ["1", "Dev, staging, prod", "Infinitos"], 1),
                    ("¿Qué es CI/CD?", ["Otro acrónimo", "Automatizar test y deploy", "Herramienta de BD"], 1),
                    ("¿Por qué monitorear?", ["Vanidad", "Detectar problemas, entender usuarios", "Costo"], 1),
                ]
            },
        ]
    }
}

# ============================================================================
# HTML TEMPLATE
# ============================================================================

def generate_lesson_html(module_key: str, lesson_data: Dict, module_data: Dict) -> str:
    """
    Generate a complete, self-contained HTML file for a lesson.
    Includes all CSS, JavaScript, and assets inline.
    """

    module_title = module_data["title"]
    color_primary = module_data["color_primary"]
    color_secondary = module_data["color_secondary"]
    module_icon = module_data["icon"]

    lesson_id = lesson_data["id"]
    lesson_title = lesson_data["title"]
    concepts = lesson_data["concepts"]
    quiz_questions = lesson_data["quiz_questions"]

    # Build slides array
    slides = []

    # Slide 1: Intro
    slides.append({
        "type": "intro",
        "module_id": module_key,
        "module_title": module_title,
        "lesson_id": lesson_id,
        "lesson_title": lesson_title,
        "lesson_description": f"Aprende {lesson_title.lower()}",
    })

    # Slides 2-4: First concept with flip card + quiz
    if len(concepts) >= 1:
        concept_title, concept_desc = concepts[0]
        q_idx = 0 if len(quiz_questions) > 0 else None
        slides.append({
            "type": "flip_card",
            "concept_title": concept_title,
            "concept_description": concept_desc,
        })
        if q_idx is not None:
            q, options, correct = quiz_questions[q_idx]
            slides.append({
                "type": "quiz",
                "question": q,
                "options": options,
                "correct_index": correct,
            })

    # Slides 5-7: Second concept
    if len(concepts) >= 2:
        concept_title, concept_desc = concepts[1]
        q_idx = 1 if len(quiz_questions) > 1 else None
        slides.append({
            "type": "flip_card",
            "concept_title": concept_title,
            "concept_description": concept_desc,
        })
        if q_idx is not None:
            q, options, correct = quiz_questions[q_idx]
            slides.append({
                "type": "quiz",
                "question": q,
                "options": options,
                "correct_index": correct,
            })

    # Slides 8-10: Third concept
    if len(concepts) >= 3:
        concept_title, concept_desc = concepts[2]
        q_idx = 2 if len(quiz_questions) > 2 else None
        slides.append({
            "type": "flip_card",
            "concept_title": concept_title,
            "concept_description": concept_desc,
        })
        if q_idx is not None:
            q, options, correct = quiz_questions[q_idx]
            slides.append({
                "type": "quiz",
                "question": q,
                "options": options,
                "correct_index": correct,
            })

    # Slides 11-13: Fourth concept (if exists)
    if len(concepts) >= 4:
        concept_title, concept_desc = concepts[3]
        q_idx = 3 if len(quiz_questions) > 3 else None
        slides.append({
            "type": "flip_card",
            "concept_title": concept_title,
            "concept_description": concept_desc,
        })
        if q_idx is not None:
            q, options, correct = quiz_questions[q_idx]
            slides.append({
                "type": "quiz",
                "question": q,
                "options": options,
                "correct_index": correct,
            })

    # Slide 14: Key points
    slides.append({
        "type": "keypoints",
        "points": [concept[0] for concept in concepts[:4]],
    })

    # Slide 15: Summary
    slides.append({
        "type": "summary",
        "lesson_title": lesson_title,
        "next_lesson": f"Próxima lección",
    })

    # Slide 16: Conclusion
    slides.append({
        "type": "conclusion",
        "module_title": module_title,
        "lesson_title": lesson_title,
    })

    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{lesson_id} - {lesson_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz@0,9..144;1,9..144&family=Geist:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --color-primary: {color_primary};
            --color-secondary: {color_secondary};
            --color-bg-light: #f8fafc;
            --color-bg-dark: #0f172a;
            --color-text-light: #1e293b;
            --color-text-dark: #f1f5f9;
            --color-border: #e2e8f0;
        }}

        [data-theme="dark"] {{
            --color-bg: var(--color-bg-dark);
            --color-text: var(--color-text-dark);
        }}

        [data-theme="light"] {{
            --color-bg: var(--color-bg-light);
            --color-text: var(--color-text-light);
        }}

        html {{
            scroll-behavior: smooth;
        }}

        body {{
            font-family: 'Geist', sans-serif;
            background-color: var(--color-bg);
            color: var(--color-text);
            line-height: 1.6;
            transition: background-color 0.3s, color 0.3s;
        }}

        .container {{
            width: 100%;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }}

        .slides-wrapper {{
            flex: 1;
            position: relative;
            overflow: hidden;
        }}

        .slide {{
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            opacity: 0;
            transition: opacity 0.5s ease-in-out;
            padding: 60px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }}

        .slide.active {{
            opacity: 1;
            z-index: 10;
        }}

        .slide-intro {{
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
            color: white;
        }}

        .slide-intro h1 {{
            font-family: 'Fraunces', serif;
            font-size: 3.5rem;
            margin-bottom: 1rem;
            font-style: italic;
        }}

        .slide-intro .module-badge {{
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 0.5rem 1rem;
            border-radius: 999px;
            font-size: 0.875rem;
            margin-bottom: 2rem;
        }}

        .slide-intro p {{
            font-size: 1.25rem;
            opacity: 0.9;
            max-width: 600px;
        }}

        .slide-flip {{
            display: flex;
            justify-content: center;
            align-items: center;
            perspective: 1000px;
        }}

        .flip-card {{
            width: 500px;
            height: 400px;
            position: relative;
            transform-style: preserve-3d;
            cursor: pointer;
            transition: transform 0.6s;
        }}

        .flip-card.flipped {{
            transform: rotateY(180deg);
        }}

        .flip-card-front, .flip-card-back {{
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        }}

        .flip-card-front {{
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
            color: white;
        }}

        .flip-card-back {{
            background: var(--color-bg);
            color: var(--color-text);
            transform: rotateY(180deg);
            border: 2px solid var(--color-primary);
        }}

        .flip-card-front h3 {{
            font-family: 'Fraunces', serif;
            font-size: 2rem;
            margin-bottom: 1rem;
        }}

        .flip-card-front p {{
            font-size: 1rem;
            opacity: 0.9;
        }}

        .flip-card-back h3 {{
            font-family: 'Fraunces', serif;
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--color-primary);
        }}

        .flip-card-back p {{
            font-size: 0.95rem;
            line-height: 1.7;
        }}

        .flip-hint {{
            font-size: 0.75rem;
            margin-top: 1rem;
            opacity: 0.6;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .slide-quiz {{
            background: var(--color-bg);
            max-width: 700px;
        }}

        .quiz-question {{
            font-family: 'Fraunces', serif;
            font-size: 1.75rem;
            margin-bottom: 2rem;
            color: var(--color-text);
        }}

        .quiz-options {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        .quiz-option {{
            padding: 1.5rem;
            border: 2px solid var(--color-border);
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s;
            background: transparent;
            color: var(--color-text);
            text-align: left;
            font-size: 1.1rem;
            font-weight: 500;
        }}

        .quiz-option:hover {{
            border-color: var(--color-primary);
            background: var(--color-primary);
            color: white;
            transform: translateX(10px);
        }}

        .quiz-option.correct {{
            border-color: #10b981;
            background: #10b981;
            color: white;
        }}

        .quiz-option.incorrect {{
            border-color: #ef4444;
            background: #ef4444;
            color: white;
        }}

        .quiz-feedback {{
            margin-top: 1.5rem;
            padding: 1rem;
            border-radius: 8px;
            font-weight: 600;
            min-height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .quiz-feedback.correct {{
            background: #d1fae5;
            color: #065f46;
        }}

        .quiz-feedback.incorrect {{
            background: #fee2e2;
            color: #7f1d1d;
        }}

        .slide-keypoints {{
            max-width: 800px;
        }}

        .slide-keypoints h2 {{
            font-family: 'Fraunces', serif;
            font-size: 2.5rem;
            margin-bottom: 2rem;
            color: var(--color-primary);
        }}

        .keypoints-list {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            text-align: left;
        }}

        .keypoint-item {{
            padding: 1.5rem;
            background: linear-gradient(135deg, var(--color-primary)11 0%, var(--color-secondary)11 100%);
            border-left: 4px solid var(--color-primary);
            border-radius: 8px;
        }}

        .keypoint-item strong {{
            color: var(--color-primary);
            display: block;
            margin-bottom: 0.5rem;
        }}

        .slide-summary {{
            max-width: 700px;
        }}

        .slide-summary h2 {{
            font-family: 'Fraunces', serif;
            font-size: 2rem;
            margin-bottom: 1rem;
            color: var(--color-primary);
        }}

        .summary-text {{
            font-size: 1.1rem;
            margin-bottom: 2rem;
            opacity: 0.8;
        }}

        .next-lesson-btn {{
            display: inline-block;
            padding: 1rem 2rem;
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.3s, box-shadow 0.3s;
        }}

        .next-lesson-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }}

        .slide-conclusion {{
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
            color: white;
        }}

        .slide-conclusion h1 {{
            font-family: 'Fraunces', serif;
            font-size: 3rem;
            margin-bottom: 1rem;
        }}

        .slide-conclusion p {{
            font-size: 1.25rem;
            opacity: 0.9;
            margin-bottom: 2rem;
        }}

        /* Controls */
        .controls {{
            padding: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid var(--color-border);
        }}

        .nav-buttons {{
            display: flex;
            gap: 1rem;
        }}

        .nav-btn {{
            padding: 0.75rem 1.5rem;
            border: 2px solid var(--color-primary);
            background: transparent;
            color: var(--color-primary);
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
        }}

        .nav-btn:hover {{
            background: var(--color-primary);
            color: white;
        }}

        .nav-btn:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}

        .progress-bar {{
            height: 4px;
            background: var(--color-border);
            border-radius: 2px;
            overflow: hidden;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--color-primary), var(--color-secondary));
            width: 0%;
            transition: width 0.3s;
        }}

        .slide-counter {{
            text-align: center;
            font-weight: 600;
            min-width: 100px;
        }}

        .theme-toggle {{
            padding: 0.75rem 1.5rem;
            border: 2px solid var(--color-border);
            background: transparent;
            color: var(--color-text);
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
        }}

        .theme-toggle:hover {{
            border-color: var(--color-primary);
            background: var(--color-primary);
            color: white;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .slide {{
                padding: 40px 20px;
            }}

            .flip-card {{
                width: 90vw;
                height: 60vh;
                max-width: 400px;
                max-height: 300px;
            }}

            .slide-intro h1 {{
                font-size: 2rem;
            }}

            .keypoints-list {{
                grid-template-columns: 1fr;
            }}

            .controls {{
                flex-direction: column;
                gap: 1rem;
            }}
        }}
    </style>
</head>
<body data-theme="light">
    <div class="container">
        <div class="slides-wrapper">
"""

    # Add slides
    for i, slide in enumerate(slides):
        slide_class = f"slide slide-{slide['type']}"
        if i == 0:
            slide_class += " active"

        html += f'            <div class="{slide_class}" data-slide-index="{i}">\n'

        if slide["type"] == "intro":
            html += f"""                <div class="slide-intro">
                    <div class="module-badge">{slide['module_id']} • {slide['module_id'].replace('M', 'Módulo ')} • {module_icon}</div>
                    <h1>{slide['lesson_title']}</h1>
                    <p>{slide['lesson_description']}</p>
                </div>
"""

        elif slide["type"] == "flip_card":
            html += f"""                <div class="slide-flip">
                    <div class="flip-card" onclick="this.classList.toggle('flipped')">
                        <div class="flip-card-front">
                            <h3>{slide['concept_title']}</h3>
                            <p>Haz click para descubrir</p>
                            <div class="flip-hint">📖 Click para voltear</div>
                        </div>
                        <div class="flip-card-back">
                            <h3>{slide['concept_title']}</h3>
                            <p>{slide['concept_description']}</p>
                        </div>
                    </div>
                </div>
"""

        elif slide["type"] == "quiz":
            html += f"""                <div class="slide-quiz">
                    <h2 class="quiz-question">{slide['question']}</h2>
                    <div class="quiz-options">
"""
            for j, option in enumerate(slide['options']):
                html += f'                        <button class="quiz-option" onclick="checkAnswer({j}, {slide["correct_index"]}, event)">{option}</button>\n'
            html += """                    </div>
                    <div class="quiz-feedback" id="feedback" style="display: none;"></div>
                </div>
"""

        elif slide["type"] == "keypoints":
            html += """                <div class="slide-keypoints">
                    <h2>Puntos clave</h2>
                    <div class="keypoints-list">
"""
            for point in slide['points']:
                html += f'                        <div class="keypoint-item"><strong>{point}</strong></div>\n'
            html += """                    </div>
                </div>
"""

        elif slide["type"] == "summary":
            html += f"""                <div class="slide-summary">
                    <h2>Resumen</h2>
                    <p class="summary-text">Completaste el módulo de <strong>{slide['lesson_title']}</strong>. ¡Excelente trabajo!</p>
                    <button class="next-lesson-btn" onclick="nextSlide()">Próxima lección →</button>
                </div>
"""

        elif slide["type"] == "conclusion":
            html += f"""                <div class="slide-conclusion">
                    <h1>¡Lo hiciste!</h1>
                    <p>{slide['lesson_title']}</p>
                    <p style="font-size: 1rem; opacity: 0.8;">{slide['module_title']}</p>
                </div>
"""

        html += "            </div>\n"

    # Add controls and JavaScript
    total_slides = len(slides)
    html += f"""        </div>

        <div class="controls">
            <div class="nav-buttons">
                <button class="nav-btn" id="prevBtn" onclick="prevSlide()">← Anterior</button>
                <button class="nav-btn" id="nextBtn" onclick="nextSlide()">Siguiente →</button>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            <div class="slide-counter"><span id="currentSlide">1</span> / {total_slides}</div>
            <button class="theme-toggle" id="themeToggle" onclick="toggleTheme()">🌙</button>
        </div>
    </div>

    <script>
        let currentSlide = 0;
        const totalSlides = {total_slides};

        function showSlide(n) {{
            const slides = document.querySelectorAll('.slide');

            if (n >= totalSlides) currentSlide = totalSlides - 1;
            if (n < 0) currentSlide = 0;

            slides.forEach(slide => slide.classList.remove('active'));
            slides[currentSlide].classList.add('active');

            // Reiniciar quiz feedback
            const feedback = document.getElementById('feedback');
            if (feedback) {{
                feedback.style.display = 'none';
                feedback.textContent = '';
            }}

            // Resetear opciones de quiz
            const options = document.querySelectorAll('.quiz-option');
            options.forEach(opt => {{
                opt.classList.remove('correct', 'incorrect');
                opt.style.pointerEvents = 'auto';
            }});

            updateControls();
            updateProgress();
            document.getElementById('currentSlide').textContent = currentSlide + 1;
        }}

        function nextSlide() {{
            currentSlide++;
            showSlide(currentSlide);
        }}

        function prevSlide() {{
            currentSlide--;
            showSlide(currentSlide);
        }}

        function updateControls() {{
            document.getElementById('prevBtn').disabled = currentSlide === 0;
            document.getElementById('nextBtn').disabled = currentSlide === totalSlides - 1;
        }}

        function updateProgress() {{
            const progress = ((currentSlide + 1) / totalSlides) * 100;
            document.getElementById('progressFill').style.width = progress + '%';
        }}

        function checkAnswer(selectedIndex, correctIndex, event) {{
            const options = document.querySelectorAll('.quiz-option');
            options.forEach(opt => opt.style.pointerEvents = 'none');

            const feedback = document.getElementById('feedback');
            feedback.style.display = 'flex';

            if (selectedIndex === correctIndex) {{
                options[selectedIndex].classList.add('correct');
                feedback.classList.add('correct');
                feedback.classList.remove('incorrect');
                feedback.textContent = '✓ ¡Correcto!';
            }} else {{
                options[selectedIndex].classList.add('incorrect');
                options[correctIndex].classList.add('correct');
                feedback.classList.add('incorrect');
                feedback.classList.remove('correct');
                feedback.textContent = '✗ Incorrecto. La respuesta correcta está destacada.';
            }}
        }}

        function toggleTheme() {{
            const html = document.documentElement;
            const theme = html.getAttribute('data-theme');
            const newTheme = theme === 'light' ? 'dark' : 'light';
            html.setAttribute('data-theme', newTheme);
            document.getElementById('themeToggle').textContent = newTheme === 'light' ? '🌙' : '☀️';
            localStorage.setItem('theme', newTheme);
        }}

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowRight') nextSlide();
            if (e.key === 'ArrowLeft') prevSlide();
        }});

        // Load theme preference
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
        document.getElementById('themeToggle').textContent = savedTheme === 'light' ? '🌙' : '☀️';

        // Initialize
        showSlide(0);
    </script>
</body>
</html>
"""

    return html


def main():
    """Generate all 38 lesson HTML files."""

    # Use relative path that works in both local and workspace contexts
    output_dir = Path(__file__).parent / "public" / "claude-101-videos"
    output_dir.mkdir(parents=True, exist_ok=True)

    total_generated = 0

    for module_key, module_data in LESSONS_DATA.items():
        print(f"\n📚 Generating {module_key}: {module_data['title']}")

        for lesson in module_data["lessons"]:
            lesson_id = lesson["id"]
            lesson_title = lesson["title"]

            # Generate HTML
            html_content = generate_lesson_html(module_key, lesson, module_data)

            # Save file
            filename = f"{lesson_id}-slides.html"
            filepath = output_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)

            file_size_kb = len(html_content.encode('utf-8')) / 1024
            print(f"  ✓ {lesson_id}: {lesson_title} ({file_size_kb:.1f} KB)")

            total_generated += 1

    print(f"\n" + "="*60)
    print(f"✨ SUCCESS! Generated {total_generated} lessons")
    print(f"📁 Location: {output_dir}")
    print(f"="*60)


if __name__ == "__main__":
    main()
