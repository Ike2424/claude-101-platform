#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera slides REALES (con valor de contenido) para los modulos M3-M9 del curso
Claude 101, reutilizando exactamente el motor de render de L1-1-slides.html.

- Lee L1-1-slides.html como plantilla (estilos + JS de render intactos).
- Sustituye: titulo, etiqueta de modulo/leccion, color de modulo, storage key,
  contador de slides y el array `const slides`.
- Escribe public/claude-101-videos/Lx-y-slides.html para cada leccion.

Tipos de slide soportados por el motor: intro, content, example,
interactive_quiz, challenge, matching_game, badge.
"""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SLIDES_DIR = REPO / "public" / "claude-101-videos"
TEMPLATE = SLIDES_DIR / "L1-1-slides.html"

# Metadatos por modulo: (titulo, etiqueta corta para el eyebrow, color hex)
MODULES = {
    1: ("Bienvenida y fundamentos", "Fundamentos", "#3B82F6"),
    2: ("Primeros pasos", "Modelos", "#10B981"),
    3: ("El arte del prompt", "Prompting", "#A855F7"),
    4: ("Tecnicas avanzadas de prompting", "Prompting Pro", "#6366F1"),
    5: ("Capacidades y herramientas", "Herramientas", "#059669"),
    6: ("Casos de uso practicos", "Casos de uso", "#EA580C"),
    7: ("Buenas practicas y limites", "Buenas practicas", "#DC2626"),
    8: ("Siguiente nivel", "Siguiente nivel", "#06B6D4"),
    9: ("Desarrollo avanzado con Claude", "Avanzado", "#7C3AED"),
}

# Helpers para construir slides de forma compacta
def intro():
    return {"type": "intro", "points": 0}

def content(title, text):
    return {"type": "content", "title": title, "text": text, "points": 10}

def example(title, code):
    return {"type": "example", "title": title, "code": code, "points": 15}

def quiz(title, question, options):
    # options: lista de tuplas (texto, correcto: bool, razon)
    opts = []
    for text, ok, reason in options:
        opts.append({"text": text, "correct": ok, "reason": reason,
                     "points": 20 if ok else 0})
    return {"type": "interactive_quiz", "title": title, "question": question,
            "options": opts, "points": 20}

def challenge(title, instruction, answer, hint):
    return {"type": "challenge", "title": title, "instruction": instruction,
            "answer": answer, "hint": hint, "points": 25}

def matching(title, pairs):
    return {"type": "matching_game", "title": title,
            "pairs": [{"left": l, "right": r, "points": 15} for l, r in pairs]}

def badge(name, description):
    return {"type": "badge", "name": name, "description": description}


# ---------------------------------------------------------------------------
# CONTENIDO POR LECCION
# clave -> (modulo, leccion, titulo, [slides])
# ---------------------------------------------------------------------------
LESSONS = {}

# ============================ MODULO 1 =====================================
LESSONS["L1-2"] = (1, 2, "La familia de modelos", [
    intro(),
    content("Una familia, no un solo modelo",
        "Claude no es un unico modelo: es una familia con distintos tamanos pensados para distintas necesidades.\n\n"
        "Los tres perfiles clasicos son Haiku, Sonnet y Opus. La idea: elegir el equilibrio justo entre velocidad, capacidad y costo para cada tarea."),
    content("Haiku: rapido y ligero",
        "El mas veloz y economico de la familia.\n\n"
        "Ideal para:\n• Tareas simples y de alto volumen\n• Clasificacion, extraccion, respuestas cortas\n• Cuando la latencia importa mas que el matiz\n\n"
        "Piensa en el para automatizaciones que corren muchas veces."),
    content("Sonnet: el equilibrio (el que mas usaras)",
        "El punto medio entre velocidad y capacidad. Para la mayoria de la gente es el modelo del dia a dia.\n\n"
        "Ideal para:\n• Redaccion y analisis general\n• Programacion cotidiana\n• Tareas que requieren buen razonamiento sin esperar demasiado\n\n"
        "Regla practica: empieza por Sonnet y sube o baja solo si lo necesitas."),
    content("Opus: la maxima capacidad",
        "El mas potente para problemas complejos.\n\n"
        "Ideal para:\n• Razonamiento profundo y multi-paso\n• Analisis matizado y escritura sofisticada\n• Tareas donde la calidad pesa mas que el costo o la velocidad\n\n"
        "Usalo cuando Sonnet se queda corto en complejidad."),
    content("Como elegir el modelo correcto",
        "Preguntate:\n• Es una tarea simple y repetitiva? -> Haiku\n• Es trabajo general del dia a dia? -> Sonnet\n• Es muy compleja y la calidad es critica? -> Opus\n\n"
        "No siempre el mas grande es el mejor: el adecuado es el que resuelve tu tarea al menor costo y tiempo."),
    quiz("Cual modelo para alto volumen simple?",
        "Necesitas clasificar miles de mensajes cortos lo mas rapido y barato posible. Cual eliges?",
        [("Haiku", True, "Correcto: el mas rapido y economico, ideal para volumen simple."),
         ("Opus", False, "Seria potente pero lento y caro para una tarea simple."),
         ("Ninguno sirve", False, "Haiku encaja perfecto en este caso.")]),
    quiz("Cual es el modelo 'por defecto'?",
        "Para el trabajo general del dia a dia, por cual conviene empezar?",
        [("Opus siempre", False, "Suele ser excesivo para tareas cotidianas."),
         ("Sonnet", True, "Correcto: el mejor equilibrio para la mayoria de tareas."),
         ("Haiku para todo", False, "Haiku se queda corto en razonamiento complejo.")]),
    challenge("Reto: el equilibrado",
        "Cual de los tres modelos es el equilibrio recomendado para el dia a dia? (una palabra)",
        "Sonnet", "Sonnet es el punto medio entre velocidad y capacidad."),
    matching("Modelo y perfil",
        [("Haiku", "Rapido y economico"),
         ("Sonnet", "Equilibrio del dia a dia"),
         ("Opus", "Maxima capacidad"),
         ("Criterio", "La tarea decide")]),
    content("Resumen",
        "Haiku para lo simple y veloz, Sonnet para lo general, Opus para lo complejo.\n\n"
        "Elige por la tarea, no por defecto el mas grande. En la siguiente leccion vemos como razona Claude por dentro."),
    badge("🧬 Conocedor de Modelos", "Sabes elegir entre Haiku, Sonnet y Opus segun la tarea."),
])

LESSONS["L1-3"] = (1, 3, "Como razona Claude", [
    intro(),
    content("Predice, no consulta",
        "Claude genera texto prediciendo, palabra a palabra, lo mas probable segun los patrones que aprendio en su entrenamiento.\n\n"
        "No consulta una base de datos ni 'busca' la respuesta: la construye. Por eso es tan flexible... y por eso a veces se equivoca."),
    content("Que es 'alucinar'",
        "Una alucinacion es cuando Claude da una respuesta que suena segura pero es falsa.\n\n"
        "Ocurre mas en:\n• Cifras y datos muy especificos\n• Citas, fechas y nombres propios\n• Temas fuera de su conocimiento\n\n"
        "La seguridad del tono no garantiza que tenga razon: verifica lo critico."),
    content("Puede pensar paso a paso",
        "En problemas complejos, Claude rinde mejor si razona antes de responder.\n\n"
        "Pedir 'piensa paso a paso' le hace descomponer el problema, mostrar calculos intermedios y llegar a conclusiones mas fiables.\n\n"
        "Lo veras en profundidad en el modulo de tecnicas avanzadas."),
    content("Probabilidad = variabilidad",
        "Como genera por probabilidades, la misma pregunta puede dar respuestas algo distintas cada vez.\n\n"
        "Eso es normal y a veces util (variedad creativa). Para tareas que exigen consistencia, da instrucciones muy precisas y formato fijo."),
    example("Hacer que razone en voz alta",
        "Resuelve este problema paso a paso, mostrando cada calculo,\n"
        "y solo al final escribe la respuesta:\n\n"
        "Si un articulo cuesta 80€ y le aplico +25% y luego -10%,\n"
        "cual es el precio final?"),
    quiz("Como genera Claude sus respuestas?",
        "Cual descripcion es la correcta?",
        [("Busca la respuesta en internet", False, "No navega por defecto; predice el texto."),
         ("Predice el texto mas probable segun patrones aprendidos", True, "Correcto: genera por probabilidad, no por consulta."),
         ("Copia de una base de datos fija", False, "No copia de una base de datos; construye la respuesta.")]),
    challenge("Reto: el termino clave",
        "Como se llama cuando Claude responde con seguridad algo que es falso? (una palabra)",
        "alucinacion", "Se llama alucinacion (hallucination)."),
    matching("Como razona",
        [("Genera por", "Probabilidad"),
         ("Alucinacion", "Seguro pero falso"),
         ("Mejor en complejo", "Paso a paso"),
         ("Misma pregunta", "Puede variar")]),
    badge("🧠 Mente de Claude", "Entiendes como razona Claude, por que alucina y como guiarlo."),
])

LESSONS["L1-4"] = (1, 4, "Diferencias clave con otros asistentes", [
    intro(),
    content("No todos los asistentes son iguales",
        "Aunque muchos asistentes de IA se parecen por fuera, su comportamiento difiere segun como fueron entrenados.\n\n"
        "Claude tiene varios rasgos que lo distinguen en el dia a dia."),
    content("Estilo mas natural",
        "Claude tiende a escribir de forma mas natural y menos formulaica.\n\n"
        "Menos plantillas rigidas, menos 'como modelo de lenguaje...'; mas un texto que suena a redaccion humana cuidada."),
    content("Honestidad calibrada",
        "En lugar de proyectar falsa certeza, Claude tiende a reconocer lo que no sabe y a senalar sus suposiciones.\n\n"
        "Tambien razona los matices en temas sensibles en vez de bloquear cualquier tema de golpe. Lo veras a fondo en el modulo 9 BONUS."),
    content("Excelente en contextos largos",
        "Claude mantiene la coherencia en documentos extensos: puedes pegar muchas paginas y seguir obteniendo respuestas consistentes.\n\n"
        "Esto lo hace fuerte para analizar informes, contratos y bases de codigo completas."),
    quiz("Cual es una ventaja de Claude?",
        "Cual de estas describe mejor un rasgo distintivo de Claude?",
        [("Tiene siempre razon", False, "Ningun modelo garantiza exactitud total."),
         ("Estilo natural y honestidad sobre lo que no sabe", True, "Correcto: redaccion natural y honestidad calibrada lo distinguen."),
         ("Nunca necesita contexto", False, "Como todos, rinde mejor con buen contexto.")]),
    challenge("Reto: rasgo distintivo",
        "Claude mantiene coherencia en documentos ___ (una palabra: cortos o largos).",
        "largos", "Destaca en contextos largos manteniendo la coherencia."),
    matching("Diferencias de Claude",
        [("Estilo", "Natural, no formulaico"),
         ("Honestidad", "Reconoce lo que no sabe"),
         ("Temas sensibles", "Razona matices"),
         ("Fortaleza", "Contextos largos")]),
    badge("🆚 Experto Comparativo", "Conoces que distingue a Claude de otros asistentes."),
])

# ============================ MODULO 2 =====================================
LESSONS["L2-2"] = (2, 2, "Anatomia de la interfaz", [
    intro(),
    content("Conoce tu espacio de trabajo",
        "Saber donde esta cada cosa te hace mas rapido. La interfaz de Claude.ai se organiza en pocas zonas claras.\n\n"
        "Las principales: el area de conversacion, el cuadro de mensaje, el historial de chats y los ajustes."),
    content("El area de conversacion",
        "Es el centro: aqui aparecen tus mensajes y las respuestas de Claude.\n\n"
        "• Se lee de arriba (mas antiguo) a abajo (mas reciente)\n• Los Artifacts (documentos, codigo) pueden abrirse en un panel aparte\n• Puedes copiar respuestas o regenerar si no te convencen"),
    content("El cuadro de mensaje",
        "Donde escribes. Aqui tambien puedes:\n• Adjuntar imagenes o archivos\n• Pegar texto largo para que Claude lo analice\n• Enviar con Enter (y salto de linea con Shift+Enter)\n\n"
        "Es tu punto de entrada para todo."),
    content("Historial y organizacion",
        "• Cada conversacion se guarda en el historial lateral\n• Puedes renombrarlas para encontrarlas despues\n• Inicia un chat nuevo para temas distintos: mantiene el contexto limpio\n\n"
        "Un historial ordenado te ahorra tiempo a futuro."),
    quiz("Donde se analiza un archivo que subes?",
        "Subes un PDF para que lo resuma. Donde interactuas principalmente?",
        [("En el cuadro de mensaje lo adjuntas y conversas sobre el", True, "Correcto: adjuntas en el cuadro de mensaje y trabajas en la conversacion."),
         ("En los ajustes de la cuenta", False, "Los ajustes no procesan archivos."),
         ("No se puede subir archivos", False, "Si se pueden adjuntar archivos e imagenes.")]),
    challenge("Reto: atajo util",
        "Que tecla combinas con Enter para hacer un salto de linea sin enviar? (una palabra)",
        "Shift", "Shift+Enter inserta salto de linea sin enviar el mensaje."),
    matching("Zonas de la interfaz",
        [("Conversacion", "Mensajes y respuestas"),
         ("Cuadro de mensaje", "Escribir y adjuntar"),
         ("Historial", "Chats guardados"),
         ("Chat nuevo", "Contexto limpio")]),
    badge("🧭 Guia de la Interfaz", "Te mueves con soltura por la interfaz de Claude."),
])

LESSONS["L2-3"] = (2, 3, "Conversaciones, proyectos y estilos", [
    intro(),
    content("Tres formas de organizar tu trabajo",
        "Claude ofrece herramientas para que tu trabajo no sea un caos de chats sueltos: conversaciones, proyectos y estilos.\n\n"
        "Usarlas bien marca la diferencia entre improvisar y tener un sistema."),
    content("Conversaciones",
        "Cada chat es una conversacion independiente con su propio contexto.\n\n"
        "• Agrupa un tema en un mismo hilo\n• Abre uno nuevo para asuntos distintos\n• Renombralos para reencontrarlos\n\n"
        "Mantener hilos enfocados mejora las respuestas."),
    content("Proyectos",
        "Un proyecto es un espacio que agrupa conversaciones y guarda contexto reutilizable (instrucciones, documentos de referencia).\n\n"
        "Ideal cuando trabajas de forma recurrente en lo mismo: Claude 'recuerda' el contexto del proyecto en cada chat dentro de el."),
    content("Estilos",
        "Los estilos definen como responde Claude: tono, formato y nivel de detalle.\n\n"
        "• Puedes elegir estilos predefinidos o crear el tuyo\n• Util para mantener una voz consistente (tu marca, tu forma de escribir)\n\n"
        "Define una vez el estilo y se aplica a tus respuestas."),
    quiz("Que usar para contexto reutilizable?",
        "Trabajas cada semana sobre el mismo cliente con documentos fijos. Que conviene usar?",
        [("Un chat nuevo cada vez sin mas", False, "Perderias el contexto una y otra vez."),
         ("Un proyecto que guarde el contexto", True, "Correcto: los proyectos conservan instrucciones y documentos reutilizables."),
         ("Cambiar de cuenta", False, "No tiene sentido para este caso.")]),
    challenge("Reto: la voz consistente",
        "Que funcion define el tono y formato de las respuestas de Claude? (una palabra)",
        "estilos", "Los estilos (o estilo) controlan tono, formato y detalle."),
    matching("Organizacion",
        [("Conversacion", "Un tema, un hilo"),
         ("Proyecto", "Contexto reutilizable"),
         ("Estilo", "Tono y formato"),
         ("Chat nuevo", "Tema distinto")]),
    badge("🗂️ Organizador Pro", "Usas conversaciones, proyectos y estilos para trabajar con sistema."),
])

LESSONS["L2-4"] = (2, 4, "Configuracion esencial", [
    intro(),
    content("Ajusta Claude a tu medida",
        "Unos minutos en los ajustes mejoran toda tu experiencia. Vale la pena revisar las opciones clave una vez."),
    content("Perfil e instrucciones personales",
        "Puedes darle a Claude contexto sobre ti que aplique a todas las conversaciones:\n• Como te llamas y a que te dedicas\n• Tu idioma y tono preferido\n• Como te gusta recibir las respuestas\n\n"
        "Asi no repites lo mismo en cada chat."),
    content("Privacidad y datos",
        "Revisa la configuracion de datos de tu cuenta:\n• Que se guarda y como\n• Opciones sobre el uso de tus conversaciones\n• Politica de tu organizacion si usas una cuenta de trabajo\n\n"
        "Conocer estos ajustes te da control sobre tu informacion."),
    content("Apariencia y accesibilidad",
        "• Tema claro/oscuro segun tu comodidad visual\n• Tamano de texto si tu plataforma lo permite\n\n"
        "Pequenos ajustes que reducen la fatiga en sesiones largas."),
    content("Plan y limites",
        "Conoce tu plan:\n• Que modelos y funciones incluye\n• Limites de uso si los hay\n\n"
        "Saber tus limites te ayuda a planificar tareas grandes sin sorpresas."),
    quiz("Para que sirven las instrucciones personales?",
        "Que ventaja dan las instrucciones de perfil?",
        [("Aplican contexto sobre ti a todas las conversaciones", True, "Correcto: evitan repetir tu contexto en cada chat."),
         ("Hacen el modelo mas rapido", False, "No afectan la velocidad."),
         ("Borran el historial", False, "No tienen que ver con borrar chats.")]),
    challenge("Reto: comodidad visual",
        "Que ajuste cambias para reducir la fatiga visual de noche: el ___ oscuro. (una palabra)",
        "tema", "El tema oscuro (modo oscuro) ayuda en sesiones nocturnas."),
    matching("Configuracion",
        [("Instrucciones", "Contexto sobre ti"),
         ("Privacidad", "Control de datos"),
         ("Apariencia", "Tema y texto"),
         ("Plan", "Modelos y limites")]),
    badge("⚙️ Configurador Experto", "Tienes Claude ajustado a tu medida: perfil, privacidad y plan."),
])

# ============================ MODULO 3 =====================================
LESSONS["L3-1"] = (3, 1, "Anatomia de un buen prompt", [
    intro(),
    content("Las 4 partes de un buen prompt",
        "Un prompt solido casi siempre tiene estos cuatro ingredientes:\n\n"
        "Rol o contexto\n• Quien debe \"ser\" Claude y para quien escribe\n• Ej: \"Eres un editor experto en textos legales\"\n\n"
        "Tarea explicita\n• Que quieres exactamente, en un verbo claro\n• \"Resume\", \"Reescribe\", \"Clasifica\", \"Compara\"\n\n"
        "Contexto y datos\n• El material sobre el que trabaja\n• Documentos, ejemplos, restricciones\n\n"
        "Formato de salida\n• Como quieres la respuesta: lista, tabla, JSON, 3 parrafos"),
    content("Por que funciona la estructura",
        "Claude no adivina tu intencion: responde a lo que escribes.\n\n"
        "Un prompt vago produce una respuesta vaga. Un prompt estructurado reduce la ambiguedad y te da resultados repetibles.\n\n"
        "Regla mental:\n• Si un humano nuevo no podria hacer la tarea solo con tu texto, a Claude tambien le faltara informacion.\n• Anade el contexto que tu das por sentado pero el modelo no conoce."),
    example("Plantilla reutilizable",
        "Rol: Eres un asistente de marketing B2B.\n\n"
        "Tarea: Escribe 3 asuntos de email para una campana de reactivacion.\n\n"
        "Contexto:\n- Producto: software de facturacion para pymes\n- Audiencia: clientes inactivos hace 90 dias\n- Tono: cercano, sin sonar desesperado\n\n"
        "Formato: lista numerada, max 8 palabras cada asunto."),
    content("De lo generico a lo especifico",
        "Comparacion directa:\n\n"
        "Generico\n• \"Escribeme algo sobre productividad\"\n• Resultado: texto plano, impredecible\n\n"
        "Especifico\n• \"Escribe 5 consejos de productividad para trabajadores remotos con hijos, en tono empatico, una frase cada uno\"\n• Resultado: util y listo para usar\n\n"
        "Cada detalle que anades es una decision que Claude ya no tiene que adivinar."),
    quiz("Detecta el ingrediente que falta",
        "\"Reescribe este parrafo para que sea mas claro.\" Que le falta a este prompt para ser excelente?",
        [("Esta perfecto asi", False, "Le falta contexto: para quien, que tono, que longitud."),
         ("Falta el formato/tono y la audiencia", True, "Correcto: definir audiencia y formato hace la salida util y predecible."),
         ("Falta decir que use IA", False, "Eso es irrelevante; el modelo ya es la IA.")]),
    content("Trucos que elevan cualquier prompt",
        "• Pon las instrucciones al principio y el material despues\n"
        "• Usa delimitadores: comillas triples, ### o etiquetas para separar el texto a procesar\n"
        "• Pide un solo entregable por prompt\n"
        "• Si la tarea es compleja, pide que piense paso a paso (lo veremos en M4)\n"
        "• Da un ejemplo del resultado ideal cuando puedas"),
    challenge("Reto: cuenta los ingredientes",
        "Cuantos de los 4 ingredientes basicos (rol, tarea, contexto, formato) tiene este prompt: \"Eres un nutricionista. Crea un menu semanal vegetariano de 1800 kcal en formato tabla\"?",
        "4", "Busca: rol (nutricionista), tarea (crear menu), contexto (vegetariano, 1800 kcal) y formato (tabla)."),
    matching("Conecta concepto y definicion",
        [("Rol", "Quien debe ser Claude"),
         ("Tarea", "El verbo de lo que pides"),
         ("Contexto", "Datos y restricciones"),
         ("Formato", "Como quieres la respuesta"),
         ("Delimitadores", "Separan instruccion de material")]),
    content("Resumen de la leccion",
        "Un buen prompt = rol + tarea + contexto + formato.\n\n"
        "Antes de enviar, preguntate: que estoy dando por sentado que Claude no sabe?\n\n"
        "En las siguientes lecciones profundizamos en contexto, ejemplos reales y los errores mas comunes."),
    badge("🎯 Arquitecto de Prompts", "Dominas la anatomia de un buen prompt: rol, tarea, contexto y formato."),
])

LESSONS["L3-2"] = (3, 2, "Contexto, claridad y especificidad", [
    intro(),
    content("Mas contexto, mejores respuestas",
        "El contexto es la informacion de fondo que Claude necesita para responder bien.\n\n"
        "Sin contexto, Claude usa supuestos genericos. Con contexto, ajusta el tono, el nivel tecnico y el enfoque a TU situacion.\n\n"
        "Tipos de contexto utiles:\n• Quien eres tu y quien es la audiencia\n• El objetivo real detras de la tarea\n• Restricciones (longitud, tono, lo que NO quieres)\n• Ejemplos de lo que consideras bueno"),
    content("Claridad: una idea, una instruccion",
        "La claridad evita que Claude interprete mal.\n\n"
        "• Usa lenguaje directo, no rodeos\n• Una tarea principal por prompt\n• Evita palabras ambiguas como \"mejoralo\" sin decir en que sentido\n• Si hay pasos, numeralos\n\n"
        "Ambiguo: \"Hazlo mas profesional\"\nClaro: \"Reemplaza el lenguaje coloquial por terminos formales y quita las exclamaciones\""),
    content("Especificidad: el nivel de detalle correcto",
        "Ser especifico no es escribir mas, es escribir lo que importa.\n\n"
        "Variables que conviene fijar:\n• Longitud: \"3 frases\", \"200 palabras\", \"1 pagina\"\n• Audiencia: \"para directivos sin perfil tecnico\"\n• Tono: \"cercano\", \"neutro\", \"academico\"\n• Estructura: \"intro, 3 puntos y cierre\"\n\n"
        "Cada variable que fijas reduce el rango de respuestas posibles."),
    example("Antes y despues con contexto",
        "# Antes (poco contexto)\nEscribe un correo de disculpa al cliente.\n\n"
        "# Despues (con contexto)\nContexto: somos una tienda online; el pedido llego 5 dias tarde\npor un error nuestro de logistica. El cliente es recurrente.\n\n"
        "Tarea: escribe un correo de disculpa.\nTono: sincero, sin excusas, ofreciendo un 15% de descuento.\nFormato: max 120 palabras, con asunto."),
    quiz("Elige la version mas clara",
        "Cual instruccion dara resultados mas predecibles?",
        [("Hazme un resumen bonito", False, "\"Bonito\" es subjetivo; no define longitud ni formato."),
         ("Resume en 5 vinetas, una frase cada una, para un lector sin tiempo", True, "Correcto: define formato, longitud y audiencia."),
         ("Resume eso", False, "No dice como ni para quien.")]),
    content("El peligro de los supuestos",
        "Claude rellena los huecos con supuestos razonables, pero pueden no ser los tuyos.\n\n"
        "Ejemplos de huecos comunes:\n• Idioma de la respuesta\n• Publico objetivo\n• Nivel de formalidad\n• Si quieres explicacion o solo el resultado\n\n"
        "Solucion: explicita lo que para ti es obvio. El modelo no esta en tu cabeza."),
    challenge("Reto: anade especificidad",
        "Que palabra clave falta en \"Escribe un post\" para fijar el canal? (responde con UNA palabra que indique donde se publica, ej: para LinkedIn)",
        "LinkedIn", "Cualquier red/plataforma vale como ejemplo; lo que importa es fijar el canal/audiencia."),
    matching("Vago vs especifico",
        [("\"Hazlo corto\"", "Ambiguo"),
         ("\"Max 100 palabras\"", "Especifico"),
         ("\"Tono pro\"", "Ambiguo"),
         ("\"Formal, sin jerga\"", "Especifico")]),
    badge("🔍 Maestro del Contexto", "Sabes dar contexto, claridad y especificidad para respuestas predecibles."),
])

LESSONS["L3-3"] = (3, 3, "Ejemplos practicos: antes y despues", [
    intro(),
    content("Por que comparar antes y despues",
        "La forma mas rapida de aprender prompting es ver el mismo objetivo escrito mal y bien.\n\n"
        "En esta leccion repasamos casos reales de tareas cotidianas y veras como pequenos cambios disparan la calidad."),
    content("Caso 1: Email de trabajo",
        "ANTES\n• \"Escribe un email pidiendo el reporte\"\n\n"
        "DESPUES\n• \"Escribe un email a mi companero Luis pidiendo el reporte de ventas de mayo. Lo necesito antes del viernes. Tono amable pero claro, max 80 palabras, con asunto.\"\n\n"
        "El segundo da algo listo para enviar; el primero, un borrador generico."),
    content("Caso 2: Resumen de documento",
        "ANTES\n• \"Resume esto\" + pegas 10 paginas\n\n"
        "DESPUES\n• \"Resume el siguiente informe en 5 puntos clave para un directivo. Destaca riesgos y decisiones pendientes. Texto: <<< ... >>>\"\n\n"
        "Definir audiencia (directivo) y foco (riesgos/decisiones) cambia por completo el resumen."),
    content("Caso 3: Ayuda con codigo",
        "ANTES\n• \"Mi codigo no funciona, ayuda\"\n\n"
        "DESPUES\n• \"Esta funcion en Python deberia devolver la suma de pares pero da error. Pega el codigo + el mensaje de error. Explica la causa y dame la version corregida.\"\n\n"
        "Incluir codigo, error esperado y error real permite un diagnostico preciso."),
    example("Plantilla 'antes/despues' para reutilizar",
        "Objetivo: <que quieres lograr>\n"
        "Audiencia: <para quien>\n"
        "Material: <<<\n  pega aqui el texto/datos\n>>>\n"
        "Restricciones: <longitud, tono, idioma>\n"
        "Entregable: <formato exacto del resultado>"),
    quiz("Que cambio mejora mas el prompt?",
        "Tienes: \"Dame ideas de marketing\". Que anadido sube mas la calidad?",
        [("Anadir 'por favor'", False, "La cortesia no aporta informacion util."),
         ("Definir producto, audiencia y canal", True, "Correcto: el contexto del negocio enfoca las ideas."),
         ("Pedir que sea creativo", False, "Demasiado vago; no orienta el resultado.")]),
    challenge("Reto: identifica el fallo",
        "En el prompt \"traduce esto\" (sin nada mas), cual es el dato critico que falta? (una palabra)",
        "idioma", "Sin el idioma destino, Claude tiene que adivinar a que lengua traducir."),
    matching("Empareja problema y arreglo",
        [("Respuesta muy larga", "Fijar longitud"),
         ("Tono equivocado", "Especificar tono"),
         ("Se inventa datos", "Dar el material fuente"),
         ("Formato inutil", "Pedir tabla/lista")]),
    badge("🛠️ Refinador de Prompts", "Conviertes prompts genericos en instrucciones que dan resultados listos para usar."),
])

LESSONS["L3-4"] = (3, 4, "Errores comunes a evitar", [
    intro(),
    content("Error 1: pedir demasiado de golpe",
        "Meter 5 tareas en un prompt produce respuestas superficiales en todas.\n\n"
        "Sintoma: \"Analiza, resume, traduce, corrige y dame ideas\" en una linea.\n\n"
        "Arreglo: divide en pasos. Una tarea principal por mensaje; encadena despues."),
    content("Error 2: ser ambiguo y luego frustrarse",
        "Si el resultado no te gusta, casi siempre el prompt era ambiguo.\n\n"
        "Antes de reescribir el prompt entero, di que cambiar: \"mas corto\", \"mas formal\", \"sin la introduccion\". Claude itera muy bien con feedback concreto."),
    content("Error 3: asumir que conoce datos privados o recientes",
        "Claude no conoce:\n• Tus documentos internos (a menos que los pegues)\n• Eventos posteriores a su entrenamiento\n• Tu contexto personal no escrito\n\n"
        "Arreglo: pega el material y, para datos actuales, usa busqueda web o herramientas."),
    content("Error 4: confiar sin verificar",
        "Claude puede sonar muy seguro y aun asi equivocarse (alucinacion).\n\n"
        "Riesgo alto en: cifras, citas, leyes, fechas, nombres propios.\n\n"
        "Arreglo: pide que indique su nivel de confianza o que cite la fuente, y verifica los datos criticos por tu cuenta."),
    content("Error 5: prompts sin formato de salida",
        "Si no dices como quieres la respuesta, recibes texto libre dificil de reutilizar.\n\n"
        "Arreglo: termina el prompt con el formato exacto: \"Devuelve solo una tabla con columnas X, Y, Z\"."),
    example("Antidoto: el prompt 'a prueba de errores'",
        "Tarea unica: clasifica estos comentarios como POSITIVO/NEGATIVO/NEUTRO.\n"
        "Material: <<<\n  ...comentarios...\n>>>\n"
        "Reglas: si dudas, marca NEUTRO. No expliques.\n"
        "Formato: tabla de 2 columnas (comentario, etiqueta)."),
    quiz("Que error comete este prompt?",
        "\"Eres abogado. Dame el articulo exacto del codigo civil que aplica a mi caso\" (sin dar el caso ni pais).",
        [("Asume datos que no tiene + falta contexto", True, "Correcto: no dio el caso ni el pais, y pide una cita exacta verificable."),
         ("Es demasiado corto", False, "La longitud no es el problema, sino la falta de datos y el riesgo de cita inventada."),
         ("Usa rol, eso esta mal", False, "Usar un rol es correcto; el problema es otro.")]),
    challenge("Reto: cuantas tareas?",
        "Cuantas tareas distintas mete este prompt: \"resume, traduce al ingles y dame 3 hashtags\"?",
        "3", "Resumir, traducir y generar hashtags son tres tareas; conviene separarlas."),
    matching("Error y solucion",
        [("Demasiadas tareas", "Una por prompt"),
         ("Ambiguedad", "Feedback concreto"),
         ("Datos inventados", "Verificar y citar"),
         ("Salida desordenada", "Definir formato")]),
    badge("🚦 Detector de Errores", "Reconoces y evitas los errores de prompting mas comunes."),
])

# ============================ MODULO 4 =====================================
LESSONS["L4-1"] = (4, 1, "Cadenas de razonamiento", [
    intro(),
    content("Que es chain-of-thought",
        "Chain-of-thought (CoT) es pedirle a Claude que piense paso a paso ANTES de dar la respuesta final.\n\n"
        "En lugar de saltar a la conclusion, el modelo escribe su razonamiento, lo que reduce errores en tareas de logica, matematicas y analisis."),
    content("Por que mejora la precision",
        "Al razonar en voz alta, Claude:\n• Descompone el problema en partes manejables\n• Detecta sus propios errores intermedios\n• Llega a conclusiones mas fiables\n\n"
        "Es especialmente util cuando la respuesta requiere varios pasos o calculos encadenados."),
    example("Como activarlo",
        "Pregunta: Un producto cuesta 80€. Subo el precio 25% y luego hago un\n"
        "descuento del 10%. Cual es el precio final?\n\n"
        "Instruccion clave:\n\"Piensa paso a paso y muestra cada calculo antes de la respuesta final.\"\n\n"
        "# Claude responde:\n# 1) +25% de 80 = 100\n# 2) -10% de 100 = 90\n# Respuesta final: 90€"),
    content("CoT para decisiones, no solo numeros",
        "Funciona igual de bien en analisis cualitativo:\n• \"Evalua pros y contras antes de recomendar\"\n• \"Lista los criterios, puntua cada opcion y luego decide\"\n\n"
        "Ver el razonamiento te deja AUDITAR la decision, no solo aceptarla."),
    content("Cuando NO necesitas CoT",
        "Para tareas simples (traducir una frase, dar una definicion) el razonamiento extra solo anade longitud y costo.\n\n"
        "Usa CoT cuando: hay varios pasos, calculos, comparaciones o logica.\nEvitalo cuando: la respuesta es directa."),
    quiz("Cuando usar chain-of-thought?",
        "En cual de estas tareas ayuda mas el razonamiento paso a paso?",
        [("Traducir 'hola' al ingles", False, "Es directo; CoT no aporta."),
         ("Resolver un problema de logica con varias condiciones", True, "Correcto: multiples pasos se benefician del razonamiento explicito."),
         ("Pedir la capital de Francia", False, "Respuesta inmediata, no necesita pasos.")]),
    challenge("Reto: aplica CoT",
        "Con +25% y luego -10% sobre 80€, cual es el precio final en euros? (solo el numero)",
        "90", "Primero 80 x 1.25 = 100; luego 100 x 0.90 = 90."),
    matching("Concepto CoT",
        [("Chain-of-thought", "Pensar paso a paso"),
         ("Mejor en", "Logica y calculos"),
         ("Beneficio", "Menos errores"),
         ("Evitar en", "Tareas triviales")]),
    badge("🧠 Pensador en Cadena", "Sabes activar el razonamiento paso a paso para tareas complejas."),
])

LESSONS["L4-2"] = (4, 2, "Few-shot: ensenar con ejemplos", [
    intro(),
    content("Que es few-shot prompting",
        "Few-shot es dar a Claude 2-3 ejemplos de entrada y salida para que aprenda el patron, sin tener que explicarlo con reglas.\n\n"
        "Zero-shot = sin ejemplos.\nFew-shot = con ejemplos (suele ganar en consistencia de formato)."),
    content("Cuando brilla el few-shot",
        "• Cuando el formato de salida es muy especifico\n• Cuando es mas facil mostrar que explicar\n• Cuando quieres un estilo o tono consistente\n• En clasificacion y extraccion de datos"),
    example("Ejemplo de clasificacion few-shot",
        "Clasifica el sentimiento. Sigue el patron:\n\n"
        "Texto: 'Me encanto, repetire' -> POSITIVO\n"
        "Texto: 'Llego roto y tarde' -> NEGATIVO\n"
        "Texto: 'Es normal, nada especial' -> NEUTRO\n\n"
        "Texto: 'El servicio fue excelente' ->"),
    content("Buenas practicas con ejemplos",
        "• 2-3 ejemplos bien elegidos suelen bastar\n• Cubre casos variados (incluido alguno dificil)\n• Manten el formato IDENTICO en todos\n• Input y output claramente separados\n• Mas ejemplos no siempre es mejor: cuesta tokens y puede sobreajustar"),
    content("Few-shot vs instrucciones",
        "A veces una regla clara basta; a veces un ejemplo vale mas que mil reglas.\n\n"
        "Combina ambos: una instruccion corta + 2 ejemplos suele ser lo mas robusto.\n\n"
        "Si el formato es complejo (JSON anidado, tabla), los ejemplos son casi obligatorios."),
    quiz("Cuantos ejemplos es lo ideal?",
        "En la mayoria de casos de few-shot, cuantos ejemplos conviene dar?",
        [("1", False, "Uno a veces no fija bien el patron."),
         ("2-3", True, "Correcto: suelen ser suficientes para fijar el patron sin gastar de mas."),
         ("10 o mas", False, "Demasiados cuestan tokens y pueden sobreajustar.")]),
    challenge("Reto: nombra la tecnica",
        "Como se llama dar ejemplos de entrada/salida para que el modelo aprenda el patron? (dos palabras con guion o sin el)",
        "few-shot", "Few-shot (o few shot) prompting."),
    matching("Few-shot esencial",
        [("Zero-shot", "Sin ejemplos"),
         ("Few-shot", "Con ejemplos"),
         ("Ideal", "2-3 ejemplos"),
         ("Clave", "Formato identico")]),
    badge("📚 Profesor por Ejemplos", "Dominas el few-shot para fijar formato y estilo con ejemplos."),
])

LESSONS["L4-3"] = (4, 3, "Etiquetas XML para estructurar", [
    intro(),
    content("Por que usar etiquetas",
        "Claude entiende muy bien las etiquetas tipo XML para separar partes de un prompt.\n\n"
        "Sirven para marcar claramente que es instruccion, que es material y que es ejemplo, evitando que Claude los confunda.\n\n"
        "Ej: <documento>...</documento>, <ejemplo>...</ejemplo>, <reglas>...</reglas>"),
    example("Estructura con etiquetas",
        "<rol>Eres un analista financiero.</rol>\n\n"
        "<tarea>Resume el informe en 3 puntos.</tarea>\n\n"
        "<documento>\n  ...texto largo del informe...\n</documento>\n\n"
        "<formato>Lista de 3 vinetas, una frase cada una.</formato>"),
    content("Ventajas concretas",
        "• Evita que Claude trate tus datos como instrucciones\n• Hace los prompts largos legibles y mantenibles\n• Facilita pedir salidas tambien etiquetadas: <resumen>...</resumen>\n• Reduce errores cuando hay mucho texto pegado"),
    content("Pedir salida estructurada",
        "Puedes pedir que la respuesta venga dentro de etiquetas para luego extraerla con codigo:\n\n"
        "\"Devuelve el resultado dentro de <json>...</json> y nada mas fuera.\"\n\n"
        "Esto facilita procesar la respuesta automaticamente en una app."),
    content("Combina etiquetas con todo lo anterior",
        "Las etiquetas no sustituyen al buen prompt: lo ordenan.\n\n"
        "Un prompt pro suele ser: <rol> + <tarea> + <contexto/documento> + <ejemplos few-shot> + <formato>.\n\n"
        "Esa estructura escala de tareas simples a flujos de produccion."),
    quiz("Para que sirven las etiquetas XML?",
        "Cual es el beneficio principal de envolver el texto en etiquetas?",
        [("Hacen que Claude sea mas rapido", False, "No afectan la velocidad de forma relevante."),
         ("Separan claramente instruccion, datos y formato", True, "Correcto: dan estructura y evitan confusiones."),
         ("Son obligatorias siempre", False, "Son utiles, no obligatorias; brillan en prompts complejos.")]),
    challenge("Reto: cierra la etiqueta",
        "Si abro <documento>, con que etiqueta de cierre lo termino? (incluye los simbolos)",
        "</documento>", "Las etiquetas de cierre usan </nombre>."),
    matching("Etiquetas",
        [("<rol>", "Quien es Claude"),
         ("<tarea>", "Que hacer"),
         ("<documento>", "Material fuente"),
         ("<formato>", "Forma de la salida")]),
    badge("🏷️ Estructurador XML", "Usas etiquetas para organizar prompts complejos y salidas procesables."),
])

LESSONS["L4-4"] = (4, 4, "Roles, personas y restricciones", [
    intro(),
    content("El poder de asignar un rol",
        "Decirle a Claude QUIEN debe ser cambia el vocabulario, el nivel de detalle y el enfoque.\n\n"
        "\"Eres un profesor de primaria\" -> explica simple.\n\"Eres un revisor de codigo senior\" -> busca bugs y buenas practicas.\n\n"
        "El rol orienta toda la respuesta sin que tengas que detallar el estilo."),
    content("Personas: voz y tono consistentes",
        "Una persona es un rol con personalidad definida: tono, valores, forma de hablar.\n\n"
        "Util para: chatbots de marca, narradores, tutores con caracter.\n\n"
        "Define: como saluda, que evita decir, su nivel de formalidad y su especialidad."),
    example("Rol + restricciones en un system prompt",
        "Eres 'Aria', asistente de soporte de una fintech.\n"
        "- Tono: claro, calmado, empatico.\n"
        "- Nunca prometas reembolsos; deriva esos casos a un humano.\n"
        "- Responde en espanol, max 4 frases.\n"
        "- Si no sabes algo, dilo y ofrece escalar el caso."),
    content("Restricciones: lo que NO debe hacer",
        "Las restricciones acotan el comportamiento y son tan importantes como la tarea:\n\n"
        "• Longitud: \"max 100 palabras\"\n• Alcance: \"solo temas de cocina\"\n• Seguridad: \"no des consejo medico, deriva al medico\"\n• Formato: \"sin emojis\"\n\n"
        "Buenas restricciones hacen el comportamiento predecible y seguro."),
    content("System prompt vs mensaje",
        "El system prompt define el rol y las reglas globales de la conversacion (se fija una vez).\n\n"
        "Los mensajes del usuario son las peticiones concretas.\n\n"
        "Pon en el system todo lo que debe valer SIEMPRE: identidad, tono y limites."),
    quiz("Para que sirve asignar un rol?",
        "Que consigues al decir 'Eres un experto en X'?",
        [("Que Claude busque en internet sobre X", False, "Un rol no activa busqueda web por si solo."),
         ("Orientar vocabulario, enfoque y nivel de la respuesta", True, "Correcto: el rol ajusta el estilo y la profundidad."),
         ("Que las respuestas sean siempre correctas", False, "El rol mejora el enfoque, no garantiza exactitud.")]),
    challenge("Reto: tipo de instruccion",
        "\"No reveles informacion personal de otros usuarios\" es un ejemplo de... (una palabra: rol, tarea o restriccion)",
        "restriccion", "Define un limite de comportamiento: es una restriccion."),
    matching("Conceptos de rol",
        [("Rol", "Quien es Claude"),
         ("Persona", "Rol con personalidad"),
         ("Restriccion", "Lo que no debe hacer"),
         ("System prompt", "Reglas globales fijas")]),
    badge("🎭 Director de Roles", "Usas roles, personas y restricciones para controlar el comportamiento de Claude."),
])


# ============================ MODULO 5 =====================================
LESSONS["L5-1"] = (5, 1, "Artifacts: documentos vivos", [
    intro(),
    content("Que son los Artifacts",
        "Los Artifacts son ventanas de contenido que Claude crea aparte de la conversacion: documentos, codigo, paginas web, tablas o disenos.\n\n"
        "En lugar de mezclar un texto largo dentro del chat, aparece en un panel propio que puedes leer, editar y descargar."),
    content("Cuando aparece un Artifact",
        "Claude crea un Artifact cuando el resultado es algo que querras reutilizar:\n• Un documento o informe largo\n• Codigo que vas a copiar a tu editor\n• Una pagina HTML o componente\n• Una tabla o plan estructurado\n\n"
        "Para respuestas cortas o conversacionales, no se usa."),
    content("Ventajas de trabajar con Artifacts",
        "• Iteras sobre la MISMA pieza sin reescribir todo\n• Puedes pedir cambios concretos: \"hazlo mas corto\", \"cambia el titulo\"\n• Se mantiene separado del hilo de conversacion\n• Facil de copiar, descargar o previsualizar"),
    content("Como pedir buenos Artifacts",
        "• Di el tipo: \"crea un documento\", \"hazme una pagina HTML\"\n• Indica el formato y la extension deseada\n• Pide iteraciones paso a paso en vez de todo de golpe\n• Si algo no encaja, describe el cambio puntual"),
    example("Pidiendo un Artifact util",
        "Crea un documento de una pagina con la propuesta de proyecto.\n"
        "Secciones: objetivo, alcance, plazos y presupuesto estimado.\n"
        "Tono profesional. Deja los importes como [PENDIENTE] para rellenar.\n\n"
        "Luego: 'Anade una seccion de riesgos con 3 vinetas.'"),
    quiz("Cuando usar un Artifact?",
        "Cual de estos casos es ideal para un Artifact?",
        [("Preguntar la hora", False, "Es una respuesta corta, no necesita panel aparte."),
         ("Generar un informe largo que editaras", True, "Correcto: contenido sustancial y reutilizable."),
         ("Un saludo rapido", False, "Conversacional; no requiere Artifact.")]),
    challenge("Reto: concepto clave",
        "Como se llama el panel aparte donde Claude crea documentos y codigo editables? (una palabra)",
        "artifacts", "Se llaman Artifacts (o artifact)."),
    matching("Artifacts",
        [("Artifact", "Contenido en panel aparte"),
         ("Ideal para", "Documentos y codigo"),
         ("Ventaja", "Iterar sin reescribir"),
         ("Evitar en", "Respuestas cortas")]),
    badge("📄 Creador de Artifacts", "Sabes cuando y como usar Artifacts para crear contenido reutilizable."),
])

LESSONS["L5-2"] = (5, 2, "Busqueda web e investigacion", [
    intro(),
    content("Por que la busqueda web importa",
        "Claude se entrena con datos hasta cierta fecha; no conoce noticias ni cambios recientes por si solo.\n\n"
        "La busqueda web le permite consultar informacion actual: precios, eventos, lanzamientos, datos que cambian con el tiempo."),
    content("Cuando conviene activar busqueda",
        "Usa busqueda cuando preguntas por:\n• Hechos actuales (quien ocupa un cargo hoy)\n• Precios o cifras que cambian\n• Noticias o eventos recientes\n• Documentacion que se actualiza\n\n"
        "Para conocimiento general estable, no hace falta."),
    content("Investigacion: mas alla de una busqueda",
        "Para temas amplios, Claude puede hacer varias busquedas, contrastar fuentes y sintetizar.\n\n"
        "Buenas peticiones:\n• \"Compara 3 fuentes y senala en que coinciden\"\n• \"Resume el estado actual del tema y cita de donde sale cada dato\""),
    content("Verifica siempre lo critico",
        "Aunque busque en la web, conviene:\n• Pedir las fuentes/enlaces\n• Contrastar cifras importantes\n• Desconfiar de un solo resultado\n\n"
        "La busqueda reduce el riesgo de datos inventados, pero tu criterio sigue siendo clave."),
    quiz("Cuando NO necesitas busqueda web?",
        "En cual caso la busqueda aporta poco?",
        [("Precio actual de un vuelo", False, "Cambia constantemente: necesita datos actuales."),
         ("Definir que es la fotosintesis", True, "Correcto: es conocimiento estable, no requiere busqueda."),
         ("Resultado del partido de ayer", False, "Es un evento reciente: necesita busqueda.")]),
    challenge("Reto: por que buscar",
        "Cual es la razon principal para usar busqueda web: porque Claude no conoce informacion ___ a su entrenamiento. (una palabra)",
        "posterior", "Vale 'posterior', 'reciente' o 'actual': no conoce datos posteriores a su entrenamiento."),
    matching("Busqueda web",
        [("Sirve para", "Datos actuales"),
         ("No hace falta en", "Conocimiento estable"),
         ("Buena practica", "Pedir fuentes"),
         ("Riesgo a evitar", "Confiar sin verificar")]),
    badge("🌐 Investigador Web", "Sabes cuando usar busqueda web y como verificar la informacion."),
])

LESSONS["L5-3"] = (5, 3, "Creacion de archivos", [
    intro(),
    content("Claude como generador de archivos",
        "Claude puede producir archivos listos para descargar: documentos de texto, hojas de calculo, presentaciones, PDF, codigo y mas.\n\n"
        "En vez de copiar y pegar, recibes el archivo terminado."),
    content("Tipos de archivo habituales",
        "• Documentos: .docx, .md, .txt\n• Datos: .csv, .xlsx\n• Presentaciones: .pptx\n• Documentos finales: .pdf\n• Codigo: .py, .js, .html\n\n"
        "Pide el formato que necesitas y para que lo usaras."),
    example("Pidiendo un archivo concreto",
        "Crea una hoja de calculo (.xlsx) con un presupuesto mensual.\n"
        "Columnas: categoria, presupuesto, gasto real, diferencia.\n"
        "Incluye filas de ejemplo y una fila de totales con formula.\n"
        "Deja una pestana de 'resumen' con los totales por categoria."),
    content("Buenas practicas",
        "• Indica el formato exacto y la estructura (columnas, secciones)\n• Da datos de ejemplo si quieres ver el resultado\n• Pide validaciones: \"que los totales cuadren\"\n• Revisa el archivo antes de usarlo en produccion"),
    content("De los datos al entregable",
        "Puedes encadenar: pegas datos en bruto y pides el archivo final.\n\n"
        "Ej: \"Con estos datos de ventas, generame un Excel con una tabla y un grafico de barras por mes.\"\n\n"
        "Asi conviertes informacion suelta en algo presentable en un paso."),
    quiz("Que formato pedir para datos tabulares?",
        "Necesitas analizar numeros en columnas y filas. Que formato encaja mejor?",
        [(".pptx", False, "Es para presentaciones, no para analizar datos."),
         (".xlsx o .csv", True, "Correcto: formatos de hoja de calculo para datos tabulares."),
         (".txt", False, "Texto plano no estructura bien tablas con formulas.")]),
    challenge("Reto: extension de Excel",
        "Cual es la extension de archivo de una hoja de calculo de Excel moderna? (incluye el punto)",
        ".xlsx", "Las hojas de Excel modernas usan .xlsx."),
    matching("Archivo segun necesidad",
        [("Informe formal", ".docx / .pdf"),
         ("Datos y formulas", ".xlsx"),
         ("Diapositivas", ".pptx"),
         ("Script", ".py / .js")]),
    badge("🗂️ Generador de Archivos", "Sabes pedir archivos listos para usar en el formato correcto."),
])

LESSONS["L5-4"] = (5, 4, "Memoria y conversaciones pasadas", [
    intro(),
    content("Como 'recuerda' Claude",
        "Dentro de una conversacion, Claude recuerda todo lo dicho hasta el limite del context window.\n\n"
        "Pero por defecto, cada conversacion nueva empieza de cero: no recuerda chats anteriores salvo que existan funciones de memoria o tu repitas el contexto."),
    content("El context window como memoria a corto plazo",
        "Todo lo que esta en la conversacion actual es 'memoria viva'.\n\n"
        "• Puedes referirte a mensajes anteriores del mismo hilo\n• Si la conversacion es muy larga, lo mas antiguo puede salir del contexto\n• Resume tu mismo los puntos clave si el hilo crece mucho"),
    content("Estrategias para mantener contexto",
        "• Trabaja temas relacionados en el mismo hilo\n• Empieza un hilo nuevo para temas distintos (mas limpio)\n• Pega un breve resumen al iniciar si necesitas continuidad\n• Usa Proyectos para guardar contexto reutilizable"),
    content("Privacidad y memoria",
        "Piensa que comparte cada hilo:\n• No pegues datos sensibles que no necesites\n• Revisa la configuracion de datos de tu cuenta\n• Para informacion confidencial, minimiza lo que incluyes\n\n"
        "Mas sobre esto en el modulo de Buenas Practicas y Limites."),
    quiz("Recuerda Claude entre conversaciones?",
        "Por defecto, que pasa al abrir una conversacion nueva?",
        [("Recuerda todos tus chats anteriores", False, "No por defecto; cada hilo suele empezar limpio."),
         ("Empieza sin memoria del hilo anterior salvo que des contexto", True, "Correcto: hay que aportar el contexto o usar funciones de memoria/proyectos."),
         ("Borra tus archivos", False, "Abrir un chat no borra nada tuyo.")]),
    challenge("Reto: nombre del 'espacio'",
        "Como se llama la cantidad de texto que Claude puede tener presente en una conversacion? (dos palabras en ingles)",
        "context window", "Es el 'context window' o ventana de contexto."),
    matching("Memoria",
        [("Mismo hilo", "Recuerda lo dicho"),
         ("Hilo nuevo", "Empieza limpio"),
         ("Context window", "Memoria del hilo"),
         ("Proyectos", "Contexto reutilizable")]),
    badge("🧩 Gestor de Contexto", "Entiendes como funciona la memoria de Claude y como mantener continuidad."),
])

# ============================ MODULO 6 =====================================
LESSONS["L6-1"] = (6, 1, "Escritura y comunicacion", [
    intro(),
    content("Claude como asistente de escritura",
        "Una de las tareas mas potentes: redactar y mejorar textos.\n\n"
        "Emails, posts, articulos, propuestas, mensajes dificiles... Claude acelera el primer borrador y pule el tono."),
    content("Redactar desde cero",
        "Da siempre: objetivo, audiencia, tono y longitud.\n\n"
        "Ej: \"Escribe un post de LinkedIn (max 150 palabras, tono inspirador pero concreto) anunciando que mi equipo lanzo una funcion nueva.\"\n\n"
        "Pide 2-3 variantes para elegir."),
    content("Mejorar texto existente",
        "Pega tu borrador y di que cambiar:\n• \"Hazlo mas conciso\"\n• \"Tono mas formal\"\n• \"Corrige gramatica sin cambiar el sentido\"\n• \"Adaptalo para un publico no tecnico\"\n\n"
        "Claude itera muy bien sobre tu material en lugar de inventar de cero."),
    content("Adaptar tono y canal",
        "El mismo mensaje cambia segun el canal:\n• Email formal vs mensaje de chat\n• Post de marca vs nota interna\n\n"
        "Pide explicitamente la adaptacion: \"reescribe esto como tweet\", \"convierte este email en un mensaje breve de WhatsApp\"."),
    example("Mensaje dificil con tacto",
        "Contexto: tengo que rechazar la propuesta de un proveedor con el\n"
        "que quiero mantener buena relacion.\n\n"
        "Tarea: escribe un email breve, agradecido y claro que diga 'no por ahora'\n"
        "dejando la puerta abierta a futuro. Max 90 palabras."),
    quiz("Que falta para un buen encargo de escritura?",
        "\"Escribeme un texto\" es debil. Que trio conviene fijar SIEMPRE?",
        [("Color, fuente y tamano", False, "Eso es diseno visual, no redaccion."),
         ("Objetivo, audiencia y tono", True, "Correcto: definen el contenido y la voz del texto."),
         ("Hora, fecha y lugar", False, "Datos del evento, no del encargo de escritura.")]),
    challenge("Reto: pide variantes",
        "Para poder elegir, cuantas variantes de un asunto de email es razonable pedir? (un numero entre 2 y 5)",
        "3", "Pedir 2-5 variantes te da opciones; 3 es un valor tipico."),
    matching("Escritura",
        [("Desde cero", "Da objetivo y tono"),
         ("Mejorar", "Pega y pide cambios"),
         ("Adaptar", "Cambia de canal"),
         ("Elegir mejor", "Pide variantes")]),
    badge("✍️ Comunicador Pro", "Usas Claude para redactar, pulir y adaptar textos a cada audiencia."),
])

LESSONS["L6-2"] = (6, 2, "Programacion y analisis tecnico", [
    intro(),
    content("Claude como copiloto de codigo",
        "Claude ayuda en todo el ciclo: escribir funciones, explicar codigo ajeno, encontrar bugs, escribir tests y refactorizar.\n\n"
        "Funciona mejor cuando le das contexto: lenguaje, version, que hace el codigo y que esperas."),
    content("Pedir codigo que sirva",
        "• Indica lenguaje y version\n• Describe la entrada y la salida esperada\n• Menciona restricciones (librerias permitidas, rendimiento)\n• Pide comentarios y manejo de errores si lo necesitas"),
    example("Debugging con contexto",
        "Lenguaje: Python 3.11\n"
        "Esta funcion deberia devolver la lista sin duplicados manteniendo el orden,\n"
        "pero a veces los pierde. Pega el codigo + un caso que falla.\n\n"
        "Pide: 'Explica la causa y dame la version corregida con un test.'"),
    content("Explicar y aprender",
        "Pega codigo que no entiendas y pide:\n• \"Explicalo linea por linea\"\n• \"Que hace esta funcion y por que?\"\n• \"Hay riesgos de seguridad aqui?\"\n\n"
        "Es una forma rapida de entender bases de codigo nuevas."),
    content("Buenas practicas al programar con IA",
        "• Revisa SIEMPRE el codigo antes de ejecutarlo\n• Prueba con casos limite\n• No pegues secretos (claves, tokens) en el prompt\n• Pide tests para validar el comportamiento"),
    quiz("Que dato ayuda mas a depurar?",
        "Al pedir ayuda con un bug, que es lo mas util incluir junto al codigo?",
        [("Tu opinion sobre el lenguaje", False, "No aporta al diagnostico."),
         ("El error real y el resultado esperado", True, "Correcto: comparar esperado vs real permite localizar la causa."),
         ("La hora a la que fallo", False, "Irrelevante para el bug en si.")]),
    challenge("Reto: buena practica",
        "Antes de ejecutar codigo generado por IA, que deberias hacer siempre? (una palabra que empieza por R)",
        "revisar", "Revisarlo: nunca ejecutes a ciegas codigo generado."),
    matching("Programar con Claude",
        [("Escribir", "Da lenguaje y E/S"),
         ("Depurar", "Error esperado vs real"),
         ("Entender", "Explicar linea a linea"),
         ("Seguridad", "No pegar secretos")]),
    badge("💻 Copiloto Tecnico", "Sabes usar Claude para escribir, depurar y entender codigo de forma segura."),
])

LESSONS["L6-3"] = (6, 3, "Analisis de datos y documentos", [
    intro(),
    content("Convierte datos en respuestas",
        "Claude puede leer documentos largos y datos y extraer lo importante: resumir, comparar, clasificar y encontrar patrones.\n\n"
        "Ideal para informes, contratos, encuestas, tablas y PDFs."),
    content("Resumen y extraccion",
        "• \"Resume este informe en 5 puntos para direccion\"\n• \"Extrae todas las fechas y montos en una tabla\"\n• \"Que riesgos menciona el documento?\"\n\n"
        "Pega el documento y define exactamente que dato quieres de vuelta."),
    content("Analisis de tablas y cifras",
        "Con datos tabulares puedes pedir:\n• Tendencias y variaciones\n• Top/bottom por categoria\n• Anomalias o valores raros\n• Conclusiones accionables\n\n"
        "Recuerda verificar los calculos criticos."),
    example("Extraccion estructurada",
        "Del siguiente texto, extrae los datos en JSON con las claves\n"
        "{cliente, fecha, importe, estado}. Si un dato no aparece, pon null.\n\n"
        "Texto: <<<\n  ...factura o email...\n>>>\n\n"
        "Devuelve SOLO el JSON."),
    content("Limites a tener en cuenta",
        "• Documentos enormes pueden superar el context window: divide o resume por partes\n• Verifica cifras y citas importantes\n• Para datos sensibles, cuida la privacidad (modulo 7)"),
    quiz("Mejor formato para extraer datos a una app?",
        "Quieres procesar la salida con codigo. Que formato pides?",
        [("Un parrafo en prosa", False, "Dificil de parsear automaticamente."),
         ("JSON con claves definidas", True, "Correcto: estructurado y facil de procesar."),
         ("Un poema", False, "Nada practico para datos.")]),
    challenge("Reto: dato faltante",
        "Si pides extraer un campo que no aparece en el texto, que valor conviene indicar que use? (una palabra en ingles, 4 letras)",
        "null", "Usar null marca claramente que el dato falta."),
    matching("Analisis de datos",
        [("Documento largo", "Resumir por partes"),
         ("Datos a app", "Pedir JSON"),
         ("Tablas", "Tendencias y top"),
         ("Cifras clave", "Verificar")]),
    badge("📊 Analista de Datos", "Extraes, resumes y analizas documentos y datos con criterio."),
])

LESSONS["L6-4"] = (6, 4, "Creatividad: ideas y storytelling", [
    intro(),
    content("Claude como socio creativo",
        "Mas alla de lo tecnico, Claude ayuda a generar ideas, nombres, guiones, historias y conceptos.\n\n"
        "Funciona como un companero de lluvia de ideas que nunca se queda sin propuestas."),
    content("Lluvia de ideas efectiva",
        "• Pide cantidad primero: \"dame 20 ideas\", luego filtras\n• Da restricciones para enfocar: publico, tono, presupuesto\n• Pide angulos distintos: \"5 ideas seguras y 5 arriesgadas\"\n\n"
        "La diversidad mejora cuando defines el espacio de busqueda."),
    content("Storytelling y estructura",
        "Para historias o contenido narrativo:\n• Define personaje, conflicto y tono\n• Pide primero la estructura (esqueleto), luego desarrolla\n• Itera escena a escena\n\n"
        "Construir por capas da mejores resultados que pedir todo de golpe."),
    example("Brief creativo",
        "Necesito nombres para una cafeteria de especialidad.\n"
        "Tono: calido, moderno, facil de recordar.\n"
        "Evita: palabras en ingles y juegos de palabras obvios.\n"
        "Dame 15 opciones con una linea de justificacion cada una."),
    content("Refinar lo creativo",
        "Las primeras ideas son materia prima. Mejora con feedback:\n• \"Mezcla la idea 3 y la 7\"\n• \"Mas atrevido\", \"mas elegante\"\n• \"Desarrolla solo la 5 en un parrafo\"\n\n"
        "Tu criterio dirige; Claude aporta volumen y variantes."),
    quiz("Como obtener mejores ideas?",
        "Que estrategia da una lluvia de ideas mas rica?",
        [("Pedir 'una buena idea'", False, "Limita el rango; mejor generar muchas y filtrar."),
         ("Pedir muchas con restricciones claras", True, "Correcto: cantidad + foco produce mejores opciones para elegir."),
         ("No dar ningun contexto", False, "Sin foco, las ideas salen genericas.")]),
    challenge("Reto: orden creativo",
        "Para una historia, conviene pedir primero la estructura/esqueleto o el texto final? (responde: estructura o final)",
        "estructura", "Mejor construir por capas: primero estructura, luego desarrollo."),
    matching("Creatividad",
        [("Ideas", "Pedir cantidad"),
         ("Enfoque", "Dar restricciones"),
         ("Historia", "Estructura primero"),
         ("Mejorar", "Feedback concreto")]),
    badge("🎨 Socio Creativo", "Usas Claude para generar y refinar ideas e historias con metodo."),
])

# ============================ MODULO 7 =====================================
LESSONS["L7-1"] = (7, 1, "Privacidad y datos sensibles", [
    intro(),
    content("Que cuentas y a quien",
        "Cada cosa que pegas en un chat sale de tu dispositivo. Antes de compartir, piensa: necesito de verdad este dato para la tarea?\n\n"
        "Datos sensibles tipicos:\n• Personales (nombres, DNI, telefonos, direcciones)\n• De salud o financieros\n• Secretos de empresa y credenciales (claves, tokens)"),
    content("Minimiza lo que compartes",
        "Principio de minimizacion: aporta solo lo imprescindible.\n\n"
        "• Anonimiza: sustituye nombres reales por [CLIENTE], [EMPLEADO]\n• Quita identificadores que no aporten a la tarea\n• Nunca pegues contrasenas o claves API en el prompt"),
    content("Configuracion y politicas",
        "• Revisa los ajustes de datos de tu cuenta\n• Conoce la politica de tu organizacion sobre IA\n• En entornos corporativos, sigue las reglas de cumplimiento\n\n"
        "Saber como se tratan tus datos te deja decidir con criterio."),
    example("Anonimizar antes de pegar",
        "ANTES:\nRevisa este contrato de Juan Perez (DNI 12345678) por 50.000€.\n\n"
        "DESPUES:\nRevisa este contrato de [CLIENTE] (DNI [REDACTADO]) por [IMPORTE].\n"
        "Identifica clausulas de riesgo y plazos de pago."),
    content("Senales de alerta",
        "Para antes de pegar si el texto incluye:\n• Credenciales o claves\n• Datos medicos o financieros de terceros\n• Informacion bajo NDA\n\n"
        "Si dudas, anonimiza o consulta la politica antes de continuar."),
    quiz("Que NO deberias pegar nunca?",
        "Cual de estos es el mas peligroso de compartir en un prompt?",
        [("Un texto publico de un blog", False, "Es publico; bajo riesgo."),
         ("Tu clave API o contrasena", True, "Correcto: las credenciales nunca deben ir en un prompt."),
         ("Una idea de negocio general", False, "Bajo riesgo si no incluye datos sensibles concretos.")]),
    challenge("Reto: principio clave",
        "Como se llama el principio de compartir solo los datos imprescindibles? (una palabra que empieza por M)",
        "minimizacion", "El principio de minimizacion de datos."),
    matching("Privacidad",
        [("Minimizar", "Solo lo imprescindible"),
         ("Anonimizar", "Sustituir datos reales"),
         ("Credenciales", "Nunca pegarlas"),
         ("Politica", "Reglas de tu organizacion")]),
    badge("🔐 Guardian de Datos", "Proteges la privacidad: minimizas, anonimizas y cuidas datos sensibles."),
])

LESSONS["L7-2"] = (7, 2, "Verificacion y pensamiento critico", [
    intro(),
    content("Por que verificar",
        "Claude puede equivocarse y sonar muy seguro al hacerlo (alucinacion).\n\n"
        "El riesgo es mayor en: cifras exactas, citas, leyes, fechas, nombres propios y datos muy especificos.\n\n"
        "La IA es un acelerador, no un oraculo: tu juicio sigue mandando."),
    content("Como reducir errores",
        "• Pide que indique su nivel de confianza\n• Pide fuentes y verificalas\n• Usa busqueda web para datos actuales\n• Pide razonamiento paso a paso en temas complejos\n• Contrasta datos criticos en una fuente fiable"),
    content("Senales de posible alucinacion",
        "Sospecha cuando:\n• Da una cita o estudio muy concreto sin fuente\n• Mezcla detalles que no logras confirmar\n• Responde con seguridad sobre algo muy reciente\n\n"
        "Ante la duda, pide la fuente o reformula la pregunta."),
    example("Prompt que invita a la honestidad",
        "Responde solo si estas seguro. Si no lo sabes o no puedes verificarlo,\n"
        "dilo claramente en lugar de inventar.\n\n"
        "Para cada dato relevante, indica tu nivel de confianza (alto/medio/bajo)."),
    content("El humano en el bucle",
        "Para decisiones importantes (legales, medicas, financieras), trata la respuesta como un borrador a revisar, no como veredicto.\n\n"
        "Combina: rapidez de Claude + verificacion humana = lo mejor de ambos."),
    quiz("Que es una 'alucinacion' en IA?",
        "Como se describe mejor?",
        [("Un error de conexion", False, "No es un fallo tecnico de red."),
         ("Una respuesta que suena segura pero es falsa", True, "Correcto: el modelo afirma con confianza algo incorrecto."),
         ("Cuando el modelo se apaga", False, "No tiene que ver con apagarse.")]),
    challenge("Reto: que pedir",
        "Para poder comprobar un dato, que conviene pedirle a Claude que incluya? (una palabra)",
        "fuente", "Pedir la fuente (o fuentes) permite verificar el dato."),
    matching("Pensamiento critico",
        [("Alucinacion", "Seguro pero falso"),
         ("Datos actuales", "Busqueda web"),
         ("Verificar", "Pedir fuentes"),
         ("Decision clave", "Humano revisa")]),
    badge("🔎 Verificador Critico", "Verificas, pides fuentes y aplicas pensamiento critico a las respuestas."),
])

LESSONS["L7-3"] = (7, 3, "Limitaciones que debes conocer", [
    intro(),
    content("Conocimiento con fecha de corte",
        "Claude se entrena hasta una fecha; no conoce eventos posteriores por si solo.\n\n"
        "Para informacion reciente, usa busqueda web o aporta tu el dato actualizado."),
    content("No tiene acceso por defecto a tu mundo",
        "Sin herramientas, Claude no puede:\n• Navegar internet en tiempo real\n• Abrir tus archivos o sistemas\n• Recordar conversaciones pasadas\n• Saber la fecha/hora exacta sin que se la des\n\n"
        "Esas capacidades llegan con herramientas e integraciones (modulo 8)."),
    content("Variabilidad y exactitud",
        "• Dos respuestas a la misma pregunta pueden diferir\n• Puede errar en cifras y datos muy especificos\n• Su 'seguridad' no garantiza que tenga razon\n\n"
        "Disena tus flujos contando con esto: verifica lo critico."),
    content("Como convivir con los limites",
        "• Pega el contexto que necesite (no asumas que lo sabe)\n• Activa herramientas para datos actuales o acciones\n• Divide tareas grandes\n• Verifica resultados importantes\n\n"
        "Conocer los limites es lo que te hace un usuario avanzado."),
    quiz("Que NO puede hacer Claude por defecto?",
        "Sin herramientas adicionales, cual de estas NO puede hacer?",
        [("Redactar un email", False, "Eso lo hace perfectamente sin herramientas."),
         ("Saber la noticia de esta manana", True, "Correcto: sin busqueda no conoce eventos recientes."),
         ("Resumir un texto que le pegas", False, "Puede resumir lo que le proporciones.")]),
    challenge("Reto: termino clave",
        "Como se llama la fecha hasta la que llega el conocimiento de un modelo? (dos palabras: fecha de ___)",
        "corte", "La 'fecha de corte' del conocimiento (knowledge cutoff)."),
    matching("Limitaciones",
        [("Fecha de corte", "No sabe lo reciente"),
         ("Sin herramientas", "No navega ni abre archivos"),
         ("Variabilidad", "Respuestas distintas"),
         ("Solucion", "Contexto y verificacion")]),
    badge("⚠️ Consciente de Limites", "Conoces las limitaciones de Claude y como trabajar alrededor de ellas."),
])

LESSONS["L7-4"] = (7, 4, "Uso responsable y etico", [
    intro(),
    content("Tu eres responsable del resultado",
        "Claude es una herramienta; las decisiones y publicaciones son tuyas.\n\n"
        "Usa la IA para amplificar tu trabajo, no para evadir responsabilidad sobre lo que generas y compartes."),
    content("Transparencia",
        "• Indica cuando un contenido fue asistido por IA si el contexto lo requiere\n• No atribuyas a personas reales frases que no dijeron\n• Respeta derechos de autor y fuentes"),
    content("Evita usos daninos",
        "No uses la IA para:\n• Enganar, suplantar o manipular\n• Generar desinformacion\n• Acosar o discriminar\n\n"
        "El uso responsable protege a otros y a tu propia reputacion."),
    content("Sesgos y equidad",
        "Los modelos pueden reflejar sesgos de sus datos.\n\n"
        "• Revisa resultados sensibles (contratacion, evaluaciones)\n• Pide multiples perspectivas\n• No delegues decisiones que afectan a personas sin supervision humana"),
    quiz("Quien es responsable del contenido generado?",
        "Si publicas un texto hecho con ayuda de Claude y tiene un error grave, quien responde?",
        [("Claude", False, "La herramienta no asume tu responsabilidad."),
         ("Tu, que lo revisas y publicas", True, "Correcto: la responsabilidad final del uso es tuya."),
         ("Nadie", False, "Siempre hay un responsable: quien publica.")]),
    challenge("Reto: principio etico",
        "Atribuir a una persona real una frase que no dijo viola que principio? (una palabra que empieza por T)",
        "transparencia", "Falta de transparencia/honestidad: no inventar citas de personas reales."),
    matching("Uso responsable",
        [("Responsabilidad", "Es del usuario"),
         ("Transparencia", "Indicar uso de IA"),
         ("Evitar", "Desinformacion"),
         ("Sesgos", "Supervisar y revisar")]),
    badge("⚖️ Usuario Responsable", "Aplicas etica, transparencia y supervision humana al usar IA."),
])

# ============================ MODULO 8 =====================================
LESSONS["L8-1"] = (8, 1, "Claude Code para desarrolladores", [
    intro(),
    content("Que es Claude Code",
        "Claude Code es una herramienta de linea de comandos que lleva a Claude a tu terminal y tu base de codigo.\n\n"
        "Puede leer y editar archivos, ejecutar comandos, correr tests y trabajar en tareas de programacion de forma agentica, paso a paso."),
    content("Que puede hacer",
        "• Entender un repositorio completo\n• Implementar funciones y arreglar bugs\n• Ejecutar y corregir tests\n• Hacer refactors grandes\n• Explicar codigo y dependencias\n\n"
        "Trabaja directamente sobre tus archivos, no solo en el chat."),
    content("Como se trabaja con el",
        "• Le das una tarea en lenguaje natural\n• Propone un plan y va ejecutando\n• Revisas sus cambios (diffs) antes de aceptarlos\n• Iteras: 'corrige esto', 'anade un test'\n\n"
        "Tu sigues al mando: apruebas los cambios importantes."),
    example("Tareas tipicas en Claude Code",
        "\"Anade validacion de email al formulario de registro y un test.\"\n"
        "\"Encuentra por que falla el test de pagos y arreglalo.\"\n"
        "\"Refactoriza utils.js para separar la logica de red.\"\n"
        "\"Explica como fluye la autenticacion en este repo.\""),
    content("Buenas practicas",
        "• Trabaja con control de versiones (git) para revisar diffs\n• Da tareas acotadas y claras\n• Revisa los cambios antes de hacer commit\n• No expongas secretos en el repositorio"),
    quiz("Que distingue a Claude Code del chat?",
        "Cual es la diferencia clave?",
        [("Es mas barato", False, "No es la diferencia esencial."),
         ("Puede leer/editar archivos y ejecutar comandos en tu proyecto", True, "Correcto: trabaja agenticamente sobre tu codigo real."),
         ("Solo responde preguntas teoricas", False, "Hace mucho mas: actua sobre el codigo.")]),
    challenge("Reto: herramienta de control",
        "Que sistema conviene usar para revisar los cambios (diffs) que hace Claude Code? (tres letras)",
        "git", "git permite ver diffs y revertir cambios con seguridad."),
    matching("Claude Code",
        [("Entorno", "Terminal y codigo"),
         ("Capacidad", "Editar y ejecutar"),
         ("Control", "Revisar diffs"),
         ("Buena practica", "Usar git")]),
    badge("🖥️ Dev con Claude Code", "Conoces Claude Code y como trabajar agenticamente sobre tu codigo."),
])

LESSONS["L8-2"] = (8, 2, "Integraciones y conectores MCP", [
    intro(),
    content("Que es MCP",
        "MCP (Model Context Protocol) es un estandar abierto para conectar Claude con herramientas y datos externos: tu calendario, tu CRM, bases de datos, APIs.\n\n"
        "Es como un 'puerto USB' universal: una vez conectado, Claude puede leer y actuar en esa herramienta."),
    content("Por que importa",
        "Con conectores, Claude pasa de 'solo conversar' a 'hacer cosas':\n• Consultar tus datos reales\n• Crear tareas, eventos o registros\n• Buscar en tus sistemas\n• Automatizar flujos entre apps"),
    content("Como funciona a alto nivel",
        "• Un servidor MCP expone herramientas (acciones) y recursos (datos)\n• Claude descubre que puede hacer y las usa cuando hace falta\n• Tu autorizas el acceso\n\n"
        "Hay conectores listos para muchas apps populares y puedes crear los tuyos."),
    example("Ejemplos de lo que habilita un conector",
        "Calendario: 'Que tengo manana? Bloquea 1h para preparar la reunion.'\n"
        "CRM: 'Crea un contacto para el lead que escribio hoy.'\n"
        "Base de datos: 'Cuantos pedidos hubo la semana pasada?'\n"
        "Documentos: 'Busca el contrato de [CLIENTE] y resumelo.'"),
    content("Seguridad con conectores",
        "• Concede solo los permisos necesarios\n• Revisa que acciones puede ejecutar\n• Confirma antes de acciones sensibles (enviar dinero, borrar datos)\n\n"
        "El control de accesos es clave cuando Claude puede actuar en tus sistemas."),
    quiz("Que es MCP?",
        "Cual definicion encaja mejor?",
        [("Un modelo de Claude mas grande", False, "No es un modelo, es un protocolo."),
         ("Un estandar para conectar Claude con herramientas y datos", True, "Correcto: Model Context Protocol conecta Claude con el exterior."),
         ("Un lenguaje de programacion", False, "No es un lenguaje; es un protocolo de conexion.")]),
    challenge("Reto: siglas",
        "Que significan las siglas MCP? (tres palabras en ingles: Model ___ Protocol)",
        "context", "Model Context Protocol."),
    matching("MCP",
        [("MCP", "Protocolo de conexion"),
         ("Herramientas", "Acciones que ejecuta"),
         ("Recursos", "Datos que consulta"),
         ("Clave", "Permisos y control")]),
    badge("🔌 Integrador MCP", "Entiendes MCP y como los conectores permiten a Claude actuar en tus herramientas."),
])

LESSONS["L8-3"] = (8, 3, "Recursos para seguir aprendiendo", [
    intro(),
    content("Aprender no termina aqui",
        "La IA evoluciona rapido. Tener un sistema para mantenerte al dia vale mas que memorizar datos que cambian."),
    content("Fuentes oficiales",
        "• Documentacion de Claude (guias y referencia de API)\n• Centro de ayuda y notas de versiones\n• Guias de prompt engineering oficiales\n\n"
        "Empieza siempre por la fuente oficial cuando dudes de una capacidad."),
    content("Practica deliberada",
        "• Elige un problema real tuyo y resuelvelo con Claude\n• Guarda tus mejores prompts como plantillas\n• Comparte y compara con otras personas\n\n"
        "Aprender haciendo supera a solo leer."),
    content("Habito de actualizacion",
        "• Revisa novedades cada cierto tiempo\n• Prueba funciones nuevas en tareas pequenas\n• Re-evalua tus flujos cuando salen mejoras\n\n"
        "Un buen usuario itera sus propios metodos."),
    quiz("Donde mirar primero ante una duda de capacidad?",
        "Que fuente conviene consultar primero?",
        [("Un foro al azar", False, "Puede estar desactualizado o ser incorrecto."),
         ("La documentacion oficial", True, "Correcto: es la fuente mas fiable y actual."),
         ("Una captura antigua", False, "Las capturas envejecen rapido.")]),
    challenge("Reto: mejor habito",
        "Para aprender de verdad, que es mas eficaz: solo leer o ___ con problemas reales? (una palabra)",
        "practicar", "La practica deliberada con problemas reales consolida el aprendizaje."),
    matching("Seguir aprendiendo",
        [("Duda de capacidad", "Doc oficial"),
         ("Mejores prompts", "Guardar plantillas"),
         ("Consolidar", "Practicar"),
         ("Estar al dia", "Revisar novedades")]),
    badge("📈 Aprendiz Continuo", "Tienes un metodo para seguir mejorando con Claude a largo plazo."),
])

LESSONS["L8-4"] = (8, 4, "Proyecto final", [
    intro(),
    content("Pon todo en practica",
        "El proyecto final integra lo aprendido: elige un problema real y resuelvelo de principio a fin usando buenas tecnicas de prompting y, si aplica, herramientas."),
    content("Pasos sugeridos",
        "1) Define el objetivo y el entregable\n2) Reune el contexto y los datos\n3) Disena el prompt (rol, tarea, contexto, formato)\n4) Itera y refina con feedback\n5) Verifica el resultado\n6) Documenta tu mejor prompt"),
    content("Ideas de proyecto",
        "• Un asistente de redaccion para tu trabajo\n• Un analizador de tus documentos o datos\n• Un generador de contenido para tu marca\n• Un flujo que conecte Claude con una de tus apps (MCP)"),
    example("Plantilla de brief del proyecto",
        "Objetivo: <que problema resuelvo>\n"
        "Entregable: <que produzco exactamente>\n"
        "Contexto/datos: <que necesita Claude>\n"
        "Tecnicas: <few-shot, CoT, etiquetas, herramientas>\n"
        "Criterio de exito: <como se que quedo bien>"),
    content("Checklist final",
        "✅ El prompt define rol, tarea, contexto y formato\n✅ Probaste con casos reales\n✅ Verificaste los datos criticos\n✅ Guardaste la plantilla reutilizable\n✅ El entregable cumple el criterio de exito"),
    quiz("Que NO debe faltar en tu proyecto?",
        "Cual es un paso imprescindible antes de dar por bueno el resultado?",
        [("Verificar el resultado", True, "Correcto: la verificacion es clave antes de usar/publicar."),
         ("Hacerlo en ingles", False, "El idioma depende de tu caso, no es imprescindible."),
         ("Usar el modelo mas caro", False, "No hace falta; elige el adecuado a la tarea.")]),
    challenge("Reto: primer paso",
        "Cual es el primer paso de un buen proyecto: definir el ___? (una palabra)",
        "objetivo", "Todo empieza por definir el objetivo y el entregable."),
    matching("Proyecto final",
        [("Paso 1", "Definir objetivo"),
         ("Diseno", "Rol/tarea/contexto/formato"),
         ("Antes de cerrar", "Verificar"),
         ("Reutilizar", "Guardar plantilla")]),
    badge("🏆 Proyecto Completado", "Integraste todo lo aprendido en un proyecto real de principio a fin."),
])

# ============================ MODULO 9 (BONUS) =============================
LESSONS["L9-1"] = (9, 1, "Claude design y Constitutional AI", [
    intro(),
    content("La filosofia detras de Claude",
        "Claude se disena para ser util, honesto e inofensivo.\n\n"
        "En la practica esto se nota: tiende a razonar los matices en vez de bloquear cualquier tema sensible, y reconoce lo que no sabe en lugar de proyectar falsa certeza."),
    content("Que es Constitutional AI",
        "Constitutional AI es un metodo de entrenamiento donde el modelo aprende a seguir un conjunto de principios (una 'constitucion') para autoevaluar y mejorar sus respuestas.\n\n"
        "En vez de depender solo de etiquetas humanas, el modelo critica y revisa sus salidas segun esos principios."),
    content("Por que te importa como usuario",
        "• Respuestas mas matizadas en temas delicados\n• Menos rechazos automaticos sin sentido\n• Mayor honestidad sobre incertidumbre\n\n"
        "Entender esta filosofia te ayuda a pedir mejor y a interpretar por que responde como responde."),
    content("Honestidad calibrada",
        "Claude tiende a:\n• Admitir cuando no sabe algo\n• Senalar suposiciones\n• Evitar inventar con falsa seguridad\n\n"
        "Puedes potenciarlo pidiendo explicitamente nivel de confianza o que distinga hecho de opinion."),
    quiz("Que es Constitutional AI?",
        "Cual descripcion encaja mejor?",
        [("Un modelo entrenado con un conjunto de principios para autoevaluarse", True, "Correcto: aprende a seguir y aplicar una 'constitucion' de principios."),
         ("Una ley de internet", False, "No es legislacion; es un metodo de entrenamiento."),
         ("Un tipo de hardware", False, "No tiene que ver con hardware.")]),
    challenge("Reto: los 3 valores",
        "Claude se disena para ser util, honesto e ___. (una palabra)",
        "inofensivo", "Util, honesto e inofensivo (helpful, honest, harmless)."),
    matching("Diseno de Claude",
        [("Constitutional AI", "Principios para autoevaluar"),
         ("Util", "Resuelve tareas"),
         ("Honesto", "Reconoce limites"),
         ("Inofensivo", "Evita el dano")]),
    badge("🏛️ Conocedor del Diseno", "Entiendes la filosofia de Claude y Constitutional AI."),
])

LESSONS["L9-2"] = (9, 2, "Markdown como input estructurado", [
    intro(),
    content("Por que Markdown ayuda",
        "Markdown es una forma simple de estructurar texto con titulos, listas, tablas y bloques de codigo.\n\n"
        "Cuando estructuras tu prompt en Markdown, Claude entiende mejor la jerarquia y responde de forma mas organizada."),
    content("Elementos utiles",
        "• # Titulos para secciones\n• - o * para listas\n• 1. para pasos ordenados\n• `codigo` y bloques con triple backtick\n• | tablas | para datos\n\n"
        "Usa la estructura para separar instruccion, datos y formato."),
    example("Prompt en Markdown",
        "# Tarea\nClasifica los tickets por prioridad.\n\n"
        "## Reglas\n- Critico: afecta a produccion\n- Alto: afecta a un usuario\n- Bajo: cosmetico\n\n"
        "## Datos\n```\n...tickets...\n```\n\n"
        "## Formato\nTabla con columnas: ticket, prioridad, motivo."),
    content("Pide salida en Markdown",
        "Tambien puedes pedir que la RESPUESTA venga en Markdown:\n• Tablas listas para pegar\n• Listas y titulos claros\n• Bloques de codigo bien formateados\n\n"
        "Ideal para documentacion, README y notas."),
    quiz("Para que sirve Markdown en un prompt?",
        "Cual es su principal ventaja?",
        [("Hace el texto mas bonito sin mas", False, "No es solo estetica: aporta estructura semantica."),
         ("Estructura la informacion para que Claude la entienda mejor", True, "Correcto: titulos, listas y bloques dan jerarquia clara."),
         ("Cifra el contenido", False, "No tiene nada que ver con cifrado.")]),
    challenge("Reto: simbolo de titulo",
        "Que simbolo se usa para un titulo de primer nivel en Markdown? (un caracter)",
        "#", "La almohadilla # marca un titulo (# = nivel 1)."),
    matching("Markdown",
        [("#", "Titulo"),
         ("-", "Lista"),
         ("```", "Bloque de codigo"),
         ("| |", "Tabla")]),
    badge("📝 Maestro del Markdown", "Usas Markdown para estructurar prompts y obtener salidas ordenadas."),
])

LESSONS["L9-3"] = (9, 3, "Skills de Claude", [
    intro(),
    content("Que son las Skills",
        "Las Skills son capacidades empaquetadas que Claude puede cargar cuando hacen falta: instrucciones, plantillas y a veces codigo para una tarea concreta.\n\n"
        "Ej: crear documentos Word, hojas Excel, presentaciones, PDFs o flujos especializados."),
    content("Como ayudan",
        "• Estandarizan tareas repetitivas\n• Aportan conocimiento experto de un dominio\n• Se activan solo cuando la tarea lo pide\n\n"
        "Es como darle a Claude un manual especializado justo para lo que necesitas."),
    content("Cuando se usan",
        "Claude reconoce que una skill encaja con tu peticion y la carga.\n\n"
        "Ej: pides 'hazme un .docx con este informe' y se activa la skill de documentos para producirlo con buen formato."),
    content("Skills + herramientas",
        "Las Skills se combinan con conectores (MCP) y con la generacion de archivos:\n• Skill define COMO hacer bien la tarea\n• Herramientas dan acceso a datos o acciones\n\n"
        "Juntas convierten a Claude en un especialista practico."),
    quiz("Que es una Skill?",
        "Cual definicion encaja mejor?",
        [("Una capacidad empaquetada que Claude carga para una tarea", True, "Correcto: instrucciones/plantillas/codigo para hacer bien algo concreto."),
         ("Un modelo distinto de Claude", False, "No es un modelo, es una capacidad que se activa."),
         ("Un tipo de suscripcion", False, "No es un plan de pago.")]),
    challenge("Reto: ejemplo de skill",
        "Que extension produce la skill de documentos de Word? (incluye el punto)",
        ".docx", "La skill de Word genera archivos .docx."),
    matching("Skills",
        [("Skill", "Capacidad empaquetada"),
         ("Activacion", "Cuando la tarea encaja"),
         ("Ejemplo", "Crear .docx/.xlsx"),
         ("Combina con", "Conectores MCP")]),
    badge("🧰 Usuario de Skills", "Sabes que son las Skills y como amplian lo que Claude puede hacer."),
])

LESSONS["L9-4"] = (9, 4, "Como construir un agente", [
    intro(),
    content("Que es un agente",
        "Un agente es Claude trabajando de forma autonoma hacia un objetivo: planifica, usa herramientas, observa resultados y ajusta, en un bucle, hasta terminar.\n\n"
        "A diferencia de una sola respuesta, un agente ejecuta varios pasos por si mismo."),
    content("El bucle agentico",
        "1) Recibe un objetivo\n2) Planifica los pasos\n3) Usa una herramienta (buscar, leer, escribir, llamar API)\n4) Observa el resultado\n5) Decide el siguiente paso\n6) Repite hasta cumplir el objetivo"),
    content("Ingredientes de un buen agente",
        "• Objetivo claro y medible\n• Herramientas adecuadas (via MCP u otras)\n• Limites y permisos (que puede y que no)\n• Criterio de parada (cuando termina)\n• Supervision humana en pasos sensibles"),
    content("Donde brillan los agentes",
        "• Tareas multi-paso (investigar + resumir + redactar)\n• Flujos entre varias apps\n• Procesos repetitivos con decisiones\n\n"
        "Para tareas de un solo paso, un agente es exceso: basta un buen prompt."),
    quiz("Que define a un agente?",
        "Cual es la caracteristica clave?",
        [("Da una sola respuesta y termina", False, "Eso es una respuesta normal, no un agente."),
         ("Planifica y ejecuta varios pasos con herramientas hacia un objetivo", True, "Correcto: actua en bucle de forma autonoma."),
         ("Es un modelo mas pequeno", False, "No es cuestion de tamano de modelo.")]),
    challenge("Reto: pieza imprescindible",
        "Para que un agente no se ejecute sin fin, necesita un criterio de ___. (una palabra)",
        "parada", "Un criterio de parada define cuando ha terminado."),
    matching("Agentes",
        [("Agente", "Autonomo y multi-paso"),
         ("Bucle", "Planear-actuar-observar"),
         ("Herramientas", "Como actua"),
         ("Seguridad", "Limites y supervision")]),
    badge("🤖 Constructor de Agentes", "Entiendes el bucle agentico y como disenar un agente."),
])

LESSONS["L9-5"] = (9, 5, "MCP — Model Context Protocol", [
    intro(),
    content("Repaso: que resuelve MCP",
        "MCP es el estandar que conecta a Claude (y a los agentes) con herramientas y datos externos de forma uniforme.\n\n"
        "Sin un estandar, cada integracion seria a medida; con MCP, las herramientas hablan un lenguaje comun."),
    content("Componentes clave",
        "• Servidor MCP: expone herramientas y recursos\n• Herramientas: acciones que Claude puede ejecutar\n• Recursos: datos que Claude puede leer\n• Cliente: la app (como Claude) que los usa"),
    content("Por que es importante para agentes",
        "Un agente necesita 'manos' para actuar. MCP le da acceso estandar a esas manos:\n• Leer una base de datos\n• Crear un evento\n• Enviar un mensaje (con permiso)\n\n"
        "Cuantas mas herramientas via MCP, mas cosas puede automatizar."),
    example("Idea de un servidor MCP minimo",
        "// Pseudocodigo conceptual\n"
        "servidor.herramienta('crear_tarea', (titulo, fecha) => {\n"
        "  // crea la tarea en tu sistema\n"
        "  return { ok: true };\n"
        "});\n"
        "// Claude descubre 'crear_tarea' y la usa cuando hace falta"),
    content("Seguridad en MCP",
        "• Define que herramientas expones\n• Limita permisos al minimo\n• Pide confirmacion en acciones sensibles\n• Registra (log) lo que se ejecuta\n\n"
        "Dar 'manos' a un agente exige control de accesos serio."),
    quiz("Que expone un servidor MCP?",
        "Que dos cosas principales ofrece?",
        [("Herramientas (acciones) y recursos (datos)", True, "Correcto: acciones que ejecutar y datos que leer."),
         ("Solo imagenes", False, "No se limita a imagenes."),
         ("Modelos de IA nuevos", False, "No sirve modelos; sirve herramientas y datos.")]),
    challenge("Reto: rol del componente",
        "El componente MCP que ejecuta una accion (crear, enviar, buscar) se llama... (una palabra)",
        "herramienta", "Las herramientas (tools) son las acciones que expone el servidor."),
    matching("MCP a fondo",
        [("Servidor", "Expone capacidades"),
         ("Herramienta", "Accion ejecutable"),
         ("Recurso", "Dato legible"),
         ("Cliente", "App que las usa")]),
    badge("🌉 Arquitecto MCP", "Dominas los componentes de MCP y su papel en los agentes."),
])

LESSONS["L9-6"] = (9, 6, "Construye tu primer agente", [
    intro(),
    content("De la teoria a la practica",
        "Vamos a juntar todo: objetivo, herramientas (MCP), bucle agentico y supervision para disenar un primer agente sencillo y util."),
    content("Paso 1: define el objetivo",
        "Elige algo acotado y repetitivo. Ejemplos:\n• 'Cada manana, resume mis emails sin leer y crea tareas'\n• 'Investiga un tema y entrega un informe con fuentes'\n\n"
        "Un objetivo claro hace al agente facil de evaluar."),
    content("Paso 2: elige herramientas y limites",
        "• Que datos necesita leer? (email, calendario, web)\n• Que acciones puede hacer? (crear tarea, enviar borrador)\n• Que NO puede hacer sin tu OK? (enviar, borrar, pagar)\n\n"
        "Menos permisos = mas seguro."),
    content("Paso 3: disena el bucle y la parada",
        "• Plan -> accion -> observacion -> decision\n• Define cuando termina (objetivo cumplido o limite de pasos)\n• Anade puntos de control humanos en lo sensible\n\n"
        "Empieza simple; anade complejidad solo si hace falta."),
    example("Brief de tu primer agente",
        "Objetivo: resumir novedades del sector y entregar un informe.\n"
        "Herramientas: busqueda web (leer), generador de documentos (escribir).\n"
        "Limites: no publicar nada; solo crear un borrador.\n"
        "Parada: cuando entrega el .docx con 5 fuentes citadas.\n"
        "Control humano: yo reviso antes de compartir."),
    quiz("Como empezar tu primer agente?",
        "Que tipo de objetivo conviene para el primero?",
        [("Algo enorme y abierto", False, "Dificil de evaluar y controlar."),
         ("Algo acotado y repetitivo", True, "Correcto: facil de definir, medir y supervisar."),
         ("Algo sin objetivo claro", False, "Sin objetivo no hay criterio de exito.")]),
    challenge("Reto: seguridad",
        "Para acciones sensibles, el agente debe pedir... antes de ejecutarlas. (una palabra que empieza por C: confirmacion o control)",
        "confirmacion", "Pedir confirmacion humana en acciones sensibles es esencial."),
    matching("Tu primer agente",
        [("Objetivo", "Acotado y medible"),
         ("Herramientas", "Leer y escribir"),
         ("Limites", "Permisos minimos"),
         ("Parada", "Cuando cumple meta")]),
    badge("🚀 Primer Agente Construido", "Sabes disenar tu primer agente: objetivo, herramientas, bucle y control."),
])


def render_all():
    template = TEMPLATE.read_text(encoding="utf-8")
    count = 0
    for lid, (m, l, title, slides) in LESSONS.items():
        mod_title, short, color = MODULES[m]
        json_str = json.dumps(slides, ensure_ascii=False)

        lines = template.split("\n")
        for i, line in enumerate(lines):
            if line.strip().startswith("const slides ="):
                lines[i] = "        const slides = " + json_str + ";"
                break
        t = "\n".join(lines)

        # contador total de slides
        t = t.replace('<span id="cnt">1</span>/17',
                      '<span id="cnt">1</span>/%d' % len(slides))
        # storage key unico
        t = t.replace("total_points_m1l1", "total_points_m%dl%d" % (m, l))
        # titulo del documento
        t = t.replace("<title>L1-1</title>", "<title>%s</title>" % lid)
        # eyebrow
        t = t.replace("M1 • L1 • Fundamentos",
                      "M%d • L%d • %s" % (m, l, short))
        # etiqueta de modulo/leccion (header + intro)
        t = t.replace("Módulo 1 - Lección 1",
                      "Módulo %d - Lección %d" % (m, l))
        # color del modulo
        t = t.replace("#3B82F6", color)

        (SLIDES_DIR / ("%s-slides.html" % lid)).write_text(t, encoding="utf-8")
        count += 1
        print("  generado %s (%d slides) -> %s" % (lid, len(slides), color))
    print("Total generado: %d archivos" % count)


if __name__ == "__main__":
    render_all()
