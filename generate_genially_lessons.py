#!/usr/bin/env python3
"""
Generador de lecciones estilo Genially para Claude 101.
Crea 38 lecciones HTML5 auto-contenidas con:
- Estructura fluida (no slides tradicionales)
- Animaciones suaves CSS
- Interactividad exploratoria (tabs, acordeones, modales)
- Diseño moderno con whitespace generoso
- Colores por módulo
"""

import json
import os
from datetime import datetime
from pathlib import Path

# ==================== CONFIGURACIÓN ====================

LESSONS_CONFIG = {
    "M1": {
        "titulo": "Fundamentos de Claude",
        "color": "#2563EB",  # Azul
        "lecciones": [
            {
                "id": "L1-1",
                "titulo": "¿Qué es Claude?",
                "descripcion": "Introducción a Claude como asistente de IA",
                "tipo": "tabs",
                "tabs": [
                    {
                        "titulo": "Capacidades",
                        "contenido": [
                            "Procesamiento de lenguaje natural avanzado",
                            "Análisis profundo de textos largos",
                            "Razonamiento lógico y analítico",
                            "Escritura creativa y técnica",
                            "Programación en múltiples lenguajes"
                        ]
                    },
                    {
                        "titulo": "Modelos",
                        "contenido": [
                            "Claude 3 Opus: Máxima capacidad",
                            "Claude 3 Sonnet: Balance óptimo",
                            "Claude 3 Haiku: Rápido y eficiente",
                            "Actualizaciones regulares",
                            "API y web"
                        ]
                    },
                    {
                        "titulo": "Casos de Uso",
                        "contenido": [
                            "Escritura y contenido",
                            "Programación y análisis técnico",
                            "Investigación y análisis de datos",
                            "Brainstorming y creatividad",
                            "Educación y capacitación"
                        ]
                    }
                ],
                "quiz": [
                    {
                        "pregunta": "¿Cuál es la principal ventaja de Claude sobre otros modelos?",
                        "opciones": ["Velocidad", "Capacidad de razonamiento", "Precio bajo", "Disponibilidad"],
                        "respuesta": 1
                    }
                ]
            },
            {
                "id": "L1-2",
                "titulo": "API Basics",
                "descripcion": "Fundamentos de la API de Claude",
                "tipo": "tabs",
                "tabs": [
                    {
                        "titulo": "¿Qué es REST?",
                        "contenido": [
                            "Arquitectura cliente-servidor",
                            "Métodos HTTP (GET, POST, PUT, DELETE)",
                            "Requests y responses en JSON",
                            "Stateless: sin sesión persistente",
                            "RESTful: patrón estándar de web"
                        ]
                    },
                    {
                        "titulo": "Estructura JSON",
                        "contenido": [
                            "Request: { model, messages, max_tokens }",
                            "Messages: array de { role, content }",
                            "Response: { content, stop_reason, usage }",
                            "Role: 'user' o 'assistant'",
                            "Token usage: tracks consumption"
                        ]
                    },
                    {
                        "titulo": "Headers y Auth",
                        "contenido": [
                            "Authorization: Bearer API_KEY",
                            "Content-Type: application/json",
                            "API Key: guardar en env variable",
                            "Rate limits: respeta límites",
                            "Versión: x-api-version header"
                        ]
                    }
                ],
                "quiz": [
                    {
                        "pregunta": "¿Qué método HTTP se usa para enviar un prompt?",
                        "opciones": ["GET", "POST", "PUT", "DELETE"],
                        "respuesta": 1
                    }
                ]
            },
            {
                "id": "L1-3",
                "titulo": "Modelos y Pricing",
                "descripcion": "Comparativa de modelos y costos",
                "tipo": "acordeon",
                "acordeon": [
                    {
                        "titulo": "Claude 3 Opus",
                        "contenido": "Mayor capacidad, mejor razonamiento. Ideal para tareas complejas. Costo: 0.015 USD / 1K input tokens"
                    },
                    {
                        "titulo": "Claude 3 Sonnet",
                        "contenido": "Balance perfecto entre velocidad y capacidad. Más usado. Costo: 0.003 USD / 1K input tokens"
                    },
                    {
                        "titulo": "Claude 3 Haiku",
                        "contenido": "Muy rápido y económico. Ideal para tareas simples. Costo: 0.00025 USD / 1K input tokens"
                    }
                ],
                "quiz": [
                    {
                        "pregunta": "¿Cuál es el modelo más económico?",
                        "opciones": ["Opus", "Sonnet", "Haiku", "Todos igual"],
                        "respuesta": 2
                    }
                ]
            },
            {
                "id": "L1-4",
                "titulo": "Setup y Primeras Llamadas",
                "descripcion": "Configuración inicial y primeras pruebas",
                "tipo": "pasos",
                "pasos": [
                    {
                        "numero": 1,
                        "titulo": "Obtener API Key",
                        "descripcion": "Ir a console.anthropic.com, crear cuenta, generar key"
                    },
                    {
                        "numero": 2,
                        "titulo": "Instalar SDK",
                        "descripcion": "pip install anthropic (Python) o npm install @anthropic-ai/sdk (JS)"
                    },
                    {
                        "numero": 3,
                        "titulo": "Configurar autenticación",
                        "descripcion": "Guardar API Key en variable de entorno ANTHROPIC_API_KEY"
                    },
                    {
                        "numero": 4,
                        "titulo": "Primera llamada",
                        "descripcion": "Crear client y enviar un mensaje simple"
                    }
                ],
                "quiz": [
                    {
                        "pregunta": "¿Dónde se obtiene la API Key?",
                        "opciones": ["GitHub", "console.anthropic.com", "Gmail", "Dashboard de Stripe"],
                        "respuesta": 1
                    }
                ]
            }
        ]
    },
    "M2": {
        "titulo": "Prompting Avanzado",
        "color": "#DC2626",  # Rojo
        "lecciones": [
            {
                "id": "L2-1",
                "titulo": "Prompting 101",
                "descripcion": "Fundamentos de escribir buenos prompts",
                "tipo": "tabs",
                "tabs": [
                    {"titulo": "Estructura", "contenido": ["Contexto claro", "Instrucción explícita", "Formato esperado", "Restricciones", "Ejemplo"]},
                    {"titulo": "Claridad", "contenido": ["Lenguaje directo", "Evita ambigüedades", "Específico no genérico", "Una tarea a la vez", "Revisa ortografía"]},
                    {"titulo": "Contexto", "contenido": ["Quién eres tú", "Quién es Claude", "Qué sabe, qué no", "Dominio de aplicación", "Audiencia target"]},
                    {"titulo": "Ejemplos", "contenido": ["Few-shot prompting", "Patrón claro", "Casos variados", "Inputs y outputs", "Consistencia"]}
                ]
            },
            {
                "id": "L2-2",
                "titulo": "Few-Shot Prompting",
                "descripcion": "Enseña mediante ejemplos",
                "tipo": "acordeon",
                "acordeon": [
                    {"titulo": "Qué es Few-Shot", "contenido": "Proporcionar ejemplos de entrada-salida para que Claude aprenda el patrón sin instrucciones explícitas."},
                    {"titulo": "Few-shot vs Zero-shot", "contenido": "Few-shot: con ejemplos (mejor). Zero-shot: sin ejemplos (más rápido)."},
                    {"titulo": "Mejores prácticas", "contenido": "3-5 ejemplos suficientes. Variedad en los ejemplos. Formato consistente. Claro input/output."}
                ]
            },
            {
                "id": "L2-3",
                "titulo": "Chain-of-Thought",
                "descripcion": "Razonamiento paso a paso",
                "tipo": "tabs",
                "tabs": [
                    {"titulo": "Qué es", "contenido": ["Pedir a Claude que piense en pasos", "Explique su razonamiento", "Muestre cálculos intermedios", "Llega a conclusiones mejor"]},
                    {"titulo": "Cuándo usar", "contenido": ["Problemas complejos", "Lógica matemática", "Análisis de casos", "Decisiones difíciles"]},
                    {"titulo": "Ejemplo", "contenido": ["Pregunta: ¿Cuánto es 15% de 240?", "CoT: 'Primero calculo 10% = 24. Luego 5% = 12. 10% + 5% = 36.'", "Respuesta correcta", "Más confiable"]}
                ]
            },
            {
                "id": "L2-4",
                "titulo": "System Prompts",
                "descripcion": "Define el rol y comportamiento de Claude",
                "tipo": "acordeon",
                "acordeon": [
                    {"titulo": "Qué es un System Prompt", "contenido": "Instrucción inicial que define cómo Claude debe actuar. Se envía una sola vez, no cambia durante la conversación."},
                    {"titulo": "Uso: Asistente técnico", "contenido": "System: 'Eres un experto en Python. Responde en español. Sé conciso.'"},
                    {"titulo": "Uso: Narrador", "contenido": "System: 'Eres un narrador épico. Describe acciones con dramatismo. Usa metáforas.'"},
                    {"titulo": "Mejores prácticas", "contenido": "Clara personalidad. Restricciones explícitas. Tono definido. Ejemplos si es necesario."}
                ]
            }
        ]
    },
    "M3": {
        "titulo": "Visión por Computadora",
        "color": "#7C3AED",  # Púrpura
        "lecciones": [
            {
                "id": "L3-1",
                "titulo": "Image Inputs",
                "descripcion": "Cómo compartir imágenes con Claude",
                "tipo": "tabs",
                "tabs": [
                    {"titulo": "Formatos soportados", "contenido": ["JPEG", "PNG", "GIF", "WebP", "Máx 5MB por imagen"]},
                    {"titulo": "Tamaños", "contenido": ["Ancho: 320 a 1024 px", "Alto: 320 a 1024 px", "Aspecto ratio libre", "Se escala automáticamente"]},
                    {"titulo": "Buenas prácticas", "contenido": ["Luz clara", "Enfoque nítido", "Objeto centrado", "Sin elementos distractores", "Comprime imágenes grandes"]}
                ]
            },
            {
                "id": "L3-2",
                "titulo": "Vision Capabilities",
                "descripcion": "Qué puede ver Claude en imágenes",
                "tipo": "accordion",
                "acordeon": [
                    {"titulo": "Identificación de objetos", "contenido": "Reconoce elementos, personas, animales, lugares."},
                    {"titulo": "OCR (Lectura de texto)", "contenido": "Lee texto impreso o manuscrito en imágenes."},
                    {"titulo": "Análisis de gráficos", "contenido": "Interpreta gráficos, tablas, diagramas, infografías."},
                    {"titulo": "Detección de emociones", "contenido": "Identifica expresiones faciales y contexto emocional."},
                    {"titulo": "Análisis de composición", "contenido": "Evalúa colores, luz, composición, estilo visual."}
                ]
            },
            {
                "id": "L3-3",
                "titulo": "Multimodal Applications",
                "descripcion": "Casos de uso combinando imagen y texto",
                "tipo": "cards",
                "cards": [
                    {"titulo": "Análisis de documentos", "descripcion": "Sube facturas, contrato, reportes. Claude los analiza y extrae info."},
                    {"titulo": "Descripción de imágenes", "descripcion": "Sube foto. Claude genera descripción detallada, ALT text, caption."},
                    {"titulo": "Traducción de texto en imagen", "descripcion": "Sube señal en otro idioma. Claude traduce el texto."},
                    {"titulo": "Análisis de datos visuales", "descripcion": "Gráficos, tablas, infografías. Claude interpreta y resume."},
                    {"titulo": "QA sobre imágenes", "descripcion": "Haz preguntas específicas sobre contenido de una imagen."}
                ]
            },
            {
                "id": "L3-4",
                "titulo": "Casos Reales con Visión",
                "descripcion": "Ejemplos prácticos del mundo real",
                "tipo": "carousel",
                "casos": [
                    {"titulo": "Auditoría de facturas", "descripcion": "Procesa 100 facturas por mes. Extrae montos, fechas, proveedores automáticamente."},
                    {"titulo": "Moderación de contenido", "descripcion": "Analiza screenshots, detecta violaciones de política, genera reportes."},
                    {"titulo": "Etiquetado de imágenes", "descripcion": "Dataset de 10K imágenes. Claude genera tags y categorías en bulk."},
                    {"titulo": "Análisis de competencia", "descripcion": "Screenshots de competitors. Claude extrae features, pricing, diferencias."},
                    {"titulo": "Validación de formularios", "descripcion": "Sube documentos escaneados. Claude valida legibilidad y completitud."}
                ]
            }
        ]
    },
    "M4": {
        "titulo": "Técnicas Avanzadas",
        "color": "#059669",  # Verde
        "lecciones": [
            {
                "id": "L4-1",
                "titulo": "Few-Shot Avanzado",
                "descripcion": "Patrones complejos con ejemplos",
                "tipo": "acordeon",
                "acordeon": [
                    {"titulo": "Chain prompting", "contenido": "Múltiples ejemplos encadenados. Cada uno más complejo. Gradualmente hacia el objetivo."},
                    {"titulo": "Cross-domain examples", "contenido": "Ejemplos de dominios similares pero diferentes. Ayuda a generalizar."},
                    {"titulo": "Negative examples", "contenido": "Mostrar qué NO hacer. Ejemplos de salidas incorrectas."},
                    {"titulo": "Progressive disclosure", "contenido": "Ejemplos básicos primero. Luego casos complejos. Escala gradualmente."}
                ]
            },
            {
                "id": "L4-2",
                "titulo": "XML Tagging",
                "descripcion": "Estructura datos con tags XML",
                "tipo": "pasos",
                "pasos": [
                    {"numero": 1, "titulo": "Define estructura", "descripcion": "<proyecto><nombre>...</nombre><estado>...</estado></proyecto>"},
                    {"numero": 2, "titulo": "Instrucción clara", "descripcion": "Responde siempre en formato XML con estos tags."},
                    {"numero": 3, "titulo": "Parseo automático", "descripcion": "Extrae datos del XML programáticamente."},
                    {"numero": 4, "titulo": "Integración", "descripcion": "Alimenta otros sistemas con datos estructurados."}
                ]
            },
            {
                "id": "L4-3",
                "titulo": "Role-Playing Prompts",
                "descripcion": "Dale a Claude un rol específico",
                "tipo": "tabs",
                "tabs": [
                    {"titulo": "Qué es", "contenido": ["Claude actúa como personaje", "Adopta perspectiva específica", "Responde en carácter", "Mejora contexto"]},
                    {"titulo": "Cómo funciona", "contenido": ["'Eres un detective investigando un robo'", "'Eres un profesor de historia'", "'Eres un crítico de arte'", "Claude responde desde ese rol"]},
                    {"titulo": "Ejemplos", "contenido": ["Chatbot de soporte", "Tutor educativo", "Consultor empresarial", "Narrador de historias"]}
                ]
            },
            {
                "id": "L4-4",
                "titulo": "Iteración Estructurada",
                "descripcion": "Refinamiento sistemático de respuestas",
                "tipo": "accordion",
                "acordeon": [
                    {"titulo": "Ciclo feedback", "contenido": "Prompt → Respuesta → Análisis → Refinamiento → Nueva respuesta."},
                    {"titulo": "Versioning", "contenido": "Guarda versiones de prompts. Compara outputs. Mejora gradualmente."},
                    {"titulo": "A/B testing", "contenido": "Dos versiones de prompt. Evalúa cuál es mejor. Itera."},
                    {"titulo": "Métricas", "contenido": "Define criterios de evaluación. Mide mejora. Documenta proceso."}
                ]
            }
        ]
    },
    "M5": {
        "titulo": "Features Avanzadas",
        "color": "#EA580C",  # Naranja
        "lecciones": [
            {
                "id": "L5-1",
                "titulo": "Artifacts",
                "descripcion": "Interfaz para código y contenido largo",
                "tipo": "tabs",
                "tabs": [
                    {"titulo": "Qué son", "contenido": ["Contenedor especial en web", "Para código, HTML, documentos", "Interfaz clara", "Separado del chat"]},
                    {"titulo": "Cuándo usar", "contenido": ["Código >15 líneas", "HTML/CSS/JS completo", "Documentos markdown", "Proyectos interactivos"]},
                    {"titulo": "Ejemplos", "contenido": ["Aplicación React interactiva", "Script Python listo para usar", "Página HTML completa", "Dashboard HTML5"]}
                ]
            },
            {
                "id": "L5-2",
                "titulo": "Búsqueda Web",
                "descripcion": "Acceso a información en tiempo real",
                "tipo": "pasos",
                "pasos": [
                    {"numero": 1, "titulo": "Claude busca en internet", "descripcion": "Si pides info actual, Claude busca automáticamente."},
                    {"numero": 2, "titulo": "Procesa resultados", "descripcion": "Analiza múltiples fuentes. Extrae lo relevante."},
                    {"numero": 3, "titulo": "Cita fuentes", "descripcion": "Incluye links a fuentes originales."},
                    {"numero": 4, "titulo": "Respuesta actualizada", "descripcion": "Combina conocimiento con info reciente."}
                ]
            },
            {
                "id": "L5-3",
                "titulo": "File Uploads",
                "descripcion": "Sube y procesa archivos",
                "tipo": "accordion",
                "acordeon": [
                    {"titulo": "Formatos soportados", "contenido": "PDF, DOC, DOCX, TXT, CSV, JSON, ZIP, y más."},
                    {"titulo": "Límite de tamaño", "contenido": "Máximo 20MB por archivo en algunos planes. API tiene límites diferentes."},
                    {"titulo": "Casos de uso", "contenido": "Análisis de documentos. Procesamiento de datasets. Extracción de datos. Resumen de reportes."},
                    {"titulo": "Privacidad", "contenido": "No se almacenan archivos. Se procesan una sola vez. Borra después."}
                ]
            },
            {
                "id": "L5-4",
                "titulo": "Memory y Contexto Largo",
                "descripcion": "Manejo de conversaciones extensas",
                "tipo": "tabs",
                "tabs": [
                    {"titulo": "Tamaño de contexto", "contenido": ["Opus: 200K tokens (~150K palabras)", "Sonnet: 200K tokens", "Haiku: 200K tokens", "Suficiente para documentos grandes"]},
                    {"titulo": "Cómo funciona", "contenido": ["Todo el historial se envía", "Claude tiene contexto completo", "Más tokens = más caro", "Optimiza si es posible"]},
                    {"titulo": "Tips de optimización", "contenido": ["Resume conversaciones largas", "Agrupa mensajes antiguos", "Usa system prompt", "Limpia historial periódicamente"]}
                ]
            }
        ]
    },
    "M6": {
        "titulo": "Aplicaciones Prácticas",
        "color": "#2563EB",  # Azul claro
        "lecciones": [
            {
                "id": "L6-1",
                "titulo": "Escritura y Contenido",
                "descripcion": "Aplicaciones en escritura",
                "tipo": "tabs",
                "tabs": [
                    {"titulo": "Blogs", "contenido": ["Brainstorm de ideas", "Estructura de artículo", "Redacción inicial", "SEO optimization", "Call-to-action"]},
                    {"titulo": "Emails", "contenido": ["Subject lines efectivos", "Body persuasivo", "Tone adaptable", "Personalization", "A/B testing copy"]},
                    {"titulo": "Redes Sociales", "contenido": ["Threads coherentes", "Hashtags relevantes", "Emojis estratégicos", "Engagement hooks", "Multi-plataforma"]}
                ]
            },
            {
                "id": "L6-2",
                "titulo": "Programación",
                "descripcion": "Ayuda en desarrollo",
                "tipo": "tabs",
                "tabs": [
                    {"titulo": "Python", "contenido": ["Snippets de código", "Debug de errores", "Data science workflows", "Optimización", "Testing"]},
                    {"titulo": "JavaScript", "contenido": ["Frontend logic", "React components", "API integration", "Performance tips", "Browser APIs"]},
                    {"titulo": "SQL", "contenido": ["Query optimization", "Diseño de schema", "Performance", "Joins complejos", "Subqueries"]}
                ]
            },
            {
                "id": "L6-3",
                "titulo": "Análisis de Datos",
                "descripcion": "Procesa y analiza información",
                "tipo": "pasos",
                "pasos": [
                    {"numero": 1, "titulo": "Preparación", "descripcion": "Limpieza de datos. Normalización. Validación."},
                    {"numero": 2, "titulo": "Análisis", "descripcion": "Identifica patrones. Estadísticas. Correlaciones."},
                    {"numero": 3, "titulo": "Visualización", "descripcion": "Gráficos. Dashboards. Reportes."},
                    {"numero": 4, "titulo": "Recomendaciones", "descripcion": "Insights. Acciones recomendadas."}
                ]
            },
            {
                "id": "L6-4",
                "titulo": "Creatividad y Brainstorm",
                "descripcion": "Genera ideas y contenido creativo",
                "tipo": "tabs",
                "tabs": [
                    {"titulo": "Ideación", "contenido": ["Brainstorm sin filtro", "Pensamiento divergente", "Múltiples ángulos", "Combinaciones nuevas"]},
                    {"titulo": "Refinamiento", "descripcion": ["Selecciona mejores ideas", "Elabora detalles", "Agrega contexto", "Prepara ejecución"]},
                    {"titulo": "Validación", "contenido": ["Feedback de audiencia", "Testing de conceptos", "Mejoras iterativas", "Lanzamiento"]}
                ]
            }
        ]
    },
    "M7": {
        "titulo": "Responsabilidad y Seguridad",
        "color": "#DC2626",  # Rojo
        "lecciones": [
            {
                "id": "L7-1",
                "titulo": "Privacidad y Datos Sensibles",
                "descripcion": "Protege información confidencial",
                "tipo": "accordion",
                "acordeon": [
                    {"titulo": "Riesgos de compartir datos", "contenido": "Breach potencial. PII expuesta. Propiedad intelectual comprometida."},
                    {"titulo": "Cómo mitigar", "contenido": "Anonimiza datos. Redacta información sensible. Usa pseudónimos. Chunking."},
                    {"titulo": "Checklist de privacidad", "contenido": "¿Contiene emails? ¿IPs? ¿Tarjetas? ¿SSN? ¿Ubicaciones? Revisa todo."},
                    {"titulo": "Compliance", "contenido": "GDPR, CCPA, HIPAA. Cumple regulaciones. Documenta. Audit trail."}
                ]
            },
            {
                "id": "L7-2",
                "titulo": "Verificación y Fact-Checking",
                "descripcion": "Valida información y evita alucinaciones",
                "tipo": "tabs",
                "tabs": [
                    {"titulo": "Técnicas", "contenido": ["Claude reconoce límites de conocimiento", "Pide fuentes cuando es posible", "Marca info potencialmente inexacta", "Honra fecha de corte de datos"]},
                    {"titulo": "Herramientas", "contenido": ["Búsqueda web integrada", "Comparación con múltiples fuentes", "Fact-checking manual", "Terceros verificadores"]},
                    {"titulo": "Flujo de verificación", "contenido": ["Prompt claro pide verificación", "Claude busca fuentes", "Cita referencias", "Marca incertidumbre"]}
                ]
            },
            {
                "id": "L7-3",
                "titulo": "Limitaciones de Claude",
                "descripcion": "Entiende qué no puede hacer",
                "tipo": "accordion",
                "acordeon": [
                    {"titulo": "No puede navegar web por su cuenta", "contenido": "Solo en interfaz web. API requiere manual."},
                    {"titulo": "Contexto finito", "contenido": "200K tokens es mucho pero no infinito."},
                    {"titulo": "No ejecuta código", "contenido": "Escribe código, no lo corre. Tú ejecutas."},
                    {"titulo": "Conocimiento con fecha límite", "contenido": "Fue entrenado hasta abril 2024. Después = desconocido."},
                    {"titulo": "No es especialista perfecto", "contenido": "Mejor que mayoría pero puede equivocarse. Verifica info crítica."}
                ]
            },
            {
                "id": "L7-4",
                "titulo": "Responsabilidad y Ética",
                "descripcion": "Usa Claude responsablemente",
                "tipo": "tabs",
                "tabs": [
                    {"titulo": "Sesgos", "contenido": ["Claude puede reflejar sesgos de training data", "Cuidado con decisiones críticas", "Diverse perspectives mejora", "Mitiga activamente"]},
                    {"titulo": "Seguridad", "contenido": ["No pidas hacer nada ilegal", "Protege info ajena", "Evita manipulación", "Respeta consentimiento"]},
                    {"titulo": "Transparencia", "contenido": ["Discierne AI vs humano", "Revela que usaste Claude", "Responsable de output final", "Audit para auditoría"]}
                ]
            }
        ]
    },
    "M8": {
        "titulo": "Herramientas y Extensiones",
        "color": "#7C3AED",  # Púrpura
        "lecciones": [
            {
                "id": "L8-1",
                "titulo": "Claude Code",
                "descripcion": "Interfaz avanzada para desarrollo",
                "tipo": "tabs",
                "tabs": [
                    {"titulo": "Qué es", "contenido": ["Interfaz desktop para Claude", "Integración con VS Code", "Command palette", "Hotkeys productivos"]},
                    {"titulo": "Features", "contenido": ["Autocompletado de código", "Error detection", "Refactoring rápido", "Testing asistido"]},
                    {"titulo": "Instalación", "contenido": ["Descargar desde Anthropic", "Instalar extensión VS Code", "Configurar API key", "Primeros pasos"]}
                ]
            },
            {
                "id": "L8-2",
                "titulo": "Model Context Protocol (MCP)",
                "descripcion": "Protocolo para integrar herramientas",
                "tipo": "accordion",
                "acordeon": [
                    {"titulo": "Qué es MCP", "contenido": "Estándar abierto para conectar Claude con herramientas externas. APIs, DBs, servicios."},
                    {"titulo": "Cómo funciona", "contenido": "Claude envia mensajes a MCP. MCP ejecuta acciones. Devuelve resultados. Loop bidireccional."},
                    {"titulo": "Casos de uso", "contenido": "Acceso a datos en tiempo real. Ejecución de scripts. Integración con sistemas legacy. APIs personalizadas."},
                    {"titulo": "Crear MCP", "contenido": "Especificación abierta. Lenguaje agnóstico. Documentación disponible. Comunidad creciente."}
                ]
            },
            {
                "id": "L8-3",
                "titulo": "Recursos Importantes",
                "descripcion": "Links y documentación clave",
                "tipo": "accordion",
                "acordeon": [
                    {"titulo": "Documentación oficial", "contenido": "https://docs.anthropic.com - API reference, guías, ejemplos."},
                    {"titulo": "Comunidad y foros", "contenido": "Discourse, Reddit r/Claude, Discord oficial. Soporte comunitario."},
                    {"titulo": "Ejemplos de código", "contenido": "GitHub Anthropic. Repositorios públicos. Snippets compartidos."},
                    {"titulo": "Status y actualizaciones", "contenido": "Status page. Changelog. Blog oficial. Anuncios importantes."}
                ]
            },
            {
                "id": "L8-4",
                "titulo": "Proyecto Final",
                "descripcion": "Planifica tu proyecto integrador",
                "tipo": "pasos",
                "pasos": [
                    {"numero": 1, "titulo": "Define objetivo", "descripcion": "Qué problema resuelve. Impacto esperado. Criterios de éxito."},
                    {"numero": 2, "titulo": "Diseña arquitectura", "descripcion": "Flujos de datos. Componentes. Integraciones. Seguridad."},
                    {"numero": 3, "titulo": "Implementa MVP", "descripcion": "Versión mínima viable. Features core. Testing básico."},
                    {"numero": 4, "titulo": "Deploy y escala", "descripcion": "Producción. Monitoreo. Optimización. Feedback loop."}
                ]
            }
        ]
    },
    "M9": {
        "titulo": "Construye tu Proyecto",
        "color": "#059669",  # Verde
        "lecciones": [
            {
                "id": "L9-1",
                "titulo": "Proyecto: Setup Base",
                "descripcion": "Configuración inicial",
                "tipo": "pasos",
                "pasos": [
                    {"numero": 1, "titulo": "Estructura de proyecto", "descripcion": "Carpetas, archivos, dependencias."},
                    {"numero": 2, "titulo": "Configuración de env", "descripcion": "Variables de entorno. Secrets. Configuración."},
                    {"numero": 3, "titulo": "SDK instalado", "descripcion": "Dependencias declaradas. Funcionando localmente."},
                    {"numero": 4, "titulo": "First test", "descripcion": "Script de prueba. Conecta a API. Respuesta exitosa."}
                ]
            },
            {
                "id": "L9-2",
                "titulo": "Proyecto: Lógica Core",
                "descripcion": "Implementa funcionalidad principal",
                "tipo": "pasos",
                "pasos": [
                    {"numero": 1, "titulo": "Input processing", "descripcion": "Valida entrada de usuario. Normaliza datos."},
                    {"numero": 2, "titulo": "Claude integration", "descripcion": "Llama API. Maneja respuestas. Error handling."},
                    {"numero": 3, "titulo": "Output formatting", "descripcion": "Presenta resultados. Limpia datos. Estructura."},
                    {"numero": 4, "titulo": "Testing", "descripcion": "Casos de prueba. Edge cases. Assertions."}
                ]
            },
            {
                "id": "L9-3",
                "titulo": "Proyecto: Optimización",
                "descripcion": "Mejora rendimiento y UX",
                "tipo": "pasos",
                "pasos": [
                    {"numero": 1, "titulo": "Profiling", "descripcion": "Identifica cuellos de botella. Mide latencia."},
                    {"numero": 2, "titulo": "Caching", "descripcion": "Guarda resultados frecuentes. Redacta tiempo."},
                    {"numero": 3, "titulo": "Async operations", "descripcion": "Llamadas no bloqueantes. Mejor UX."},
                    {"numero": 4, "titulo": "Rate limiting", "descripcion": "Respeta limits. Backoff strategy. Graceful degradation."}
                ]
            },
            {
                "id": "L9-4",
                "titulo": "Proyecto: Deploy y Monitoreo",
                "descripcion": "Saca a producción",
                "tipo": "pasos",
                "pasos": [
                    {"numero": 1, "titulo": "Pre-deploy checklist", "descripcion": "Tests pasan. Secrets seguros. Docs actualizados."},
                    {"numero": 2, "titulo": "Deployment", "descripcion": "CI/CD pipeline. Staging test. Rollout controlado."},
                    {"numero": 3, "titulo": "Monitoreo", "descripcion": "Logs. Alertas. Métricas. Health checks."},
                    {"numero": 4, "titulo": "Post-launch", "descripcion": "Feedback user. Bugs fixes. Iteración continua."}
                ]
            },
            {
                "id": "L9-5",
                "titulo": "Proyecto: Casos Avanzados",
                "descripcion": "Features adicionales",
                "tipo": "pasos",
                "pasos": [
                    {"numero": 1, "titulo": "Multimodal features", "descripcion": "Integra imágenes. Procesa archivos. Vision capabilities."},
                    {"numero": 2, "titulo": "Agents y workflows", "descripcion": "Decisiones automáticas. Iteración interna. Tool use."},
                    {"numero": 3, "titulo": "Personalización", "descripcion": "System prompts dinámicos. Contexto del usuario. Memoria."},
                    {"numero": 4, "titulo": "Analytics", "descripcion": "Tracking de usage. Performance metrics. User insights."}
                ]
            },
            {
                "id": "L9-6",
                "titulo": "Proyecto: Showcase Final",
                "descripcion": "Comparte y celebra tu proyecto",
                "tipo": "pasos",
                "pasos": [
                    {"numero": 1, "titulo": "Documentación", "descripcion": "README. API docs. Examples. Troubleshooting."},
                    {"numero": 2, "titulo": "Demo público", "descripcion": "Live app. Ejemplos interactivos. Case study."},
                    {"numero": 3, "titulo": "Community sharing", "descripcion": "GitHub. Comunidades. Blog post. Showcase."},
                    {"numero": 4, "titulo": "Feedback y mejora", "descripcion": "Recolecta testimonios. Itera. Escala éxito."}
                ]
            }
        ]
    }
}

# ==================== COLORES POR MÓDULO ====================
MODULE_COLORS = {
    "M1": "#2563EB",  # Azul
    "M2": "#DC2626",  # Rojo
    "M3": "#7C3AED",  # Púrpura
    "M4": "#059669",  # Verde
    "M5": "#EA580C",  # Naranja
    "M6": "#06B6D4",  # Cian
    "M7": "#D97706",  # Ámbar
    "M8": "#7C3AED",  # Púrpura
    "M9": "#059669",  # Verde
}

# ==================== GENERADOR HTML ====================

def generate_html(lesson_id, lesson_data, module_id, module_color):
    """Genera HTML para una lección estilo Genially"""

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{lesson_id} - {lesson_data['titulo']}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz@0,9..144;1,9..144&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --color-primary: {module_color};
            --color-secondary: #F97316;
            --color-bg: #ffffff;
            --color-text: #1e293b;
            --color-text-light: #64748b;
            --color-border: #e2e8f0;
            --color-success: #10b981;
            --color-error: #ef4444;
        }}

        [data-theme="dark"] {{
            --color-bg: #0f172a;
            --color-text: #f1f5f9;
            --color-text-light: #cbd5e1;
            --color-border: #334155;
        }}

        html {{
            scroll-behavior: smooth;
        }}

        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--color-bg);
            color: var(--color-text);
            line-height: 1.6;
            transition: background-color 0.3s, color 0.3s;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0;
        }}

        /* ========== HEADER ========== */
        .lesson-header {{
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
            color: white;
            padding: 80px 60px;
            min-height: 400px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }}

        .lesson-header::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -10%;
            width: 500px;
            height: 500px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 50%;
            pointer-events: none;
        }}

        .lesson-header::after {{
            content: '';
            position: absolute;
            bottom: -30%;
            left: -5%;
            width: 400px;
            height: 400px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 50%;
            pointer-events: none;
        }}

        .header-content {{
            position: relative;
            z-index: 2;
        }}

        .lesson-badge {{
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 999px;
            font-size: 0.875rem;
            font-weight: 600;
            margin-bottom: 16px;
            backdrop-filter: blur(10px);
        }}

        .lesson-header h1 {{
            font-family: 'Fraunces', serif;
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 16px;
            line-height: 1.1;
            letter-spacing: -0.02em;
        }}

        .lesson-header p {{
            font-size: 1.25rem;
            max-width: 600px;
            opacity: 0.95;
            font-weight: 300;
        }}

        /* ========== SECCIONES ========== */
        .section {{
            padding: 100px 60px;
            margin: 0;
            border-bottom: 1px solid var(--color-border);
            opacity: 0;
            animation: fadeInUp 0.8s ease-out forwards;
        }}

        .section:nth-child(2) {{ animation-delay: 0.1s; }}
        .section:nth-child(3) {{ animation-delay: 0.2s; }}
        .section:nth-child(4) {{ animation-delay: 0.3s; }}
        .section:nth-child(5) {{ animation-delay: 0.4s; }}

        .section h2 {{
            font-family: 'Fraunces', serif;
            font-size: 2.5rem;
            margin-bottom: 48px;
            color: var(--color-primary);
            position: relative;
            padding-bottom: 20px;
        }}

        .section h2::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 80px;
            height: 4px;
            background: var(--color-primary);
            border-radius: 2px;
        }}

        /* ========== TABS ========== */
        .tabs {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}

        .tab-button {{
            padding: 16px 24px;
            border: 2px solid var(--color-border);
            background: var(--color-bg);
            color: var(--color-text);
            border-radius: 12px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.4s ease;
            font-size: 1rem;
        }}

        .tab-button:hover {{
            border-color: var(--color-primary);
            background: rgba(var(--color-primary), 0.05);
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
        }}

        .tab-button.active {{
            background: var(--color-primary);
            color: white;
            border-color: var(--color-primary);
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
        }}

        .tab-content {{
            display: none;
            padding: 40px;
            background: linear-gradient(135deg, rgba(var(--color-primary), 0.05) 0%, rgba(var(--color-secondary), 0.05) 100%);
            border-radius: 16px;
            margin-top: 20px;
            animation: fadeInUp 0.4s ease-out;
        }}

        .tab-content.active {{
            display: block;
        }}

        .tab-content ul {{
            list-style: none;
            display: grid;
            gap: 16px;
        }}

        .tab-content li {{
            padding: 16px 20px;
            background: white;
            border-left: 4px solid var(--color-primary);
            border-radius: 8px;
            position: relative;
            padding-left: 40px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }}

        .tab-content li::before {{
            content: '▪';
            position: absolute;
            left: 16px;
            color: var(--color-primary);
            font-weight: 700;
        }}

        /* ========== ACORDEÓN ========== */
        .accordion {{
            display: grid;
            gap: 16px;
        }}

        .accordion-item {{
            border: 2px solid var(--color-border);
            border-radius: 12px;
            overflow: hidden;
            transition: all 0.4s ease;
        }}

        .accordion-item:hover {{
            border-color: var(--color-primary);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        }}

        .accordion-header {{
            padding: 24px 32px;
            background: white;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: 600;
            transition: all 0.3s ease;
            user-select: none;
        }}

        .accordion-item.active .accordion-header {{
            background: rgba(var(--color-primary), 0.08);
            color: var(--color-primary);
        }}

        .accordion-toggle {{
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            transition: transform 0.3s ease;
        }}

        .accordion-item.active .accordion-toggle {{
            transform: rotate(180deg);
        }}

        .accordion-content {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.4s ease;
            background: var(--color-bg);
            border-top: 1px solid var(--color-border);
        }}

        .accordion-item.active .accordion-content {{
            max-height: 500px;
            padding: 24px 32px;
        }}

        .accordion-content p {{
            color: var(--color-text-light);
            line-height: 1.7;
        }}

        /* ========== PASOS ========== */
        .steps {{
            display: grid;
            gap: 32px;
        }}

        .step {{
            display: grid;
            grid-template-columns: 60px 1fr;
            gap: 32px;
            align-items: start;
        }}

        .step-number {{
            width: 60px;
            height: 60px;
            background: var(--color-primary);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: 700;
            flex-shrink: 0;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        }}

        .step-content h3 {{
            font-size: 1.5rem;
            margin-bottom: 8px;
            color: var(--color-primary);
        }}

        .step-content p {{
            color: var(--color-text-light);
            font-size: 1.05rem;
        }}

        /* ========== QUIZ ========== */
        .quiz {{
            background: linear-gradient(135deg, rgba(var(--color-primary), 0.1) 0%, rgba(var(--color-secondary), 0.1) 100%);
            padding: 40px;
            border-radius: 16px;
            margin-top: 60px;
        }}

        .quiz h3 {{
            font-size: 1.25rem;
            margin-bottom: 24px;
            color: var(--color-primary);
        }}

        .quiz-option {{
            padding: 16px 24px;
            background: white;
            border: 2px solid var(--color-border);
            border-radius: 8px;
            margin-bottom: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }}

        .quiz-option:hover {{
            border-color: var(--color-primary);
            background: rgba(var(--color-primary), 0.05);
        }}

        .quiz-option.selected {{
            background: var(--color-primary);
            color: white;
            border-color: var(--color-primary);
        }}

        .quiz-option.correct {{
            background: var(--color-success);
            color: white;
            border-color: var(--color-success);
        }}

        .quiz-option.incorrect {{
            background: var(--color-error);
            color: white;
            border-color: var(--color-error);
        }}

        /* ========== ANIMACIONES ========== */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes slideInLeft {{
            from {{
                opacity: 0;
                transform: translateX(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}

        /* ========== FOOTER ========== */
        .lesson-footer {{
            padding: 60px;
            text-align: center;
            background: linear-gradient(135deg, rgba(var(--color-primary), 0.05) 0%, rgba(var(--color-secondary), 0.05) 100%);
        }}

        .lesson-footer h3 {{
            font-family: 'Fraunces', serif;
            font-size: 2rem;
            margin-bottom: 24px;
            color: var(--color-primary);
        }}

        .nav-buttons {{
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-top: 32px;
        }}

        .btn {{
            padding: 14px 32px;
            border-radius: 8px;
            border: 2px solid var(--color-primary);
            background: var(--color-bg);
            color: var(--color-primary);
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 1rem;
        }}

        .btn:hover {{
            background: var(--color-primary);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
        }}

        .btn-primary {{
            background: var(--color-primary);
            color: white;
        }}

        .btn-primary:hover {{
            background: var(--color-secondary);
            border-color: var(--color-secondary);
        }}

        /* ========== RESPONSIVE ========== */
        @media (max-width: 768px) {{
            .lesson-header {{
                padding: 60px 30px;
            }}

            .lesson-header h1 {{
                font-size: 2.5rem;
            }}

            .section {{
                padding: 60px 30px;
            }}

            .section h2 {{
                font-size: 1.75rem;
            }}

            .tabs {{
                grid-template-columns: 1fr;
            }}

            .tab-content {{
                padding: 24px;
            }}

            .step {{
                grid-template-columns: 1fr;
            }}

            .step-number {{
                width: 50px;
                height: 50px;
                font-size: 1.2rem;
            }}
        }}

        @media (max-width: 480px) {{
            .lesson-header {{
                padding: 40px 20px;
                min-height: 300px;
            }}

            .lesson-header h1 {{
                font-size: 2rem;
            }}

            .section {{
                padding: 40px 20px;
            }}

            .section h2 {{
                font-size: 1.5rem;
            }}
        }}

        /* ========== DARK MODE FIXES ========== */
        [data-theme="dark"] .tab-button,
        [data-theme="dark"] .tab-content,
        [data-theme="dark"] .accordion-header,
        [data-theme="dark"] .quiz-option,
        [data-theme="dark"] .tab-content li {{
            background: #1e293b;
            color: var(--color-text);
            border-color: var(--color-border);
        }}

        [data-theme="dark"] .tab-content li {{
            border-left-color: var(--color-primary);
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <header class="lesson-header">
            <div class="header-content">
                <div class="lesson-badge">{lesson_id}</div>
                <h1>{lesson_data['titulo']}</h1>
                <p>{lesson_data['descripcion']}</p>
            </div>
        </header>
"""

    # Generar secciones según tipo
    if lesson_data['tipo'] == 'tabs':
        html += generate_tabs_section(lesson_data)
    elif lesson_data['tipo'] == 'acordeon' or lesson_data['tipo'] == 'accordion':
        html += generate_accordion_section(lesson_data)
    elif lesson_data['tipo'] == 'pasos':
        html += generate_steps_section(lesson_data)
    elif lesson_data['tipo'] == 'cards':
        html += generate_cards_section(lesson_data)
    elif lesson_data['tipo'] == 'carousel':
        html += generate_carousel_section(lesson_data)

    # Agregar quiz si existe
    if 'quiz' in lesson_data and lesson_data['quiz']:
        html += generate_quiz_section(lesson_data['quiz'])

    # FOOTER
    html += """
        <footer class="lesson-footer">
            <h3>¡Excelente trabajo!</h3>
            <p>Has completado esta lección. Continúa con la siguiente para profundizar tu conocimiento.</p>
            <div class="nav-buttons">
                <button class="btn" onclick="history.back()">← Anterior</button>
                <button class="btn btn-primary" onclick="window.location.href='../course.html'">Ver curso</button>
            </div>
        </footer>
    </div>

    <script>
        // ========== DARK MODE TOGGLE ==========
        document.addEventListener('DOMContentLoaded', () => {{
            const theme = localStorage.getItem('theme') || 'light';
            document.documentElement.setAttribute('data-theme', theme);

            // Tab switching
            document.querySelectorAll('.tab-button').forEach(button => {{
                button.addEventListener('click', (e) => {{
                    const tabs = button.parentElement.parentElement;
                    tabs.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
                    tabs.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

                    button.classList.add('active');
                    const contentId = button.getAttribute('data-tab');
                    document.getElementById(contentId)?.classList.add('active');
                }});
            }});

            // Accordion toggle
            document.querySelectorAll('.accordion-header').forEach(header => {{
                header.addEventListener('click', () => {{
                    const item = header.parentElement;
                    const otherItems = item.parentElement.querySelectorAll('.accordion-item');

                    otherItems.forEach(i => {{
                        if (i !== item) i.classList.remove('active');
                    }});

                    item.classList.toggle('active');
                }});
            }});

            // Quiz handling
            document.querySelectorAll('.quiz-option').forEach(option => {{
                option.addEventListener('click', () => {{
                    const quizItem = option.parentElement;
                    const correctIndex = parseInt(quizItem.getAttribute('data-correct'));
                    const selectedIndex = Array.from(quizItem.querySelectorAll('.quiz-option')).indexOf(option);

                    quizItem.querySelectorAll('.quiz-option').forEach((o, idx) => {{
                        o.classList.remove('selected', 'correct', 'incorrect');
                        if (idx === correctIndex) o.classList.add('correct');
                        if (idx === selectedIndex && idx !== correctIndex) o.classList.add('incorrect');
                    }});

                    option.classList.add('selected');
                }});
            }});
        }});
    </script>
</body>
</html>
"""

    return html


def generate_tabs_section(lesson_data):
    """Genera HTML para sección con tabs"""
    html = '<section class="section">'

    tabs = lesson_data.get('tabs', [])
    html += f'<div class="tabs">'

    for idx, tab in enumerate(tabs):
        active = 'active' if idx == 0 else ''
        html += f'<button class="tab-button {active}" data-tab="tab-{idx}">{tab["titulo"]}</button>'

    html += '</div>'

    for idx, tab in enumerate(tabs):
        active = 'active' if idx == 0 else ''
        html += f'<div class="tab-content {active}" id="tab-{idx}"><ul>'

        for item in tab.get('contenido', []):
            html += f'<li>{item}</li>'

        html += '</ul></div>'

    html += '</section>'
    return html


def generate_accordion_section(lesson_data):
    """Genera HTML para sección con acordeón"""
    html = '<section class="section"><div class="accordion">'

    accordion_items = lesson_data.get('acordeon', [])

    for idx, item in enumerate(accordion_items):
        active = 'active' if idx == 0 else ''
        html += f'''
        <div class="accordion-item {active}">
            <div class="accordion-header">
                <span>{item.get('titulo', '')}</span>
                <span class="accordion-toggle">▼</span>
            </div>
            <div class="accordion-content">
                <p>{item.get('contenido', '')}</p>
            </div>
        </div>
        '''

    html += '</div></section>'
    return html


def generate_steps_section(lesson_data):
    """Genera HTML para sección con pasos"""
    html = '<section class="section"><div class="steps">'

    steps = lesson_data.get('pasos', [])

    for step in steps:
        html += f'''
        <div class="step">
            <div class="step-number">{step.get('numero', '')}</div>
            <div class="step-content">
                <h3>{step.get('titulo', '')}</h3>
                <p>{step.get('descripcion', '')}</p>
            </div>
        </div>
        '''

    html += '</div></section>'
    return html


def generate_cards_section(lesson_data):
    """Genera HTML para sección con cards"""
    html = '<section class="section"><div class="accordion">'

    cards = lesson_data.get('cards', [])

    for idx, card in enumerate(cards):
        active = 'active' if idx == 0 else ''
        html += f'''
        <div class="accordion-item {active}">
            <div class="accordion-header">
                <span>{card.get('titulo', '')}</span>
                <span class="accordion-toggle">▼</span>
            </div>
            <div class="accordion-content">
                <p>{card.get('descripcion', '')}</p>
            </div>
        </div>
        '''

    html += '</div></section>'
    return html


def generate_carousel_section(lesson_data):
    """Genera HTML para sección con carousel (como tabs)"""
    html = '<section class="section">'

    casos = lesson_data.get('casos', [])
    html += f'<div class="tabs">'

    for idx, caso in enumerate(casos):
        active = 'active' if idx == 0 else ''
        html += f'<button class="tab-button {active}" data-tab="caso-{idx}">{caso["titulo"]}</button>'

    html += '</div>'

    for idx, caso in enumerate(casos):
        active = 'active' if idx == 0 else ''
        html += f'<div class="tab-content {active}" id="caso-{idx}"><ul><li>{caso.get("descripcion", "")}</li></ul></div>'

    html += '</section>'
    return html


def generate_quiz_section(quiz_items):
    """Genera HTML para sección de quiz"""
    html = '<section class="section"><div class="quiz"><h3>Prueba tu conocimiento</h3>'

    for idx, q in enumerate(quiz_items):
        html += f'<div class="quiz-item" data-correct="{q.get("respuesta", 0)}">'
        html += f'<h4 style="margin-bottom: 16px; font-size: 1.1rem;">{q.get("pregunta", "")}</h4>'

        for opt_idx, option in enumerate(q.get('opciones', [])):
            html += f'<div class="quiz-option">{option}</div>'

        html += '</div>'

    html += '</div></section>'
    return html


def main():
    """Función principal para generar todas las lecciones"""
    # Detectar ruta correcta (session o host)
    test_paths = [
        '/Users/martadeangulo/claude-101-platform/public/claude-101-videos',
        '/sessions/wonderful-admiring-faraday/mnt/claude-101-platform/public/claude-101-videos',
    ]

    output_dir = None
    for path in test_paths:
        p = Path(path)
        if path.startswith('/sessions'):
            output_dir = p
            break
        elif Path('/Users/martadeangulo/claude-101-platform').exists():
            output_dir = Path('/Users/martadeangulo/claude-101-platform/public/claude-101-videos')
            break

    if output_dir is None:
        output_dir = Path('/sessions/wonderful-admiring-faraday/mnt/claude-101-platform/public/claude-101-videos')

    output_dir.mkdir(parents=True, exist_ok=True)

    print("Generando lecciones estilo Genially...")
    print("=" * 60)

    lesson_count = 0

    for module_id, module_data in LESSONS_CONFIG.items():
        module_color = MODULE_COLORS[module_id]
        lecciones = module_data.get('lecciones', [])

        print(f"\n{module_id}: {module_data['titulo']}")
        print(f"  Color: {module_color}")
        print(f"  Lecciones: {len(lecciones)}")

        for lesson in lecciones:
            lesson_id = lesson['id']
            filename = f"{lesson_id}-slides.html"
            filepath = output_dir / filename

            # Generar HTML
            html_content = generate_html(lesson_id, lesson, module_id, module_color)

            # Guardar archivo
            filepath.write_text(html_content, encoding='utf-8')

            lesson_count += 1
            print(f"    ✓ {lesson_id}: {lesson['titulo']}")

    print("\n" + "=" * 60)
    print(f"HECHO: {lesson_count} lecciones generadas")
    print(f"Ubicación: {output_dir}")


if __name__ == '__main__':
    main()
