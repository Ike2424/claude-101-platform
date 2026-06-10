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
        "Claude no es un unico modelo: es una familia con varios tamanos pensados para distintas necesidades.\n\n"
        "Los tres perfiles clasicos son Haiku, Sonnet y Opus, ordenados de mas ligero a mas potente.\n\n"
        "La idea central de toda la leccion: no existe 'el mejor modelo', existe 'el mejor modelo para ESTA tarea'. Aprender a elegir te ahorra tiempo y dinero."),
    content("La analogia de los vehiculos",
        "Para fijar la idea, piensa en transporte:\n\n"
        "🛵 Haiku = una moto\n• Agil, barata, perfecta para trayectos cortos y frecuentes\n\n"
        "🚗 Sonnet = un coche\n• Equilibrio entre velocidad, capacidad y consumo. Sirve para casi todo\n\n"
        "🚚 Opus = un camion\n• Mueve cargas pesadas, pero es mas lento y caro de operar\n\n"
        "Nadie usa un camion para ir a por el pan, ni una moto para una mudanza."),
    content("Haiku: rapido y ligero",
        "El mas veloz y economico de la familia.\n\n"
        "Ideal para:\n• Tareas simples y de alto volumen\n• Clasificacion (spam/no spam, positivo/negativo)\n• Extraccion de datos sencillos\n• Respuestas cortas donde la latencia importa\n\n"
        "Piensa en el para automatizaciones que corren miles de veces: cada milisegundo y cada centimo se multiplican."),
    content("Sonnet: el equilibrio (el que mas usaras)",
        "El punto medio entre velocidad y capacidad. Para la mayoria de la gente es el modelo del dia a dia.\n\n"
        "Ideal para:\n• Redaccion y edicion de textos\n• Analisis de documentos\n• Programacion cotidiana\n• Tareas con buen razonamiento sin esperar demasiado\n\n"
        "Regla practica: empieza SIEMPRE por Sonnet. Solo cambia si una tarea concreta te pide menos (Haiku) o mas (Opus)."),
    content("Opus: la maxima capacidad",
        "El mas potente para problemas verdaderamente complejos.\n\n"
        "Ideal para:\n• Razonamiento profundo y multi-paso\n• Analisis matizado de temas delicados\n• Escritura sofisticada y de marca\n• Problemas donde un error sale caro\n\n"
        "Es mas lento y costoso, asi que reservalo para cuando la calidad pesa mas que el tiempo o el dinero."),
    content("El triangulo: velocidad, capacidad, costo",
        "Toda eleccion de modelo equilibra tres fuerzas:\n\n"
        "⚡ Velocidad: cuanto tarda en responder\n🧠 Capacidad: que tan complejo puede razonar\n💰 Costo: cuanto cuesta cada uso\n\n"
        "No puedes maximizar las tres a la vez. Haiku prioriza velocidad/costo; Opus prioriza capacidad; Sonnet busca el centro.\n\n"
        "Elegir bien = saber cual de las tres fuerzas domina TU tarea."),
    content("Como elegir en 3 preguntas",
        "Hazte estas preguntas en orden:\n\n"
        "1. Es una tarea simple y repetitiva (clasificar, extraer)?\n   -> Haiku\n\n"
        "2. Es trabajo general del dia a dia (escribir, analizar, programar)?\n   -> Sonnet\n\n"
        "3. Es muy compleja y un error sale caro?\n   -> Opus\n\n"
        "Ante la duda, Sonnet casi nunca falla como punto de partida."),
    content("Errores comunes al elegir",
        "❌ Usar siempre el mas potente 'por si acaso'\n• Pagas de mas y esperas de mas sin necesidad\n\n"
        "❌ Usar el mas barato para todo\n• Te frustras cuando se queda corto en tareas complejas\n\n"
        "❌ No probar alternativas\n• A veces Haiku resuelve algo que creias que necesitaba Opus\n\n"
        "✅ Lo sano: prototipa con Sonnet, mide, y ajusta hacia arriba o abajo."),
    content("El mismo prompt, distinto modelo",
        "Una buena practica: prueba tu tarea en dos modelos y compara.\n\n"
        "• Si Haiku da un resultado igual de bueno que Sonnet -> usa Haiku y ahorra\n• Si Sonnet falla en matiz -> sube a Opus solo en esa tarea\n\n"
        "La eleccion no es para siempre: puedes usar modelos distintos para partes distintas de un mismo flujo."),
    example("Pensar la eleccion como codigo",
        "# Pseudocodigo de decision\n"
        "def elegir_modelo(tarea):\n"
        "    if tarea.es_simple and tarea.alto_volumen:\n"
        "        return 'haiku'    # rapido y barato\n"
        "    if tarea.es_muy_compleja or tarea.error_caro:\n"
        "        return 'opus'     # maxima capacidad\n"
        "    return 'sonnet'       # el equilibrio por defecto"),
    quiz("Cual modelo para alto volumen simple?",
        "Necesitas clasificar miles de mensajes cortos lo mas rapido y barato posible. Cual eliges?",
        [("Haiku", True, "Correcto: el mas rapido y economico, ideal para volumen simple."),
         ("Opus", False, "Seria potente pero lento y caro para una tarea simple."),
         ("Ninguno sirve", False, "Haiku encaja perfecto en este caso.")]),
    quiz("Cual es el modelo 'por defecto'?",
        "Para el trabajo general del dia a dia, por cual conviene empezar?",
        [("Opus siempre", False, "Suele ser excesivo y caro para tareas cotidianas."),
         ("Sonnet", True, "Correcto: el mejor equilibrio para la mayoria de tareas."),
         ("Haiku para todo", False, "Haiku se queda corto en razonamiento complejo.")]),
    quiz("Cuando subir a Opus?",
        "En cual situacion tiene mas sentido pagar por Opus?",
        [("Para traducir una frase corta", False, "Eso lo hace Haiku de sobra."),
         ("Para un analisis legal complejo donde un error sale caro", True, "Correcto: maxima capacidad cuando la calidad es critica."),
         ("Para clasificar tickets por volumen", False, "Volumen simple = Haiku.")]),
    challenge("Reto: el equilibrado",
        "Cual de los tres modelos es el equilibrio recomendado para empezar el dia a dia? (una palabra)",
        "Sonnet", "Sonnet es el punto medio entre velocidad y capacidad."),
    matching("Modelo y perfil",
        [("Haiku", "Rapido y economico"),
         ("Sonnet", "Equilibrio del dia a dia"),
         ("Opus", "Maxima capacidad"),
         ("Velocidad", "Cuanto tarda"),
         ("Costo", "Cuanto cuesta cada uso")]),
    content("Resumen de la leccion",
        "• Claude es una familia: Haiku, Sonnet, Opus\n"
        "• Cada uno equilibra velocidad, capacidad y costo de forma distinta\n"
        "• Empieza por Sonnet; baja a Haiku para lo simple, sube a Opus para lo complejo\n"
        "• La eleccion la decide la tarea, no el ego de usar 'el mas grande'\n\n"
        "En la siguiente leccion abrimos el capo: como razona Claude por dentro."),
    badge("🧬 Conocedor de Modelos", "Sabes elegir entre Haiku, Sonnet y Opus equilibrando velocidad, capacidad y costo."),
])

LESSONS["L1-3"] = (1, 3, "Como razona Claude", [
    intro(),
    content("Predice, no consulta",
        "Claude genera texto prediciendo, palabra a palabra, lo mas probable segun los patrones que aprendio durante su entrenamiento.\n\n"
        "No consulta una base de datos ni 'busca' la respuesta en ningun sitio: la CONSTRUYE sobre la marcha.\n\n"
        "Esta sola idea explica casi todo su comportamiento: por que es tan flexible, por que a veces se equivoca, y por que el contexto que le das cambia tanto el resultado."),
    content("La maquina de autocompletar (muy potente)",
        "En el fondo, Claude es un autocompletado extraordinariamente sofisticado.\n\n"
        "• Mira todo el texto hasta ahora (tu prompt + lo que lleva escrito)\n• Calcula que palabra es la mas probable que venga despues\n• La escribe, y repite\n\n"
        "Lo asombroso es que, a partir de ese mecanismo simple, emergen razonamiento, traduccion y creatividad. Pero en su nucleo sigue siendo prediccion."),
    content("Que son los tokens",
        "Claude no ve 'palabras' exactamente, ve tokens: trozos de texto.\n\n"
        "• Un token es ~4 caracteres en promedio\n• Una palabra suele ser 1-2 tokens\n• 1000 palabras ≈ 1300 tokens\n\n"
        "Importa porque: el costo y el limite de contexto se miden en tokens, no en palabras. Textos mas largos = mas tokens = mas costo y mas tiempo."),
    content("El context window: su memoria de trabajo",
        "El context window es todo el texto que Claude puede 'tener presente' a la vez en una conversacion.\n\n"
        "• Incluye tus instrucciones + el material + toda la charla previa\n• Es enorme: caben decenas o cientos de paginas\n• Pero tiene un limite: lo mas antiguo puede salir si la conversacion crece mucho\n\n"
        "Es su memoria a corto plazo: dentro de ella recuerda todo; fuera, no."),
    content("Que es 'alucinar'",
        "Una alucinacion es cuando Claude da una respuesta que suena segura y plausible pero es falsa.\n\n"
        "No miente a proposito: como genera por probabilidad, a veces el texto 'mas probable' no es el verdadero.\n\n"
        "Ocurre mas en:\n• Cifras y datos muy especificos\n• Citas, fechas y nombres propios\n• Temas muy recientes o de nicho\n\n"
        "La seguridad del tono NO garantiza que tenga razon."),
    content("Por que el tono seguro engana",
        "Claude siempre escribe con fluidez, tenga razon o no. Esa fluidez puede dar una falsa sensacion de certeza.\n\n"
        "Regla de oro:\n• Para ideas, redaccion y brainstorming -> confia y itera\n• Para datos verificables (numeros, leyes, citas) -> verifica siempre\n\n"
        "Trata a Claude como un colega brillante pero que a veces se equivoca con seguridad."),
    content("Puede pensar paso a paso",
        "En problemas complejos, Claude rinde mucho mejor si razona ANTES de dar la respuesta final.\n\n"
        "Pedir 'piensa paso a paso' le hace:\n• Descomponer el problema en partes\n• Mostrar calculos intermedios\n• Detectar sus propios errores\n• Llegar a conclusiones mas fiables\n\n"
        "Es una de las tecnicas mas potentes; la veras a fondo en el modulo 4."),
    content("Probabilidad = variabilidad",
        "Como genera por probabilidades, la misma pregunta puede dar respuestas algo distintas cada vez.\n\n"
        "• Es normal, no es un fallo\n• A veces es util (variedad de ideas)\n• A veces molesta (quieres consistencia)\n\n"
        "Para resultados mas consistentes: da instrucciones precisas, formato fijo y ejemplos. Cuanto mas acotas, menos varia."),
    content("Conocimiento con fecha de corte",
        "Claude se entrena hasta cierta fecha y no conoce nada posterior por si solo.\n\n"
        "• No sabe la noticia de hoy\n• No conoce tus documentos privados\n• No sabe la hora actual si no se la dices\n\n"
        "Para datos recientes, usa busqueda web; para datos tuyos, pegalos en el prompt. Lo veremos en M5 y M7."),
    example("Hacer que razone en voz alta",
        "Resuelve este problema paso a paso, mostrando cada calculo,\n"
        "y solo al final escribe la respuesta:\n\n"
        "Un articulo cuesta 80€. Le aplico una subida del 25%\n"
        "y luego un descuento del 10%. Cual es el precio final?\n\n"
        "# Claude razona:\n# 1) 80 x 1.25 = 100\n# 2) 100 x 0.90 = 90\n# Respuesta: 90€"),
    quiz("Como genera Claude sus respuestas?",
        "Cual descripcion es la correcta?",
        [("Busca la respuesta en internet", False, "No navega por defecto; predice el texto."),
         ("Predice el texto mas probable segun patrones aprendidos", True, "Correcto: genera por probabilidad, no por consulta."),
         ("Copia de una base de datos fija", False, "No copia de una base de datos; construye la respuesta.")]),
    quiz("Que es una alucinacion?",
        "Como se describe mejor?",
        [("Un fallo de conexion a internet", False, "No es un problema tecnico de red."),
         ("Una respuesta que suena segura pero es falsa", True, "Correcto: plausible en la forma, incorrecta en el fondo."),
         ("Cuando el modelo se apaga", False, "No tiene que ver con apagarse.")]),
    quiz("Como obtener respuestas mas consistentes?",
        "Si quieres que varie menos entre intentos, que ayuda mas?",
        [("Dar instrucciones precisas y formato fijo", True, "Correcto: acotar reduce la variabilidad."),
         ("Repetir la pregunta a secas", False, "Sin mas precision, seguira variando."),
         ("Pedir que sea creativo", False, "Eso aumenta la variabilidad, no la reduce.")]),
    challenge("Reto: el termino clave",
        "Como se llama cuando Claude responde con seguridad algo que es falso? (una palabra)",
        "alucinacion", "Se llama alucinacion (hallucination)."),
    challenge("Reto: unidad de texto",
        "Como se llama el trozo de texto (~4 caracteres) que Claude procesa? (una palabra)",
        "token", "Claude procesa el texto en tokens."),
    matching("Como razona Claude",
        [("Genera por", "Probabilidad"),
         ("Token", "Trozo de texto"),
         ("Context window", "Memoria de trabajo"),
         ("Alucinacion", "Seguro pero falso"),
         ("Mejor en complejo", "Paso a paso")]),
    content("Resumen de la leccion",
        "• Claude predice texto, no lo consulta: es autocompletado muy potente\n"
        "• Procesa tokens y recuerda dentro del context window\n"
        "• Puede alucinar: verifica datos criticos pese al tono seguro\n"
        "• Razona mejor paso a paso y varia entre intentos\n"
        "• Tiene fecha de corte: aporta tu el contexto reciente o privado\n\n"
        "Entender esto te convierte en alguien que GUIA al modelo en vez de pelearse con el."),
    badge("🧠 Mente de Claude", "Entiendes como razona Claude: prediccion, tokens, contexto, alucinaciones y razonamiento."),
])

LESSONS["L1-4"] = (1, 4, "Diferencias clave con otros asistentes", [
    intro(),
    content("No todos los asistentes son iguales",
        "Por fuera, muchos asistentes de IA se parecen: una caja de texto y respuestas. Pero por dentro se comportan distinto segun como fueron disenados y entrenados.\n\n"
        "Conocer los rasgos de Claude te ayuda a sacarle partido y a saber cuando es la mejor herramienta para el trabajo."),
    content("Rasgo 1: estilo mas natural",
        "Claude tiende a escribir de forma mas natural y menos formulaica.\n\n"
        "• Menos plantillas rigidas y muletillas tipo 'como modelo de lenguaje...'\n• Menos listas roboticas cuando un parrafo va mejor\n• Un tono que suena a redaccion humana cuidada\n\n"
        "Esto se nota mucho en escritura, donde el resultado necesita menos 'limpieza' despues."),
    content("Rasgo 2: honestidad calibrada",
        "En lugar de proyectar falsa certeza, Claude tiende a:\n• Reconocer cuando no sabe algo\n• Senalar sus suposiciones\n• Distinguir hecho de opinion\n\n"
        "No es perfecto (sigue pudiendo alucinar), pero su sesgo de diseno es hacia la honestidad, no hacia 'inventar para complacer'."),
    content("Rasgo 3: matiz en temas sensibles",
        "Donde otros asistentes bloquean cualquier tema delicado de golpe, Claude tiende a evaluar si hay dano real y a razonar los grises.\n\n"
        "• Menos rechazos automaticos sin sentido\n• Mas disposicion a tratar temas complejos con cuidado\n\n"
        "Esto viene de su entrenamiento con principios (Constitutional AI), que veras en el modulo 9 BONUS."),
    content("Rasgo 4: excelente en contextos largos",
        "Claude mantiene la coherencia en documentos extensos: puedes pegar muchas paginas y seguir obteniendo respuestas consistentes.\n\n"
        "Ideal para:\n• Analizar informes y contratos completos\n• Resumir libros o transcripciones largas\n• Entender bases de codigo enteras\n\n"
        "Mantiene el hilo donde otros se pierden."),
    content("Rasgo 5: fuerte en razonamiento y codigo",
        "Claude destaca especialmente en:\n• Razonamiento paso a paso\n• Escritura y reescritura de calidad\n• Generacion y revision de codigo\n\n"
        "No significa que sea el unico bueno en esto, pero son areas donde rinde de forma muy solida en el dia a dia."),
    content("Que NO lo hace especial (sé realista)",
        "Para mantener expectativas sanas, Claude (como todos) tambien:\n• Puede equivocarse con seguridad\n• No conoce eventos posteriores a su entrenamiento\n• No accede a tus datos sin que se los des\n• Varia entre respuestas\n\n"
        "La ventaja no es 'ser infalible', sino el estilo, la honestidad y el manejo de contexto."),
    content("Cuando Claude es la mejor opcion",
        "Brilla especialmente cuando necesitas:\n• Texto de calidad con poco retoque\n• Trabajar con documentos largos\n• Honestidad sobre incertidumbre\n• Tratar temas matizados con cuidado\n\n"
        "Para esas tareas, su forma de comportarse marca una diferencia practica real."),
    example("Comprobar la honestidad calibrada",
        "Prueba este prompt para ver el rasgo en accion:\n\n"
        "\"Responde solo si estas seguro. Si no lo sabes o no puedes\n"
        "verificarlo, dilo claramente en vez de inventar. Para cada dato,\n"
        "indica tu nivel de confianza (alto/medio/bajo).\"\n\n"
        "Veras como distingue lo que sabe de lo que supone."),
    quiz("Cual es un rasgo distintivo de Claude?",
        "Cual de estas describe mejor a Claude?",
        [("Tiene siempre razon", False, "Ningun modelo garantiza exactitud total."),
         ("Estilo natural y honestidad sobre lo que no sabe", True, "Correcto: redaccion natural y honestidad calibrada lo distinguen."),
         ("Nunca necesita contexto", False, "Como todos, rinde mejor con buen contexto.")]),
    quiz("En que tarea brilla especialmente?",
        "Cual aprovecha mejor sus fortalezas?",
        [("Recordar la noticia de hoy sin buscar", False, "No conoce eventos posteriores a su entrenamiento."),
         ("Analizar un contrato largo manteniendo coherencia", True, "Correcto: los contextos largos son una de sus fortalezas."),
         ("Garantizar cero errores en cifras", False, "Puede alucinar; los datos hay que verificarlos.")]),
    challenge("Reto: rasgo distintivo",
        "Claude mantiene coherencia en documentos ___ (una palabra: cortos o largos).",
        "largos", "Destaca en contextos largos manteniendo la coherencia."),
    matching("Diferencias de Claude",
        [("Estilo", "Natural, no formulaico"),
         ("Honestidad", "Reconoce lo que no sabe"),
         ("Temas sensibles", "Razona matices"),
         ("Fortaleza", "Contextos largos"),
         ("Tambien", "Puede equivocarse")]),
    content("Resumen del modulo 1",
        "Completaste los fundamentos:\n• Que es Claude y como accedes a el\n• La familia de modelos y como elegir\n• Como razona por dentro\n• Que lo distingue de otros asistentes\n\n"
        "Ya tienes la base. En el modulo 2 entramos en lo practico: la interfaz, conversaciones, proyectos y configuracion."),
    badge("🆚 Experto Comparativo", "Conoces que distingue a Claude y cuando es la mejor herramienta."),
])

# ============================ MODULO 2 =====================================
LESSONS["L2-2"] = (2, 2, "Anatomia de la interfaz", [
    intro(),
    content("Conoce tu espacio de trabajo",
        "Saber donde esta cada cosa te hace mucho mas rapido y te quita el miedo a 'romper algo'.\n\n"
        "La interfaz de Claude.ai se organiza en pocas zonas claras: el area de conversacion, el cuadro de mensaje, el historial lateral y los ajustes.\n\n"
        "En esta leccion recorremos cada una y los detalles que la mayoria pasa por alto."),
    content("El area de conversacion",
        "Es el centro de la pantalla: aqui aparece el ida y vuelta entre tus mensajes y las respuestas de Claude.\n\n"
        "• Se lee de arriba (mas antiguo) a abajo (mas reciente)\n• Cada respuesta puedes copiarla, regenerarla o editar tu mensaje\n• El hilo completo es el 'contexto' que Claude tiene presente\n\n"
        "Piensa en ella como una conversacion real que queda escrita."),
    content("El cuadro de mensaje",
        "Donde escribes, abajo del todo. Es tu punto de entrada para TODO:\n\n"
        "• Escribes tu prompt y envias con Enter\n• Shift+Enter hace salto de linea sin enviar (util para prompts largos)\n• Puedes adjuntar imagenes y archivos\n• Puedes pegar texto largo para que Claude lo analice\n\n"
        "Dominar este cuadro es dominar el 90% del uso diario."),
    content("Adjuntar archivos e imagenes",
        "Claude no solo lee texto que escribes: puede trabajar con lo que subes.\n\n"
        "• Imagenes: capturas, fotos, graficos, diagramas\n• Documentos: PDF, texto, hojas de datos\n• Varios a la vez para compararlos\n\n"
        "Ej: sube una foto de una factura y pide 'extrae el total y la fecha'. Lo veras a fondo en los modulos de capacidades y casos de uso."),
    content("Los Artifacts",
        "Cuando Claude crea algo sustancial (un documento, codigo, una pagina), suele abrirlo en un panel aparte llamado Artifact.\n\n"
        "• No se mezcla con el hilo de chat\n• Puedes leerlo, editarlo y descargarlo\n• Puedes pedir cambios sin reescribir todo\n\n"
        "Es la diferencia entre 'una respuesta' y 'un entregable'. Dedicamos una leccion entera a esto en M5."),
    content("El historial lateral",
        "Cada conversacion se guarda automaticamente en una lista a un lado.\n\n"
        "• Puedes volver a cualquier chat anterior\n• Renombralos para encontrarlos rapido ('Campana junio', 'Bug login')\n• Borra los que ya no necesites\n\n"
        "Un historial ordenado es como un escritorio limpio: encuentras todo y trabajas mejor."),
    content("Empezar un chat nuevo (cuando y por que)",
        "El boton de 'nuevo chat' hace mas de lo que parece: empieza con contexto LIMPIO.\n\n"
        "Abre uno nuevo cuando:\n• Cambias de tema por completo\n• El hilo se volvio muy largo y confuso\n• Quieres evitar que ideas viejas 'contaminen' la respuesta\n\n"
        "Quédate en el mismo hilo cuando sigues con el mismo tema y quieres que recuerde lo anterior."),
    content("Seleccionar modelo y opciones",
        "Segun tu plan, la interfaz te deja elegir el modelo (Haiku/Sonnet/Opus) y activar funciones como busqueda web.\n\n"
        "• El selector suele estar cerca del cuadro de mensaje\n• Cambiar de modelo afecta velocidad, capacidad y costo (recuerda M1-L2)\n\n"
        "No tengas miedo de experimentar: cambiar opciones no rompe nada."),
    example("Tu primera sesion ordenada",
        "1. Abre un chat nuevo\n"
        "2. Renombralo segun el tema: 'Plan de contenidos'\n"
        "3. Adjunta el documento de referencia\n"
        "4. Escribe tu peticion (Shift+Enter para varias lineas)\n"
        "5. Si crea un documento, editalo en el Artifact\n"
        "6. Tema distinto -> chat nuevo"),
    quiz("Donde se analiza un archivo que subes?",
        "Subes un PDF para que lo resuma. Donde interactuas principalmente?",
        [("En el cuadro de mensaje lo adjuntas y conversas sobre el", True, "Correcto: adjuntas en el cuadro de mensaje y trabajas en la conversacion."),
         ("En los ajustes de la cuenta", False, "Los ajustes no procesan archivos."),
         ("No se puede subir archivos", False, "Si se pueden adjuntar archivos e imagenes.")]),
    quiz("Cuando conviene un chat nuevo?",
        "Cual es el mejor momento para empezar conversacion nueva?",
        [("Cuando cambias por completo de tema", True, "Correcto: contexto limpio evita que ideas viejas interfieran."),
         ("Cuando quieres que recuerde lo anterior", False, "Para eso te quedas en el mismo hilo."),
         ("Nunca, todo en un solo chat", False, "Un mega-hilo se vuelve confuso y pierde foco.")]),
    challenge("Reto: atajo util",
        "Que tecla combinas con Enter para hacer un salto de linea sin enviar? (una palabra)",
        "Shift", "Shift+Enter inserta salto de linea sin enviar el mensaje."),
    matching("Zonas de la interfaz",
        [("Conversacion", "Mensajes y respuestas"),
         ("Cuadro de mensaje", "Escribir y adjuntar"),
         ("Artifact", "Documento en panel aparte"),
         ("Historial", "Chats guardados"),
         ("Chat nuevo", "Contexto limpio")]),
    content("Resumen de la leccion",
        "• El area de conversacion es el hilo (y el contexto) de Claude\n"
        "• El cuadro de mensaje: escribir, adjuntar, Shift+Enter\n"
        "• Los Artifacts abren entregables editables en panel aparte\n"
        "• El historial guarda y organiza tus chats\n"
        "• Nuevo chat = contexto limpio para temas distintos\n\n"
        "Con el mapa claro, en la siguiente leccion organizamos el trabajo con conversaciones, proyectos y estilos."),
    badge("🧭 Guia de la Interfaz", "Te mueves con soltura por toda la interfaz de Claude."),
])

LESSONS["L2-3"] = (2, 3, "Conversaciones, proyectos y estilos", [
    intro(),
    content("De chats sueltos a un sistema",
        "Mucha gente usa la IA como un monton de chats desordenados y pierde tiempo repitiendo contexto.\n\n"
        "Claude ofrece tres herramientas para trabajar con metodo: conversaciones, proyectos y estilos.\n\n"
        "Entender cuando usar cada una es lo que separa al usuario casual del que va en serio."),
    content("Conversaciones: la unidad basica",
        "Cada chat es una conversacion independiente con su propio contexto (su propia memoria de trabajo).\n\n"
        "• Agrupa un tema en un mismo hilo para que Claude recuerde lo dicho\n• Abre uno nuevo para asuntos distintos\n• Renombralos para reencontrarlos\n\n"
        "Hilos enfocados = respuestas mas precisas. Hilos gigantes mezclando temas = confusion."),
    content("Buenas practicas con conversaciones",
        "• Un tema, un hilo: 'Campana de verano' separado de 'Soporte tecnico'\n• Si el hilo se desvia mucho, abre uno nuevo\n• Resume tu mismo los puntos clave si la charla se alarga\n• Borra o archiva lo que ya no usas\n\n"
        "Tratar los hilos con orden es como nombrar bien tus carpetas: tu yo futuro lo agradece."),
    content("Proyectos: contexto reutilizable",
        "Un proyecto es un espacio que agrupa conversaciones y guarda contexto que se aplica a TODAS ellas.\n\n"
        "Puedes anadir:\n• Instrucciones permanentes (como debe comportarse)\n• Documentos de referencia (que siempre tenga a mano)\n\n"
        "Asi, cada chat dentro del proyecto ya 'conoce' tu contexto sin que lo repitas."),
    content("Cuando usar un proyecto",
        "Los proyectos brillan en trabajo recurrente:\n\n"
        "• Un cliente fijo con sus documentos y tono\n• Una asignatura o investigacion en curso\n• Tu negocio: productos, voz de marca, politicas\n• Un producto de software con su documentacion\n\n"
        "Si te ves pegando el mismo contexto una y otra vez, eso deberia ser un proyecto."),
    content("Estilos: tu voz consistente",
        "Los estilos definen COMO responde Claude: tono, formato y nivel de detalle.\n\n"
        "• Puedes elegir estilos predefinidos (formal, conciso, explicativo...)\n• Puedes crear el tuyo para que suene a TI o a tu marca\n\n"
        "Lo defines una vez y se aplica a tus respuestas, sin tener que pedir el tono en cada mensaje."),
    content("Como combinar las tres",
        "Las tres herramientas se potencian juntas:\n\n"
        "• Proyecto -> guarda el QUE (contexto y documentos)\n• Estilo -> fija el COMO (tono y formato)\n• Conversaciones -> cada tarea concreta dentro de ese marco\n\n"
        "Ejemplo: proyecto 'Mi tienda' + estilo 'cercano y breve' + un hilo por cada campana."),
    example("Montar tu sistema en 4 pasos",
        "1. Crea un proyecto: 'Marketing de mi negocio'\n"
        "2. Anade instrucciones: 'Publico: pymes. Tono: cercano, claro.'\n"
        "3. Sube referencia: tu catalogo y tu guia de marca\n"
        "4. Crea un estilo propio y, dentro, un hilo por cada tarea\n\n"
        "A partir de ahi, cada chat ya sabe quien eres y como hablar."),
    quiz("Que usar para contexto reutilizable?",
        "Trabajas cada semana sobre el mismo cliente con documentos fijos. Que conviene usar?",
        [("Un chat nuevo cada vez sin mas", False, "Perderias el contexto una y otra vez."),
         ("Un proyecto que guarde el contexto", True, "Correcto: los proyectos conservan instrucciones y documentos reutilizables."),
         ("Cambiar de cuenta", False, "No tiene sentido para este caso.")]),
    quiz("Para que sirve un estilo?",
        "Que controla principalmente un estilo?",
        [("La velocidad del modelo", False, "El estilo no cambia la velocidad."),
         ("El tono, formato y nivel de detalle de las respuestas", True, "Correcto: define el COMO responde Claude."),
         ("Los documentos que recuerda", False, "Eso lo hacen los proyectos, no los estilos.")]),
    challenge("Reto: la voz consistente",
        "Que funcion define el tono y formato de las respuestas de Claude? (una palabra)",
        "estilos", "Los estilos (o estilo) controlan tono, formato y detalle."),
    matching("Organizacion",
        [("Conversacion", "Un tema, un hilo"),
         ("Proyecto", "Contexto reutilizable"),
         ("Estilo", "Tono y formato"),
         ("Chat nuevo", "Tema distinto"),
         ("Combinar", "Proyecto + estilo + hilos")]),
    content("Resumen de la leccion",
        "• Conversaciones: la unidad basica; un tema por hilo\n"
        "• Proyectos: guardan contexto y documentos reutilizables\n"
        "• Estilos: fijan tu voz (tono y formato)\n"
        "• Juntos: un sistema que deja de hacerte repetir contexto\n\n"
        "Te falta un ultimo paso para dominar tu entorno: la configuracion esencial."),
    badge("🗂️ Organizador Pro", "Usas conversaciones, proyectos y estilos para trabajar con sistema."),
])

LESSONS["L2-4"] = (2, 4, "Configuracion esencial", [
    intro(),
    content("Ajusta Claude a tu medida",
        "Unos minutos en los ajustes, una sola vez, mejoran TODAS tus conversaciones futuras.\n\n"
        "En esta leccion repasamos las opciones que de verdad importan: perfil, privacidad, apariencia y plan.\n\n"
        "No necesitas tocar todo: con revisar estos cuatro bloques vas sobrado."),
    content("Perfil e instrucciones personales",
        "Puedes darle a Claude contexto sobre ti que se aplique a todas las conversaciones:\n\n"
        "• Como te llamas y a que te dedicas\n• Tu idioma y tono preferido\n• Como te gusta recibir las respuestas (breves, con ejemplos, etc.)\n\n"
        "Es el ajuste de mayor impacto: lo configuras una vez y dejas de repetir tu contexto en cada chat."),
    content("Como escribir buenas instrucciones de perfil",
        "Piensa en lo que repetirias en casi cada conversacion:\n\n"
        "Ejemplos utiles:\n• 'Soy duena de una pyme de reposteria; explicame sin tecnicismos'\n• 'Responde en espanol, directo y conciso'\n• 'Cuando des codigo, anade comentarios'\n\n"
        "Cuanto mas claras, mas se ajustan las respuestas a ti desde el primer mensaje."),
    content("Privacidad y datos",
        "Tomate un momento para entender como se tratan tus datos:\n\n"
        "• Que se guarda de tus conversaciones y por cuanto tiempo\n• Las opciones sobre el uso de tus datos que ofrece tu cuenta\n• La politica de tu empresa si usas una cuenta de trabajo\n\n"
        "Conocer estos ajustes te da control. Profundizamos en privacidad en el modulo 7."),
    content("Que NO compartir nunca",
        "Independiente de la configuracion, evita pegar:\n\n"
        "• Contrasenas, claves API o tokens\n• Datos sensibles de terceros sin necesidad\n• Informacion bajo acuerdos de confidencialidad\n\n"
        "Regla simple: comparte solo lo imprescindible para la tarea. Lo veras como 'minimizacion' en M7."),
    content("Apariencia y accesibilidad",
        "Pequenos ajustes que reducen la fatiga en sesiones largas:\n\n"
        "• Tema claro u oscuro segun tu comodidad visual\n• Tamano de texto si tu plataforma lo permite\n\n"
        "El tema oscuro ayuda mucho de noche. No es estetica tonta: cuidar la vista te deja trabajar mas tiempo sin cansancio."),
    content("Plan, modelos y limites",
        "Conoce que incluye tu plan para planificar sin sorpresas:\n\n"
        "• Que modelos y funciones tienes disponibles\n• Si hay limites de uso y de que tipo\n• Que funciones extra desbloquea un plan superior\n\n"
        "Saber tus limites te ayuda a repartir tareas grandes y a decidir si te compensa subir de plan."),
    content("Checklist de configuracion inicial",
        "Hazlo una vez y olvidate:\n\n"
        "✅ Rellenar instrucciones de perfil (quien eres, idioma, tono)\n"
        "✅ Revisar ajustes de privacidad/datos\n"
        "✅ Elegir tema claro/oscuro\n"
        "✅ Mirar que incluye tu plan\n"
        "✅ (Opcional) Crear un estilo propio\n\n"
        "Cinco minutos que mejoran cada conversacion futura."),
    example("Plantilla de instrucciones de perfil",
        "Sobre mi:\n"
        "- Me llamo [NOMBRE] y trabajo en [SECTOR].\n"
        "- Idioma: espanol. Tono: cercano pero profesional.\n\n"
        "Como quiero las respuestas:\n"
        "- Directas y al grano, sin relleno.\n"
        "- Con un ejemplo cuando ayude.\n"
        "- Si no estas seguro de un dato, dimelo."),
    quiz("Para que sirven las instrucciones personales?",
        "Que ventaja dan las instrucciones de perfil?",
        [("Aplican contexto sobre ti a todas las conversaciones", True, "Correcto: evitan repetir tu contexto en cada chat."),
         ("Hacen el modelo mas rapido", False, "No afectan la velocidad."),
         ("Borran el historial", False, "No tienen que ver con borrar chats.")]),
    quiz("Que NO deberias compartir nunca?",
        "Cual es el dato mas peligroso de pegar en un chat?",
        [("Tu idioma preferido", False, "Eso es justo lo que conviene indicar."),
         ("Tu clave API o una contrasena", True, "Correcto: las credenciales nunca deben ir en un prompt."),
         ("El sector en el que trabajas", False, "Es contexto util y de bajo riesgo.")]),
    challenge("Reto: comodidad visual",
        "Que ajuste cambias para reducir la fatiga visual de noche: el ___ oscuro. (una palabra)",
        "tema", "El tema oscuro (modo oscuro) ayuda en sesiones nocturnas."),
    matching("Configuracion",
        [("Instrucciones", "Contexto sobre ti"),
         ("Privacidad", "Control de datos"),
         ("Apariencia", "Tema y texto"),
         ("Plan", "Modelos y limites"),
         ("Nunca compartir", "Claves y contrasenas")]),
    content("Resumen del modulo 2",
        "Ya dominas tu entorno de trabajo:\n• La interfaz y sus zonas\n• Conversaciones, proyectos y estilos\n• La configuracion esencial a tu medida\n\n"
        "Con las herramientas claras, en el modulo 3 empieza la magia de verdad: el arte de escribir buenos prompts."),
    badge("⚙️ Configurador Experto", "Tienes Claude ajustado a tu medida: perfil, privacidad, apariencia y plan."),
])

# ============================ MODULO 3 =====================================
LESSONS["L3-1"] = (3, 1, "Anatomia de un buen prompt", [
    intro(),
    content("El prompt es el volante",
        "Un prompt es la instruccion que le das a Claude. Es, literalmente, el volante: la calidad de tu resultado depende casi por completo de como lo escribas.\n\n"
        "La buena noticia: escribir buenos prompts no es magia ni programacion. Es una habilidad con reglas claras que cualquiera puede aprender.\n\n"
        "Este modulo entero va de eso. Y empieza por la anatomia: las partes de las que se compone un buen prompt."),
    content("Las 4 partes de un buen prompt",
        "Un prompt solido casi siempre tiene estos cuatro ingredientes:\n\n"
        "1. Rol o contexto\n• Quien debe 'ser' Claude y para quien escribe\n\n"
        "2. Tarea explicita\n• Que quieres exactamente, en un verbo claro\n\n"
        "3. Contexto y datos\n• El material sobre el que trabaja\n\n"
        "4. Formato de salida\n• Como quieres la respuesta\n\n"
        "No siempre necesitas los cuatro, pero cuantos mas incluyas, mejor el resultado."),
    content("Ingrediente 1: el rol",
        "Decirle a Claude QUIEN debe ser orienta todo: vocabulario, profundidad y enfoque.\n\n"
        "• 'Eres un editor experto en textos legales'\n• 'Eres un profesor de primaria paciente'\n• 'Eres un revisor de codigo senior'\n\n"
        "El mismo encargo cambia por completo segun el rol. Es la forma mas rapida de subir la calidad sin escribir mucho mas."),
    content("Ingrediente 2: la tarea",
        "La tarea es el verbo: que quieres que HAGA, sin ambiguedad.\n\n"
        "Verbos claros: resume, reescribe, clasifica, compara, traduce, genera, corrige.\n\n"
        "❌ 'Mira esto' (no es una tarea)\n✅ 'Resume esto en 3 puntos'\n\n"
        "Una tarea principal por prompt. Si necesitas varias, encadenalas en mensajes separados."),
    content("Ingrediente 3: el contexto",
        "El contexto es todo lo que Claude necesita saber pero no puede adivinar:\n\n"
        "• El material a procesar (texto, datos)\n• La audiencia ('para directivos sin perfil tecnico')\n• El objetivo real detras de la tarea\n• Las restricciones ('sin tecnicismos', 'tono formal')\n\n"
        "Regla mental: si un humano nuevo no podria hacer la tarea solo con tu texto, a Claude tambien le falta informacion."),
    content("Ingrediente 4: el formato",
        "Si no dices COMO quieres la respuesta, recibes texto libre dificil de reutilizar.\n\n"
        "Especifica el entregable:\n• 'Lista de 5 vinetas, una frase cada una'\n• 'Tabla con columnas X, Y, Z'\n• 'JSON con estas claves'\n• 'Maximo 100 palabras'\n\n"
        "El formato convierte una respuesta en algo listo para usar."),
    content("Por que funciona la estructura",
        "Claude no adivina tu intencion: responde a lo que escribes.\n\n"
        "• Prompt vago -> respuesta vaga\n• Prompt estructurado -> resultado util y repetible\n\n"
        "Cada parte que anades es una decision que Claude YA no tiene que adivinar. Y menos adivinanza significa resultados mas cercanos a lo que tenias en la cabeza."),
    content("De lo generico a lo especifico",
        "Comparacion directa:\n\n"
        "Generico\n• 'Escribeme algo sobre productividad'\n• Resultado: texto plano, impredecible\n\n"
        "Especifico\n• 'Escribe 5 consejos de productividad para trabajadores remotos con hijos, tono empatico, una frase cada uno'\n• Resultado: util y listo para usar\n\n"
        "Mismo tema, mundos de diferencia."),
    content("Trucos que elevan cualquier prompt",
        "• Pon las instrucciones al principio y el material despues\n"
        "• Usa delimitadores (comillas triples, ###, etiquetas) para separar el texto a procesar\n"
        "• Pide un solo entregable por prompt\n"
        "• Si la tarea es compleja, pide que piense paso a paso (M4)\n"
        "• Da un ejemplo del resultado ideal cuando puedas\n\n"
        "Pequenos habitos que, juntos, marcan una gran diferencia."),
    example("Plantilla reutilizable (los 4 ingredientes)",
        "Rol: Eres un asistente de marketing B2B.\n\n"
        "Tarea: Escribe 3 asuntos de email para una campana de reactivacion.\n\n"
        "Contexto:\n- Producto: software de facturacion para pymes\n- Audiencia: clientes inactivos hace 90 dias\n- Tono: cercano, sin sonar desesperado\n\n"
        "Formato: lista numerada, max 8 palabras cada asunto."),
    example("El mismo prompt, version pobre vs pro",
        "# Pobre\nHazme un email de ventas.\n\n"
        "# Pro\nRol: vendedor consultivo, no agresivo.\n"
        "Tarea: escribe un email de primer contacto.\n"
        "Contexto: vendo software de agendas a clinicas dentales;\n"
        "el destinatario es el gerente; no me conoce.\n"
        "Formato: max 90 palabras, con asunto, una sola llamada a la accion."),
    quiz("Detecta el ingrediente que falta",
        "'Reescribe este parrafo para que sea mas claro.' Que le falta para ser excelente?",
        [("Esta perfecto asi", False, "Le falta contexto: para quien, que tono, que longitud."),
         ("El formato/tono y la audiencia", True, "Correcto: definir audiencia y formato hace la salida util y predecible."),
         ("Decir que use IA", False, "Eso es irrelevante; el modelo ya es la IA.")]),
    quiz("Cual es el rol en este prompt?",
        "'Eres un chef. Crea un menu de 3 platos.' Que parte es 'Eres un chef'?",
        [("La tarea", False, "La tarea es 'crea un menu'."),
         ("El rol", True, "Correcto: define quien debe ser Claude."),
         ("El formato", False, "El formato seria como presentar el menu.")]),
    challenge("Reto: cuenta los ingredientes",
        "Cuantos de los 4 ingredientes tiene: 'Eres un nutricionista. Crea un menu semanal vegetariano de 1800 kcal en formato tabla'?",
        "4", "Rol (nutricionista), tarea (crear menu), contexto (vegetariano, 1800 kcal) y formato (tabla)."),
    matching("Conecta concepto y definicion",
        [("Rol", "Quien debe ser Claude"),
         ("Tarea", "El verbo de lo que pides"),
         ("Contexto", "Datos y restricciones"),
         ("Formato", "Como quieres la respuesta"),
         ("Delimitadores", "Separan instruccion de material")]),
    content("Resumen de la leccion",
        "• Un buen prompt = rol + tarea + contexto + formato\n"
        "• El rol orienta, la tarea concreta, el contexto informa, el formato hace util\n"
        "• Especifico siempre gana a generico\n"
        "• Antes de enviar: que doy por sentado que Claude no sabe?\n\n"
        "En la siguiente leccion profundizamos en el ingrediente que mas mueve la aguja: el contexto."),
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
    content("Contexto explicito vs implicito",
        "Hay contexto que tu tienes en la cabeza (implicito) y que Claude no puede ver. Tu trabajo es hacerlo explicito.\n\n"
        "Implicito (en tu cabeza): 'es para mi jefe, que odia los rodeos'.\nExplicito (en el prompt): 'el lector es un directivo que valora la brevedad'.\n\n"
        "Cada vez que algo es 'obvio para ti', preguntate si esta escrito. Si no lo esta, Claude no lo sabe."),
    content("La escalera de la especificidad",
        "Sube peldanos hasta que la respuesta no tenga escapatoria:\n\n"
        "1. 'Escribe un resumen' (vago)\n"
        "2. 'Resume en 5 puntos' (mejor)\n"
        "3. 'Resume en 5 puntos para un directivo' (audiencia)\n"
        "4. '...destacando riesgos y decisiones' (foco)\n\n"
        "Cada peldano elimina interpretaciones posibles y te acerca a lo que querias."),
    content("Demasiado contexto tambien estorba",
        "Ojo: especificidad no es escribir un testamento.\n\n"
        "• Incluye lo que cambia la respuesta\n• Quita el relleno que no aporta\n• Un dato irrelevante puede despistar tanto como la falta de datos\n\n"
        "El objetivo es contexto UTIL, no contexto largo. Calidad sobre cantidad."),
    example("Mismo encargo, 3 niveles de contexto",
        "Nivel 1: Traduce esto.\n\n"
        "Nivel 2: Traduce esto al ingles.\n\n"
        "Nivel 3: Traduce esto al ingles britanico, tono formal,\n"
        "es para un email a un cliente corporativo. Manten los\n"
        "nombres propios sin traducir.\n\n"
        "El nivel 3 casi no deja margen de error."),
    quiz("Que tipo de contexto falta mas a menudo?",
        "Cual es el contexto que la gente olvida con mas frecuencia?",
        [("La audiencia y el objetivo real", True, "Correcto: para quien y para que es lo que mas cambia la respuesta."),
         ("El color de fondo", False, "Irrelevante para un texto."),
         ("La marca del ordenador", False, "No influye en la tarea.")]),
    content("Resumen de la leccion",
        "• El contexto es lo que mas mueve la calidad de la respuesta\n"
        "• Haz explicito lo que para ti es obvio\n"
        "• Sube la escalera de especificidad hasta cerrar interpretaciones\n"
        "• Pero incluye solo contexto util, no relleno\n\n"
        "Lo veras todo junto en la siguiente leccion con ejemplos antes/despues."),
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
    content("Caso 4: Generar ideas",
        "ANTES\n• 'Dame ideas de marketing'\n\n"
        "DESPUES\n• 'Dame 10 ideas de marketing de bajo presupuesto para una cafeteria local que quiere atraer publico joven entre semana. Una linea cada una.'\n\n"
        "Definir presupuesto, negocio, publico y momento convierte ideas genericas en ideas accionables."),
    content("Caso 5: Aprender un tema",
        "ANTES\n• 'Explicame las hipotecas'\n\n"
        "DESPUES\n• 'Explicame como funciona una hipoteca a alguien que compra su primera casa, sin jerga financiera, con un ejemplo numerico simple.'\n\n"
        "La audiencia ('primera casa', 'sin jerga') y el ejemplo cambian totalmente la utilidad."),
    content("El patron comun de todos los casos",
        "Fijate que en cada 'despues' anadimos lo mismo:\n\n"
        "• Para QUIEN es (audiencia)\n• Con que FOCO (que destacar)\n• En que FORMATO (longitud, estructura)\n• Con que TONO\n\n"
        "Memoriza ese patron: audiencia + foco + formato + tono. Es tu receta para mejorar casi cualquier prompt."),
    example("Plantilla universal antes/despues",
        "Objetivo: <que quieres lograr>\n"
        "Audiencia: <para quien>\n"
        "Material: <<<\n  pega aqui el texto/datos\n>>>\n"
        "Foco: <que destacar>\n"
        "Formato: <longitud y estructura del resultado>"),
    quiz("Cual es el patron para mejorar un prompt?",
        "Que conjunto de elementos eleva casi cualquier prompt?",
        [("Audiencia + foco + formato + tono", True, "Correcto: ese es el patron que repetimos en todos los casos."),
         ("Mas palabras y cortesia", False, "El relleno no mejora el resultado."),
         ("Pedir que sea creativo", False, "Demasiado vago; no orienta.")]),
    content("Resumen de la leccion",
        "• Comparar antes/despues es la forma mas rapida de aprender\n"
        "• El salto de calidad viene de anadir audiencia, foco, formato y tono\n"
        "• Reutiliza la plantilla universal en tu dia a dia\n\n"
        "Ya sabes que hacer bien. En la ultima leccion del modulo vemos que NO hacer: los errores comunes."),
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
    content("Error 6: no iterar",
        "El mayor error invisible: pedir una vez, conformarte y cerrar.\n\n"
        "Los mejores resultados casi nunca salen al primer intento. Claude esta disenado para iterar:\n• 'Mas corto'\n• 'Cambia el tono'\n• 'Desarrolla el punto 2'\n\n"
        "Trata el primer resultado como un borrador, no como la respuesta final."),
    content("Error 7: pelearse en vez de reformular",
        "Si tras 2-3 intentos no mejora, no insistas con lo mismo: reformula desde cero.\n\n"
        "• Cambia el enfoque del prompt\n• Anade un ejemplo del resultado ideal\n• Divide la tarea en partes\n\n"
        "A veces, empezar un chat nuevo y limpio resuelve lo que mil correcciones no lograban."),
    content("La checklist anti-errores",
        "Antes de dar por bueno un prompt, repasa:\n\n"
        "✅ Una sola tarea principal\n"
        "✅ Contexto y material incluidos\n"
        "✅ Audiencia y formato definidos\n"
        "✅ Datos criticos a verificar identificados\n"
        "✅ Plan B si el resultado no convence (iterar/reformular)\n\n"
        "Cinco comprobaciones que evitan el 90% de los problemas."),
    quiz("Que hacer si el resultado no convence tras varios intentos?",
        "Llevas 3 correcciones y no mejora. Que es lo mas sensato?",
        [("Repetir la misma correccion mas fuerte", False, "Insistir igual no suele cambiar nada."),
         ("Reformular desde cero o empezar un chat limpio", True, "Correcto: cambiar el enfoque suele desbloquear."),
         ("Rendirse y hacerlo a mano", False, "Antes de eso, reformular casi siempre funciona.")]),
    content("Resumen del modulo 3",
        "Ya dominas el arte del prompt:\n• La anatomia (rol, tarea, contexto, formato)\n• El poder del contexto y la especificidad\n• Casos reales antes/despues\n• Los errores a evitar y como iterar\n\n"
        "En el modulo 4 subimos de nivel con tecnicas avanzadas: razonamiento, few-shot, etiquetas y roles."),
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
    content("Por que funciona el razonamiento explicito",
        "Cuando Claude escribe su razonamiento, cada paso se apoya en el anterior.\n\n"
        "• Reduce saltos logicos erroneos\n• Hace visibles los supuestos\n• Permite que se corrija a si mismo a mitad de camino\n\n"
        "Es la diferencia entre soltar un numero y mostrar el desarrollo de un problema de mates: con desarrollo, hay menos errores."),
    content("Formas de activar CoT",
        "Frases que disparan el razonamiento paso a paso:\n\n"
        "• 'Piensa paso a paso antes de responder'\n• 'Muestra tu razonamiento y luego la conclusion'\n• 'Desglosa el problema en partes'\n• 'Antes de decidir, lista pros y contras'\n\n"
        "Todas comparten lo mismo: piden el proceso, no solo el resultado."),
    content("CoT en decisiones del mundo real",
        "No es solo para mates. Aplicalo a:\n\n"
        "• Elegir entre proveedores: 'puntua cada uno por precio, calidad y plazo, luego recomienda'\n• Diagnosticar un problema: 'lista causas posibles y descartalas una a una'\n• Planificar: 'desglosa el objetivo en pasos ordenados'\n\n"
        "Ver el razonamiento te deja auditar la decision, no solo aceptarla."),
    example("CoT estructurado para una decision",
        "Tengo que elegir CRM para mi pyme. Antes de recomendar:\n"
        "1. Lista mis 4 criterios (precio, facilidad, soporte, integraciones)\n"
        "2. Puntua cada opcion del 1 al 5 en cada criterio\n"
        "3. Suma y explica el ganador\n"
        "Opciones: A, B y C. Razona paso a paso."),
    quiz("Que pide realmente el chain-of-thought?",
        "Cual es la esencia de la tecnica?",
        [("Pedir el proceso de razonamiento, no solo el resultado", True, "Correcto: el valor esta en hacer explicito el razonamiento."),
         ("Pedir respuestas mas largas porque si", False, "No se trata de longitud, sino de razonar."),
         ("Repetir la pregunta varias veces", False, "Eso no es CoT.")]),
    content("Resumen de la leccion",
        "• CoT = pedir que razone paso a paso antes de concluir\n"
        "• Reduce errores en logica, calculos y decisiones\n"
        "• Sirve tanto para mates como para elegir y planificar\n"
        "• Evitalo en tareas triviales: solo anade longitud\n\n"
        "Siguiente tecnica: ensenar con ejemplos (few-shot)."),
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
    content("Few-shot para fijar un estilo",
        "No solo sirve para clasificar: tambien para clonar un tono o formato.\n\n"
        "Dale 2-3 ejemplos de tu estilo de escritura y pide que continue igual.\n\n"
        "• Titulares de tu marca\n• El formato de tus fichas de producto\n• El tono de tus respuestas de soporte\n\n"
        "Es la forma mas rapida de que suene a TI sin describir tu estilo con palabras."),
    content("La consistencia del formato es clave",
        "El error mas comun en few-shot: ejemplos con formatos distintos.\n\n"
        "Si un ejemplo usa '-> POSITIVO' y otro 'Resultado: positivo', Claude no sabe cual imitar.\n\n"
        "Regla: todos los ejemplos identicos en estructura. La separacion input/output siempre igual. La consistencia es lo que ensena el patron."),
    content("Cuando few-shot no es necesario",
        "No metas ejemplos por inercia:\n\n"
        "• Si una instruccion clara basta -> no hacen falta\n• Si la tarea es simple -> ahorras tokens sin ellos\n• Si el formato es obvio -> con describirlo vale\n\n"
        "Usa few-shot cuando mostrar es mas facil que explicar, o cuando el formato es complejo."),
    example("Few-shot para clonar tono de marca",
        "Escribe descripciones de producto en NUESTRO estilo:\n\n"
        "Producto: taza termica -> 'Tu cafe, caliente hasta la ultima gota. Sin dramas.'\n"
        "Producto: mochila -> 'Todo lo tuyo, a la espalda y sin peso de mas.'\n\n"
        "Producto: botella de agua ->"),
    quiz("Cual es el error mas comun en few-shot?",
        "Que estropea mas un prompt con ejemplos?",
        [("Que los ejemplos tengan formatos distintos entre si", True, "Correcto: sin consistencia, Claude no sabe que patron imitar."),
         ("Usar exactamente 3 ejemplos", False, "2-3 es justo lo recomendado."),
         ("Separar input y output", False, "Eso es buena practica, no un error.")]),
    content("Resumen de la leccion",
        "• Few-shot = ensenar con ejemplos de entrada/salida\n"
        "• 2-3 ejemplos consistentes suelen bastar\n"
        "• Sirve para clasificar, extraer y clonar estilo/tono\n"
        "• La consistencia del formato es lo que ensena el patron\n\n"
        "Siguiente: estructurar prompts complejos con etiquetas."),
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
    content("Etiquetas mas utiles en la practica",
        "No necesitas memorizar muchas. Con estas vas sobrado:\n\n"
        "• <instrucciones> ... </instrucciones>\n• <contexto> ... </contexto>\n• <documento> ... </documento>\n• <ejemplos> ... </ejemplos>\n• <formato> ... </formato>\n\n"
        "Elige nombres claros en tu idioma; lo importante es que separen partes distintas."),
    content("El problema que resuelven de verdad",
        "Cuando pegas texto largo sin etiquetas, Claude puede confundir tus DATOS con tus INSTRUCCIONES.\n\n"
        "Ej: pegas un email que dice 'ignora lo anterior' y sin etiquetas Claude podria obedecerlo.\n\n"
        "Con <documento>...</documento>, queda claro: 'esto es material a procesar, no ordenes para ti'. Es tambien una proteccion basica."),
    content("Salida etiquetada para automatizar",
        "Pedir la respuesta dentro de etiquetas facilita procesarla con codigo:\n\n"
        "'Devuelve el resultado dentro de <json>...</json> y nada fuera.'\n\n"
        "Luego tu programa extrae lo que hay entre <json> y </json>. Imprescindible cuando conectas Claude a una app (lo veras en M8)."),
    example("Prompt completo bien etiquetado",
        "<rol>Eres analista de soporte.</rol>\n"
        "<instrucciones>Clasifica el ticket por urgencia.</instrucciones>\n"
        "<reglas>alta=produccion caida; media=un usuario; baja=cosmetico</reglas>\n"
        "<documento>\n  ...texto del ticket...\n</documento>\n"
        "<formato>Devuelve solo: <urgencia>VALOR</urgencia></formato>"),
    quiz("Por que protegen las etiquetas?",
        "Que riesgo reducen al envolver el material en <documento>?",
        [("Que Claude confunda tus datos con instrucciones", True, "Correcto: separan claramente material de ordenes."),
         ("Que la respuesta sea mas larga", False, "No afectan la longitud."),
         ("Que el modelo vaya mas rapido", False, "No cambian la velocidad.")]),
    content("Resumen de la leccion",
        "• Las etiquetas XML separan instruccion, datos, ejemplos y formato\n"
        "• Evitan que Claude confunda material con ordenes\n"
        "• La salida etiquetada facilita automatizar con codigo\n"
        "• Pocas etiquetas claras bastan para prompts profesionales\n\n"
        "Ultima tecnica del modulo: roles, personas y restricciones."),
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
    content("Un rol no es solo una profesion",
        "Puedes dar roles muy especificos para afinar el resultado:\n\n"
        "• 'Eres un editor esceptico que busca agujeros en el argumento'\n• 'Eres un nino de 8 anos curioso' (para simplificar)\n• 'Eres un traductor que prioriza el sentido sobre la literalidad'\n\n"
        "Cuanto mas concreto el rol, mas se ajusta la respuesta a lo que buscas."),
    content("Restricciones positivas y negativas",
        "Define tanto lo que SI como lo que NO:\n\n"
        "Positivas (haz):\n• 'Responde en max 3 frases'\n• 'Usa ejemplos cotidianos'\n\n"
        "Negativas (no hagas):\n• 'No uses jerga tecnica'\n• 'No inventes datos; si no sabes, dilo'\n\n"
        "Las restricciones negativas suelen ser las que mas mejoran el control."),
    content("Roles para obtener varias perspectivas",
        "Truco potente: pide a Claude que adopte varios roles para un mismo tema.\n\n"
        "'Analiza esta idea de negocio desde 3 roles: un inversor cauto, un cliente ideal y un competidor.'\n\n"
        "Obtienes una vision 360 que un solo punto de vista no da. Ideal para decisiones y revisiones."),
    example("System prompt completo (rol + persona + restricciones)",
        "Eres 'Aria', asistente de una clinica dental.\n"
        "- Persona: calmada, cercana, tranquilizadora.\n"
        "- Haz: responde dudas de citas y cuidados basicos.\n"
        "- No hagas: nunca des diagnosticos; deriva al dentista.\n"
        "- Formato: max 4 frases, en espanol, sin tecnicismos."),
    quiz("Cual restriccion da mas control?",
        "Cual de estas acota mejor el comportamiento?",
        [("'Hazlo bien'", False, "Es vago; no acota nada."),
         ("'No des diagnosticos; deriva al profesional'", True, "Correcto: una restriccion negativa clara y segura."),
         ("'Se util'", False, "Demasiado generico para controlar.")]),
    content("Resumen del modulo 4",
        "Ya manejas las tecnicas avanzadas:\n• Chain-of-thought para razonar paso a paso\n• Few-shot para ensenar con ejemplos\n• Etiquetas XML para estructurar\n• Roles, personas y restricciones para controlar\n\n"
        "Con esto escribes prompts de nivel profesional. En el modulo 5 pasamos a las capacidades y herramientas de Claude."),
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
    content("Tipos de Artifact que puedes pedir",
        "Claude crea Artifacts de muchas clases:\n\n"
        "• Documentos y textos largos\n• Codigo (Python, JS, etc.)\n• Paginas y componentes web (HTML)\n• Tablas y planes estructurados\n• Diagramas y visualizaciones\n\n"
        "Si es algo que querras copiar, descargar o seguir editando, probablemente sera un Artifact."),
    content("Iterar: la verdadera ventaja",
        "Lo potente no es crear, es REFINAR sobre lo mismo.\n\n"
        "• 'Acorta la introduccion'\n• 'Cambia el titulo por algo mas directo'\n• 'Anade una seccion de riesgos'\n\n"
        "Claude edita el mismo Artifact en vez de empezar de cero. Es como trabajar con un companero que reescribe el documento contigo, no que te manda uno nuevo cada vez."),
    content("Artifacts + tu flujo de trabajo",
        "Un Artifact terminado lo puedes:\n\n"
        "• Copiar a tu editor o documento\n• Descargar como archivo\n• Pegar en tu web o herramienta\n\n"
        "Piensa en el chat como el taller y el Artifact como la pieza que sale lista para llevar."),
    example("Crear e iterar un Artifact",
        "1) 'Crea una propuesta de proyecto de 1 pagina con objetivo,\n"
        "   alcance, plazos y presupuesto. Deja importes como [PENDIENTE].'\n\n"
        "2) 'Anade una seccion de riesgos con 3 vinetas.'\n\n"
        "3) 'Hazlo mas formal y acorta el alcance a 2 frases.'\n\n"
        "Cada paso edita el MISMO documento."),
    quiz("Cual es la mayor ventaja de los Artifacts?",
        "Que los hace especialmente utiles?",
        [("Iterar sobre la misma pieza sin reescribir todo", True, "Correcto: refinas el mismo entregable paso a paso."),
         ("Que cambian de color solos", False, "No es una ventaja real ni el punto."),
         ("Que borran el chat", False, "No tienen que ver con borrar nada.")]),
    content("Resumen de la leccion",
        "• Los Artifacts son entregables editables en panel aparte\n"
        "• Sirven para documentos, codigo, webs, tablas y mas\n"
        "• Su poder real es iterar sin reescribir\n"
        "• Listos para copiar o descargar a tu flujo\n\n"
        "Siguiente capacidad: dar a Claude acceso a informacion actual con la busqueda web."),
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
    content("Senales de que necesitas busqueda",
        "Activa busqueda cuando tu pregunta incluya pistas de actualidad:\n\n"
        "• 'Ahora', 'hoy', 'ultimo', 'reciente', 'actual'\n• Precios, disponibilidad, horarios\n• Quien ocupa un cargo, resultados, noticias\n\n"
        "Si la respuesta correcta pudo cambiar desde el ano pasado, casi seguro necesitas datos frescos."),
    content("Investigacion multi-fuente",
        "Para temas amplios, pide a Claude que vaya mas alla de un solo resultado:\n\n"
        "• 'Consulta varias fuentes y dime en que coinciden y en que no'\n• 'Resume el estado actual del tema citando cada dato'\n• 'Senala si hay opiniones encontradas'\n\n"
        "Contrastar fuentes da una vision mas fiable que fiarte de la primera pagina."),
    content("La verificacion sigue siendo tuya",
        "La busqueda reduce errores, pero no los elimina:\n\n"
        "• Pide siempre los enlaces/fuentes\n• Contrasta cifras importantes en la fuente original\n• Desconfia si todo viene de un solo sitio\n\n"
        "Tu criterio es el filtro final. Claude busca y resume; tu decides que es fiable."),
    example("Pedir investigacion con fuentes",
        "Investiga las opciones actuales de [TEMA].\n"
        "- Consulta al menos 3 fuentes distintas.\n"
        "- Resume en una tabla: opcion, ventaja, inconveniente.\n"
        "- Cita el enlace de cada dato.\n"
        "- Marca con (?) cualquier dato que no puedas confirmar."),
    quiz("Cuando NO necesitas busqueda web?",
        "En cual caso aporta poco?",
        [("Precio de un vuelo manana", False, "Cambia constantemente: necesita datos actuales."),
         ("Explicar que es la fotosintesis", True, "Correcto: conocimiento estable, no requiere busqueda."),
         ("Quien gano el partido de ayer", False, "Evento reciente: necesita busqueda.")]),
    content("Resumen de la leccion",
        "• La busqueda web da acceso a informacion actual\n"
        "• Usala para datos que cambian; no para conocimiento estable\n"
        "• Para temas amplios, contrasta varias fuentes\n"
        "• Pide enlaces y verifica lo critico tu mismo\n\n"
        "Siguiente: convertir respuestas en archivos listos para usar."),
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
    content("Del dato suelto al entregable",
        "El verdadero valor: pegas informacion en bruto y recibes algo presentable.\n\n"
        "• Notas desordenadas -> documento estructurado\n• Numeros pegados -> Excel con tabla y totales\n• Puntos sueltos -> presentacion de diapositivas\n\n"
        "Tu aportas la materia prima; Claude la convierte en el formato final."),
    content("Detalles que mejoran el archivo",
        "Cuando pidas un archivo, especifica:\n\n"
        "• La estructura (columnas, secciones, pestanas)\n• Datos de ejemplo si quieres verlo relleno\n• Reglas: 'que los totales cuadren con formula'\n• Que dejar como [PENDIENTE] para completar tu\n\n"
        "Cuanto mas claro el molde, menos retoques despues."),
    content("Revisa antes de usar",
        "Un archivo generado es un borrador muy avanzado, no un producto final infalible:\n\n"
        "• Verifica numeros y formulas criticas\n• Comprueba que el formato abre bien en tu programa\n• Ajusta lo que no encaje con tu caso\n\n"
        "Te ahorra el 90% del trabajo; el 10% de revision sigue siendo tuyo."),
    example("Pedir un Excel util",
        "Crea una hoja de calculo (.xlsx) de presupuesto mensual.\n"
        "Columnas: categoria, presupuesto, gasto real, diferencia.\n"
        "- Filas de ejemplo para 5 categorias.\n"
        "- Fila de totales con formula de suma.\n"
        "- Una pestana 'resumen' con el total por categoria."),
    quiz("Que formato pedir para datos tabulares?",
        "Necesitas analizar numeros en columnas y filas. Que encaja mejor?",
        [(".pptx", False, "Es para presentaciones, no para analizar datos."),
         (".xlsx o .csv", True, "Correcto: formatos de hoja de calculo para datos tabulares."),
         (".txt", False, "Texto plano no estructura tablas con formulas.")]),
    content("Resumen de la leccion",
        "• Claude genera documentos, hojas, presentaciones, PDF y codigo\n"
        "• Indica formato y estructura exactos\n"
        "• Convierte datos en bruto en entregables presentables\n"
        "• Revisa numeros y formato antes de usarlo\n\n"
        "Siguiente: como funciona la memoria de Claude entre conversaciones."),
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
    content("Dos tipos de memoria",
        "Conviene distinguir:\n\n"
        "Memoria del hilo (siempre)\n• Todo lo dicho en la conversacion actual, hasta el limite del contexto\n\n"
        "Memoria entre hilos (segun funcion)\n• Recordar chats anteriores requiere funciones de memoria o proyectos\n\n"
        "Por defecto, cada conversacion nueva arranca limpia: no asumas que recuerda lo de ayer."),
    content("Cuando el hilo se hace muy largo",
        "Si una conversacion crece mucho, lo mas antiguo puede salir del context window.\n\n"
        "Senales: Claude 'olvida' algo que dijiste al principio.\n\n"
        "Soluciones:\n• Resume tu mismo los puntos clave y pegalos\n• Empieza un hilo nuevo con un resumen de contexto\n• Manten los hilos enfocados en un tema"),
    content("Proyectos: memoria reutilizable",
        "Para continuidad real, usa proyectos:\n\n"
        "• Guardan instrucciones y documentos que se aplican a todos sus chats\n• No tienes que repetir el contexto cada vez\n• Ideal para trabajo recurrente (un cliente, un tema)\n\n"
        "Es la forma practica de que Claude 'recuerde' tu contexto de forma estable."),
    example("Dar continuidad con un resumen",
        "Si retomas un tema en un chat nuevo, empieza asi:\n\n"
        "'Contexto de lo que llevamos: estoy escribiendo un curso de\n"
        "Claude. Ya definimos 9 modulos. Ahora quiero pulir el modulo 5.\n"
        "Con eso en mente, ayudame a...'\n\n"
        "Un parrafo de contexto reconstruye la continuidad."),
    quiz("Que pasa al abrir una conversacion nueva por defecto?",
        "Sin funciones de memoria, como arranca?",
        [("Recuerda todos tus chats anteriores", False, "No por defecto; arranca limpia."),
         ("Empieza sin memoria del hilo anterior salvo que des contexto", True, "Correcto: hay que aportar contexto o usar proyectos/memoria."),
         ("Borra tus archivos", False, "Abrir un chat no borra nada.")]),
    content("Resumen del modulo 5",
        "Ya conoces las capacidades y herramientas:\n• Artifacts para entregables editables\n• Busqueda web para datos actuales\n• Creacion de archivos\n• Como funciona la memoria y el contexto\n\n"
        "En el modulo 6 lo aplicamos a casos de uso practicos del dia a dia."),
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
    content("El flujo de escritura asistida",
        "Una forma fiable de escribir con Claude:\n\n"
        "1. Borrador: 'escribe una primera version de...'\n"
        "2. Critica: 'que mejorarias de este texto?'\n"
        "3. Ajuste: 'aplica esos cambios y acorta un 20%'\n"
        "4. Pulido: 'revisa tono y gramatica'\n\n"
        "Trabajar por capas da mejores resultados que esperar el texto perfecto al primer intento."),
    content("Romper el bloqueo de la pagina en blanco",
        "El mayor regalo de Claude al escribir: nunca empiezas de cero.\n\n"
        "• 'Dame 3 formas distintas de abrir este articulo'\n• 'Hazme un esquema y lo relleno yo'\n• 'Escribe un borrador feo, ya lo pulo'\n\n"
        "Es mas facil mejorar algo que existe que crear de la nada. Usa Claude para tener siempre con que empezar."),
    content("Tu voz, no la de la maquina",
        "Para que suene a ti y no generico:\n\n"
        "• Dale ejemplos de tu estilo (few-shot, recuerda M4)\n• Especifica tu tono: 'cercano, con humor seco'\n• Edita el resultado: la ultima palabra es tuya\n\n"
        "Claude es el borrador y el espejo; la voz la pones tu."),
    example("Adaptar un mensaje a 3 canales",
        "Toma este anuncio y adaptalo a 3 versiones:\n\n"
        "1. Email formal a clientes (max 100 palabras)\n"
        "2. Post de Instagram (con gancho y emojis)\n"
        "3. Mensaje breve de WhatsApp (2 frases)\n\n"
        "Mensaje base: 'Lanzamos envio gratis en pedidos +30€'."),
    quiz("Como evitar que el texto suene generico?",
        "Que ayuda mas a que suene a ti?",
        [("Dar ejemplos de tu estilo y editar el resultado", True, "Correcto: ejemplos + tu edicion fijan tu voz."),
         ("Pedir que sea 'profesional' sin mas", False, "Demasiado vago para capturar tu voz."),
         ("Usar siempre el modelo mas caro", False, "El modelo no define tu estilo.")]),
    content("Resumen de la leccion",
        "• Escribe por capas: borrador, critica, ajuste, pulido\n"
        "• Usa Claude para vencer la pagina en blanco\n"
        "• Mantén tu voz con ejemplos y edicion final\n"
        "• Adapta el mismo mensaje a cada canal\n\n"
        "Siguiente caso de uso: programacion y analisis tecnico."),
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
    content("No hace falta ser programador",
        "Aunque no programes, Claude te ayuda con lo tecnico:\n\n"
        "• Escribir formulas de Excel/Sheets\n• Automatizar tareas repetitivas con pequenos scripts\n• Entender un error que te aparecio\n• Explicarte que hace un trozo de codigo\n\n"
        "Es como tener un programador paciente al lado que ademas te explica."),
    content("Escribir tests para validar",
        "Una practica de oro: pedir tests junto al codigo.\n\n"
        "'Dame la funcion y ademas 3 pruebas que confirmen que funciona, incluido un caso limite.'\n\n"
        "Los tests son tu red de seguridad: demuestran que el codigo hace lo que dice, en vez de fiarte a ciegas."),
    content("Refactor y mejora",
        "Claude no solo arregla, tambien mejora codigo existente:\n\n"
        "• 'Hazlo mas legible'\n• 'Separa esta funcion en partes mas pequenas'\n• 'Hay riesgos de seguridad aqui?'\n• 'Optimiza esta parte lenta'\n\n"
        "Pega tu codigo y pide la mejora concreta que necesitas."),
    example("Pedir codigo con red de seguridad",
        "Lenguaje: Python 3.11\n"
        "Tarea: funcion que valide si un email tiene formato correcto.\n"
        "Requisitos:\n- Comentarios explicando la logica\n"
        "- Manejo de entrada vacia\n- 3 tests: uno valido, uno invalido, uno vacio"),
    quiz("Por que pedir tests junto al codigo?",
        "Cual es la razon principal?",
        [("Para confirmar que el codigo hace lo que dice", True, "Correcto: los tests validan el comportamiento."),
         ("Para que el codigo sea mas largo", False, "No se trata de longitud."),
         ("Para gastar mas tokens", False, "El objetivo es seguridad, no gasto.")]),
    content("Resumen de la leccion",
        "• Claude ayuda en todo el ciclo: escribir, depurar, explicar, mejorar\n"
        "• Da contexto: lenguaje, entrada/salida, error real\n"
        "• Pide tests como red de seguridad\n"
        "• Revisa siempre antes de ejecutar y no pegues secretos\n\n"
        "Siguiente: analisis de datos y documentos."),
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
    content("Preguntas que puedes hacerle a un documento",
        "Pega un informe, contrato o PDF y pregunta como a un experto:\n\n"
        "• 'Cual es la idea principal en una frase?'\n• 'Que riesgos o clausulas raras tiene?'\n• 'Que decisiones quedan pendientes?'\n• 'Resumelo para alguien con 2 minutos'\n\n"
        "Conviertes 50 paginas en las respuestas que de verdad necesitas."),
    content("Comparar varios documentos",
        "Claude puede cruzar informacion de varias fuentes:\n\n"
        "• 'Compara estas 3 propuestas en una tabla'\n• 'Que dice cada contrato sobre el plazo de pago?'\n• 'En que se contradicen estos dos informes?'\n\n"
        "Ideal para decisiones donde tienes que sopesar opciones."),
    content("Cuidado con documentos enormes y cifras",
        "Dos limites a recordar:\n\n"
        "• Si el documento supera el context window, divide o resume por partes\n• Verifica los calculos y cifras criticas: el analisis ayuda, pero la responsabilidad del numero final es tuya\n\n"
        "Y para datos sensibles, anonimiza antes de pegar (lo veras en M7)."),
    example("Extraccion estructurada a JSON",
        "Del siguiente texto, extrae en JSON con las claves\n"
        "{cliente, fecha, importe, estado}. Si un dato falta, pon null.\n\n"
        "Texto: <<<\n  ...factura o email...\n>>>\n\n"
        "Devuelve SOLO el JSON, sin explicaciones."),
    quiz("Mejor formato para procesar la salida con una app?",
        "Quieres que un programa use el resultado. Que pides?",
        [("Un parrafo en prosa", False, "Dificil de parsear automaticamente."),
         ("JSON con claves definidas", True, "Correcto: estructurado y facil de procesar."),
         ("Un resumen libre", False, "Poco fiable para automatizar.")]),
    content("Resumen de la leccion",
        "• Claude resume, extrae, compara y analiza documentos y datos\n"
        "• Preguntale como a un experto: idea principal, riesgos, decisiones\n"
        "• Para apps, pide salida en JSON estructurado\n"
        "• Divide documentos enormes y verifica cifras criticas\n\n"
        "Ultimo caso del modulo: creatividad e ideas."),
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
    content("Cantidad primero, calidad despues",
        "El error creativo numero uno: pedir 'la idea perfecta'.\n\n"
        "Mejor flujo:\n• Genera muchas (20-30) sin filtrar\n• Marca las 3-5 que te resuenan\n• Pide desarrollar o combinar solo esas\n\n"
        "La creatividad es un juego de volumen: necesitas materia prima antes de pulir."),
    content("Combinar y cruzar ideas",
        "Las mejores ideas suelen salir de mezclar:\n\n"
        "• 'Combina la idea 2 y la 7'\n• 'Y si lo llevamos al extremo opuesto?'\n• 'Dame una version segura y una atrevida'\n\n"
        "Usa Claude como un companero de pizarra que nunca se cansa de proponer variantes."),
    content("Construir historias por capas",
        "Para narrativa, no pidas todo de golpe:\n\n"
        "1. Premisa y personaje\n2. Estructura (esqueleto de escenas)\n3. Desarrollo escena a escena\n4. Pulido de tono y dialogos\n\n"
        "Construir por capas da historias mas solidas que un volcado unico."),
    example("Brief creativo enfocado",
        "Necesito nombres para una cafeteria de especialidad.\n"
        "Tono: calido, moderno, facil de recordar.\n"
        "Evita: palabras en ingles y juegos de palabras obvios.\n"
        "Dame 15 opciones con una linea de justificacion cada una.\n"
        "Luego desarrollamos las 3 mejores."),
    quiz("Como conseguir mejores ideas?",
        "Que estrategia funciona mejor en lluvia de ideas?",
        [("Pedir 'una buena idea'", False, "Limita el rango; mejor generar muchas."),
         ("Generar muchas con restricciones y luego filtrar", True, "Correcto: volumen + foco, despues seleccionas."),
         ("No dar ningun contexto", False, "Sin foco, salen ideas genericas.")]),
    content("Resumen del modulo 6",
        "Ya aplicas Claude a casos reales:\n• Escritura y comunicacion\n• Programacion y analisis tecnico\n• Analisis de datos y documentos\n• Creatividad e ideas\n\n"
        "En el modulo 7 vemos lo que sostiene todo esto: buenas practicas y limites."),
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
    content("La regla de oro: 'lo veria en una postal?'",
        "Un test mental rapido antes de pegar algo:\n\n"
        "Si no escribirias ese dato en una postal que cualquiera puede leer, piensalo dos veces antes de pegarlo.\n\n"
        "No es paranoia: es higiene digital. Aplica sobre todo a datos de otras personas, no solo tuyos."),
    content("Anonimizar sin perder utilidad",
        "Casi siempre puedes hacer la tarea SIN los datos sensibles:\n\n"
        "• Nombres -> [CLIENTE], [EMPLEADO_1]\n• Numeros de cuenta/DNI -> [REDACTADO]\n• Importes exactos -> [IMPORTE] si no son necesarios\n\n"
        "Claude analiza la estructura igual de bien con marcadores. Recuperas los datos reales tu, al final."),
    content("En cuentas de empresa",
        "Si usas Claude en el trabajo:\n\n"
        "• Conoce la politica de IA de tu organizacion\n• Respeta acuerdos de confidencialidad (NDA)\n• Ante la duda, pregunta antes de pegar informacion de clientes\n\n"
        "La privacidad no es solo tuya: tambien proteges a las personas y empresas con las que trabajas."),
    example("Anonimizar antes de pegar",
        "ANTES:\nRevisa el contrato de Juan Perez (DNI 12345678) por 50.000€.\n\n"
        "DESPUES:\nRevisa el contrato de [CLIENTE] (DNI [REDACTADO]) por [IMPORTE].\n"
        "Identifica clausulas de riesgo y plazos de pago."),
    quiz("Cual es la mejor practica de privacidad?",
        "Necesitas que Claude revise un contrato con datos personales. Que haces?",
        [("Pegarlo tal cual con todos los datos", False, "Expones datos sensibles sin necesidad."),
         ("Anonimizar los datos personales antes de pegarlo", True, "Correcto: la tarea sale igual de bien y proteges la informacion."),
         ("No usar Claude nunca para contratos", False, "Puedes usarlo perfectamente si anonimizas.")]),
    content("Resumen de la leccion",
        "• Comparte solo lo imprescindible (minimizacion)\n"
        "• Anonimiza datos personales; la tarea sale igual\n"
        "• Nunca pegues credenciales\n"
        "• Respeta la politica de tu organizacion\n\n"
        "Siguiente: verificacion y pensamiento critico."),
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
    content("El mapa de cuando verificar",
        "No todo necesita la misma desconfianza:\n\n"
        "Confia e itera (bajo riesgo):\n• Ideas, borradores, brainstorming, estilo\n\n"
        "Verifica siempre (alto riesgo):\n• Cifras, fechas, citas, leyes, nombres, datos medicos o legales\n\n"
        "Ajusta tu nivel de verificacion al coste de equivocarte."),
    content("Tecnicas para reducir errores",
        "• Pide nivel de confianza: 'marca alto/medio/bajo en cada dato'\n• Pide fuentes y compruebalas\n• Activa busqueda web para datos actuales\n• Pide razonamiento paso a paso (recuerda M4)\n• Cruza el dato con una fuente fiable\n\n"
        "Combinadas, bajan muchisimo el riesgo de tragar un error."),
    content("El humano en el bucle",
        "Para decisiones importantes (salud, dinero, legal), trata la respuesta como un borrador a revisar, NO como un veredicto.\n\n"
        "El mejor flujo: Claude acelera (rapidez) + tu verificas (criterio).\n\n"
        "La IA no te quita la responsabilidad de la decision final; te da una primera version mucho mas rapida."),
    example("Prompt que invita a la honestidad",
        "Responde solo si estas seguro. Si no lo sabes o no puedes\n"
        "verificarlo, dilo en vez de inventar.\n\n"
        "Para cada dato relevante, indica tu nivel de confianza\n"
        "(alto/medio/bajo) y, si es posible, la fuente."),
    quiz("Que es una alucinacion en IA?",
        "Como se describe mejor?",
        [("Un error de conexion", False, "No es un fallo tecnico de red."),
         ("Una respuesta que suena segura pero es falsa", True, "Correcto: el modelo afirma con confianza algo incorrecto."),
         ("Cuando el modelo se apaga", False, "No tiene que ver con apagarse.")]),
    content("Resumen de la leccion",
        "• Claude puede equivocarse con tono seguro: verifica lo critico\n"
        "• Confia para ideas; verifica para datos comprobables\n"
        "• Pide fuentes, confianza y razonamiento\n"
        "• Manten un humano en el bucle para decisiones importantes\n\n"
        "Siguiente: las limitaciones que conviene conocer."),
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
    content("Limite: no tiene intencion ni memoria propia",
        "Claude no 'quiere' nada ni recuerda quien eres entre sesiones (salvo funciones de memoria).\n\n"
        "• No guarda rencor ni preferencias por su cuenta\n• No aprende de tu chat para el siguiente usuario\n• Cada conversacion parte de su entrenamiento, no de 'experiencias'\n\n"
        "Esto es bueno para la privacidad, pero significa que el contexto lo aportas tu cada vez."),
    content("Limite: matematica y conteo exactos",
        "Como genera por probabilidad, puede fallar en aritmetica precisa o al contar elementos.\n\n"
        "• Para calculos criticos, pidele que razone paso a paso\n• O mejor: que use codigo/herramientas para calcular\n\n"
        "No asumas que un numero esta bien solo porque lo escribio con seguridad."),
    content("Convertir limites en metodo",
        "Cada limite tiene su contramedida:\n\n"
        "• No sabe lo reciente -> busqueda web\n• No conoce tus datos -> pegaselos\n• Puede alucinar -> verifica\n• Falla en calculo -> paso a paso o codigo\n• No recuerda -> proyectos o resumen\n\n"
        "Un usuario avanzado no es el que ignora los limites, sino el que los rodea con metodo."),
    example("Rodear el limite de calculo",
        "En vez de: 'cuanto es el total de esta lista de 50 numeros?'\n\n"
        "Mejor: 'escribe y ejecuta codigo Python que sume esta lista\n"
        "y muestre el total. Lista: [ ... ]'\n\n"
        "Asi el numero lo calcula codigo, no la prediccion."),
    quiz("Como manejar un calculo critico?",
        "Necesitas un total exacto de muchos numeros. Que es mas fiable?",
        [("Pedir el resultado directo y confiar", False, "Puede fallar en aritmetica precisa."),
         ("Pedir que lo calcule con codigo o paso a paso", True, "Correcto: reduces el error de calculo."),
         ("Asumir que siempre acierta", False, "El tono seguro no garantiza exactitud.")]),
    content("Resumen de la leccion",
        "• Claude tiene fecha de corte y no accede a tu mundo sin herramientas\n"
        "• Puede fallar en calculo y varia entre respuestas\n"
        "• No tiene intencion ni memoria propia entre sesiones\n"
        "• Cada limite se rodea con una contramedida concreta\n\n"
        "Ultima leccion del modulo: uso responsable y etico."),
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
    content("Propiedad intelectual y citas",
        "Respeta el trabajo ajeno:\n\n"
        "• No publiques como tuyo texto que no revisaste ni adaptaste\n• No atribuyas a personas reales frases inventadas\n• Cita fuentes cuando uses datos o ideas de otros\n\n"
        "La IA facilita generar; tu responsabilidad es publicar de forma honesta."),
    content("Sesgos: revisa lo sensible",
        "Los modelos pueden reflejar sesgos de sus datos de entrenamiento.\n\n"
        "Ten especial cuidado en decisiones sobre personas:\n• Contratacion, evaluaciones, prestamos\n• Cualquier juicio que afecte a alguien\n\n"
        "Pide varias perspectivas y no delegues estas decisiones sin supervision humana."),
    content("Transparencia con tu audiencia",
        "Segun el contexto, conviene indicar cuando un contenido fue asistido por IA.\n\n"
        "• En trabajo academico o periodistico, suele ser obligado\n• Con clientes, genera confianza ser honesto\n\n"
        "La transparencia no resta valor a tu trabajo: lo hace mas creible."),
    example("Pedir una revision de sesgos",
        "Revisa este anuncio de empleo y senala cualquier lenguaje\n"
        "que pueda excluir o sesgar a algun grupo (genero, edad,\n"
        "origen). Sugiere alternativas neutras.\n\n"
        "Texto: <<< ...oferta de empleo... >>>"),
    quiz("Quien es responsable del contenido generado?",
        "Publicas algo hecho con Claude y tiene un error grave. Quien responde?",
        [("Claude", False, "La herramienta no asume tu responsabilidad."),
         ("Tu, que lo revisas y publicas", True, "Correcto: la responsabilidad final del uso es tuya."),
         ("Nadie", False, "Siempre responde quien publica.")]),
    content("Resumen del modulo 7",
        "Ya usas Claude con criterio:\n• Privacidad y datos sensibles\n• Verificacion y pensamiento critico\n• Limitaciones y como rodearlas\n• Uso responsable y etico\n\n"
        "En el modulo 8 damos el salto al siguiente nivel: Claude Code, MCP y un proyecto final."),
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
    content("Chat vs Claude Code",
        "La diferencia clave:\n\n"
        "Chat (Claude.ai)\n• Conversas, copias y pegas codigo manualmente\n\n"
        "Claude Code (terminal)\n• Lee y edita tus archivos directamente\n• Ejecuta comandos y tests\n• Trabaja en varios pasos hacia un objetivo\n\n"
        "Es pasar de 'pedir consejo' a 'delegar la tarea'."),
    content("El flujo tipico",
        "1. Le das una tarea en lenguaje natural\n"
        "2. Explora tu proyecto y propone un plan\n"
        "3. Hace cambios (que ves como diffs)\n"
        "4. Ejecuta tests para comprobar\n"
        "5. Tu revisas y apruebas\n\n"
        "En todo momento mantienes el control: nada se da por bueno sin tu visto bueno."),
    content("Por que git es tu mejor aliado",
        "Trabajar con control de versiones (git) hace que Claude Code sea seguro:\n\n"
        "• Ves exactamente que cambio (diffs)\n• Puedes revertir si algo no te gusta\n• Cada paso queda registrado\n\n"
        "Con git, experimentar no da miedo: siempre puedes volver atras."),
    example("Tareas tipicas en Claude Code",
        "'Anade validacion de email al registro y un test.'\n"
        "'Encuentra por que falla el test de pagos y arreglalo.'\n"
        "'Refactoriza utils.js para separar la logica de red.'\n"
        "'Explica como fluye la autenticacion en este repo.'"),
    quiz("Que distingue a Claude Code del chat?",
        "Cual es la diferencia esencial?",
        [("Es mas barato", False, "No es la diferencia esencial."),
         ("Lee/edita archivos y ejecuta comandos en tu proyecto", True, "Correcto: actua agenticamente sobre tu codigo real."),
         ("Solo responde teoria", False, "Hace mucho mas: actua sobre el codigo.")]),
    content("Resumen de la leccion",
        "• Claude Code lleva a Claude a tu terminal y tu codigo\n"
        "• Lee, edita, ejecuta y testea de forma agentica\n"
        "• Tu revisas los diffs y apruebas\n"
        "• Trabaja con git para experimentar sin riesgo\n\n"
        "Siguiente: conectar Claude con tus herramientas via MCP."),
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
    content("De conversar a actuar",
        "Sin conectores, Claude solo puede hablar. Con MCP, puede HACER:\n\n"
        "• Leer tus datos reales (no solo lo que pegas)\n• Crear registros, eventos, tareas\n• Buscar en tus sistemas\n• Encadenar acciones entre apps\n\n"
        "Es el salto de 'asistente que aconseja' a 'asistente que ejecuta'."),
    content("Conectores listos y a medida",
        "Hay dos caminos:\n\n"
        "• Conectores ya hechos para apps populares (calendario, CRM, almacenamiento, chat...)\n• Conectores propios que tu o tu equipo construyen para sistemas internos\n\n"
        "Al ser un estandar abierto, MCP evita reinventar cada integracion desde cero."),
    content("Permisos: el punto critico",
        "Cuando Claude puede ACTUAR, el control de accesos es esencial:\n\n"
        "• Concede solo los permisos necesarios\n• Revisa que acciones puede ejecutar\n• Exige confirmacion antes de algo sensible (enviar, borrar, pagar)\n\n"
        "Dar 'manos' a un asistente es potente, pero pide responsabilidad."),
    example("Lo que habilita un conector",
        "Calendario: 'Que tengo manana? Bloquea 1h para preparar la reunion.'\n"
        "CRM: 'Crea un contacto para el lead que escribio hoy.'\n"
        "Base de datos: 'Cuantos pedidos hubo la semana pasada?'\n"
        "Documentos: 'Busca el contrato de [CLIENTE] y resumelo.'"),
    quiz("Que es MCP?",
        "Cual definicion encaja mejor?",
        [("Un modelo de Claude mas grande", False, "No es un modelo, es un protocolo."),
         ("Un estandar para conectar Claude con herramientas y datos", True, "Correcto: Model Context Protocol conecta Claude con el exterior."),
         ("Un lenguaje de programacion", False, "No es un lenguaje; es un protocolo.")]),
    content("Resumen de la leccion",
        "• MCP conecta Claude con herramientas y datos externos\n"
        "• Convierte a Claude de 'conversar' a 'actuar'\n"
        "• Hay conectores listos y puedes crear los tuyos\n"
        "• Los permisos y la confirmacion en acciones sensibles son clave\n\n"
        "Siguiente: recursos para seguir aprendiendo."),
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
    content("Construye tu biblioteca de prompts",
        "Tu recurso mas valioso eres tu mismo, organizado:\n\n"
        "• Guarda los prompts que te funcionaron\n• Conviertelos en plantillas reutilizables\n• Anota que modelo y ajustes usaste\n\n"
        "Con el tiempo tendras un arsenal propio que vale mas que cualquier curso: esta hecho a la medida de tu trabajo."),
    content("Aprende en comunidad",
        "No aprendas en solitario:\n\n"
        "• Comparte prompts con tu equipo o comunidad\n• Mira como otros resuelven problemas parecidos\n• Comenta que funciona y que no\n\n"
        "Ver el enfoque de otros acelera tu propio aprendizaje y te da ideas que no se te habrian ocurrido."),
    content("Mantente al dia sin agobio",
        "La IA cambia rapido, pero no necesitas seguirlo todo:\n\n"
        "• Revisa novedades cada cierto tiempo, no a diario\n• Prueba lo nuevo en una tarea pequena antes de adoptarlo\n• Re-evalua tus flujos cuando salgan mejoras relevantes\n\n"
        "Mejor un habito sostenible que el agobio de querer saberlo todo."),
    example("Ficha para guardar un buen prompt",
        "Nombre: Resumen ejecutivo de informes\n"
        "Prompt: 'Resume en 5 puntos para direccion, destacando\n"
        "riesgos y decisiones. Texto: <<< >>>'\n"
        "Modelo: Sonnet\n"
        "Notas: funciona mejor si pego el indice del informe primero."),
    quiz("Cual es tu recurso mas valioso a largo plazo?",
        "Que te hara mejorar de forma sostenida?",
        [("Una biblioteca propia de prompts y plantillas", True, "Correcto: a medida de tu trabajo y reutilizable."),
         ("Memorizar datos que cambian", False, "Envejecen rapido; mejor un metodo."),
         ("Usar siempre el modelo mas caro", False, "El modelo no sustituye al metodo.")]),
    content("Resumen de la leccion",
        "• Empieza por la documentacion oficial ante dudas\n"
        "• Construye tu biblioteca de prompts y plantillas\n"
        "• Aprende en comunidad y practica con problemas reales\n"
        "• Mantente al dia con un habito sostenible\n\n"
        "Ya casi cierras el modulo: solo falta el proyecto final."),
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
    content("Elige un problema que te duela",
        "El mejor proyecto resuelve una molestia real tuya:\n\n"
        "• Algo que haces a mano cada semana\n• Una tarea que odias por repetitiva\n• Un cuello de botella en tu trabajo\n\n"
        "Si resuelve un dolor real, lo usaras de verdad y veras el valor de inmediato."),
    content("Aplica todo lo aprendido",
        "Tu proyecto deberia usar varias piezas del curso:\n\n"
        "• Buen prompt (rol, tarea, contexto, formato) — M3\n• Tecnica avanzada si aplica (CoT, few-shot) — M4\n• Una herramienta (Artifacts, busqueda, archivos) — M5\n• Verificacion de lo critico — M7\n\n"
        "Integrar varias piezas es lo que convierte el aprendizaje en habilidad."),
    content("Mide si funciona",
        "Define un criterio de exito ANTES de empezar:\n\n"
        "• 'Me ahorra 2 horas a la semana'\n• 'El borrador sale listo en un 80%'\n• 'Reduce errores en X'\n\n"
        "Sin criterio no sabras si funciono. Con criterio, puedes mejorarlo iteracion a iteracion."),
    example("Plantilla de brief del proyecto",
        "Objetivo: <que problema resuelvo>\n"
        "Entregable: <que produzco exactamente>\n"
        "Contexto/datos: <que necesita Claude>\n"
        "Tecnicas: <few-shot, CoT, etiquetas, herramientas>\n"
        "Criterio de exito: <como se que quedo bien>"),
    quiz("Que NO debe faltar antes de dar por bueno el proyecto?",
        "Cual paso es imprescindible?",
        [("Verificar el resultado", True, "Correcto: la verificacion es clave antes de usar/publicar."),
         ("Hacerlo en ingles", False, "El idioma depende de tu caso."),
         ("Usar el modelo mas caro", False, "Elige el adecuado, no el mas caro.")]),
    content("Resumen del modulo 8",
        "Diste el salto al siguiente nivel:\n• Claude Code para desarrolladores\n• Integraciones y conectores MCP\n• Recursos para seguir aprendiendo\n• Tu proyecto final\n\n"
        "Si quieres ir aun mas lejos, el modulo 9 BONUS abre la caja de herramientas avanzada."),
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
    content("Como funciona, en simple",
        "Constitutional AI, paso a paso:\n\n"
        "1. Se define un conjunto de principios (la 'constitucion')\n"
        "2. El modelo genera una respuesta\n"
        "3. Se critica a si mismo segun esos principios\n"
        "4. Reescribe la respuesta mejorada\n\n"
        "En vez de depender solo de etiquetas humanas, el modelo aprende a autoevaluarse con esos principios."),
    content("Util, honesto, inofensivo",
        "Los tres valores guia, con ejemplos de lo que provocan:\n\n"
        "🤝 Util: se esfuerza en resolver tu tarea de verdad\n"
        "📝 Honesto: reconoce lo que no sabe, no inventa para complacer\n"
        "🛡️ Inofensivo: evita causar dano real\n\n"
        "El reto del diseno es equilibrarlos: ser util sin dejar de ser seguro, y honesto sin ser inutilmente rigido."),
    content("Por que importa para ti",
        "Esta filosofia explica comportamientos que notaras:\n\n"
        "• Razona los matices en temas delicados en vez de bloquear\n• Te dice cuando no esta seguro\n• Intenta ayudar de verdad, no solo cumplir\n\n"
        "Saberlo te ayuda a pedir mejor: si quieres mas honestidad sobre incertidumbre, pidela explicitamente."),
    example("Ver la honestidad calibrada en accion",
        "Compara estos dos prompts y observa la diferencia:\n\n"
        "1. 'Dame el dato exacto de X' (puede arriesgar)\n\n"
        "2. 'Dame el dato de X. Si no estas seguro, dimelo y\n"
        "   explica que harias para verificarlo.' (invita a la honestidad)"),
    quiz("Que es Constitutional AI?",
        "Cual descripcion encaja mejor?",
        [("Un modelo que se autoevalua con un conjunto de principios", True, "Correcto: aprende a aplicar una 'constitucion' de principios."),
         ("Una ley de internet", False, "No es legislacion; es un metodo de entrenamiento."),
         ("Un tipo de hardware", False, "No tiene que ver con hardware.")]),
    content("Resumen de la leccion",
        "• Claude se disena para ser util, honesto e inofensivo\n"
        "• Constitutional AI le ensena a autoevaluarse con principios\n"
        "• Esto explica el matiz y la honestidad que notaras\n"
        "• Puedes potenciar esa honestidad pidiendola explicitamente\n\n"
        "Siguiente: Markdown como input estructurado."),
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
    content("Markdown en 60 segundos",
        "Los simbolos esenciales:\n\n"
        "# Titulo (un # = nivel 1, ## = nivel 2)\n"
        "- elemento de lista\n"
        "1. lista numerada\n"
        "**negrita** y *cursiva*\n"
        "`codigo en linea`\n"
        "> cita\n\n"
        "Con esto cubres el 95% de lo que necesitas para estructurar un prompt."),
    content("Por que Claude lo entiende tan bien",
        "Claude se entreno con muchisimo texto en Markdown (documentacion, README, foros tecnicos).\n\n"
        "Por eso 'piensa' de forma natural en titulos, listas y bloques. Darle Markdown es como hablarle en un idioma que domina a la perfeccion: capta la jerarquia sin esfuerzo."),
    content("Pedir salida en Markdown",
        "Tambien puedes pedir que la RESPUESTA venga en Markdown:\n\n"
        "• Tablas listas para pegar\n• Titulos y listas claras\n• Bloques de codigo bien formateados\n\n"
        "Ideal para documentacion, notas, README y cualquier cosa que vayas a pegar en otra herramienta que entienda Markdown."),
    example("Prompt estructurado en Markdown",
        "# Tarea\nClasifica los tickets por prioridad.\n\n"
        "## Reglas\n- Critico: afecta a produccion\n- Alto: afecta a un usuario\n- Bajo: cosmetico\n\n"
        "## Datos\n```\n...tickets...\n```\n\n"
        "## Formato\nTabla con columnas: ticket, prioridad, motivo."),
    quiz("Para que sirve Markdown en un prompt?",
        "Cual es su ventaja principal?",
        [("Hacer el texto bonito y nada mas", False, "No es solo estetica: aporta estructura."),
         ("Estructurar la informacion para que Claude la entienda mejor", True, "Correcto: titulos, listas y bloques dan jerarquia clara."),
         ("Cifrar el contenido", False, "No tiene que ver con cifrado.")]),
    content("Resumen de la leccion",
        "• Markdown estructura tus prompts con titulos, listas y bloques\n"
        "• Claude lo entiende de forma natural por su entrenamiento\n"
        "• Puedes pedir la salida tambien en Markdown\n"
        "• Pocos simbolos bastan para un gran salto de claridad\n\n"
        "Siguiente: las Skills de Claude."),
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
    content("La analogia del manual experto",
        "Imagina que contratas a alguien muy capaz y, para una tarea concreta, le das el manual perfecto de tu empresa.\n\n"
        "Eso es una Skill: un paquete de conocimiento y plantillas que Claude 'abre' justo cuando la tarea lo pide, para hacerla de forma experta y consistente."),
    content("Que contiene una Skill",
        "Una Skill puede empaquetar:\n\n"
        "• Instrucciones de como hacer bien la tarea\n• Plantillas y formatos\n• A veces, codigo de apoyo\n\n"
        "Todo junto y reutilizable, para que no tengas que explicar el 'como' cada vez."),
    content("Skills en accion",
        "Ejemplos de lo que habilitan:\n\n"
        "• Crear documentos Word con buen formato (.docx)\n• Generar hojas de calculo (.xlsx)\n• Construir presentaciones (.pptx)\n• Producir PDFs o flujos especializados\n\n"
        "Pides 'hazme un .docx con este informe' y la Skill correspondiente se encarga del formato."),
    example("Disparar una Skill sin esfuerzo",
        "No necesitas 'invocarla' tecnicamente; basta pedir la tarea:\n\n"
        "'Convierte este texto en una presentacion de 6 diapositivas\n"
        "con titulo, 4 puntos clave y un cierre.'\n\n"
        "Claude reconoce que encaja una Skill de presentaciones y la usa."),
    quiz("Que es una Skill?",
        "Cual definicion encaja mejor?",
        [("Una capacidad empaquetada que Claude carga para una tarea", True, "Correcto: instrucciones/plantillas/codigo para hacer bien algo concreto."),
         ("Un modelo distinto de Claude", False, "No es un modelo; es una capacidad que se activa."),
         ("Un tipo de suscripcion", False, "No es un plan de pago.")]),
    content("Resumen de la leccion",
        "• Las Skills son capacidades empaquetadas que Claude carga al vuelo\n"
        "• Aportan conocimiento experto y plantillas para una tarea\n"
        "• Se activan cuando tu peticion encaja, sin pasos tecnicos\n"
        "• Se combinan con herramientas (MCP) y generacion de archivos\n\n"
        "Siguiente: como construir un agente."),
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
    content("Agente vs respuesta normal",
        "La diferencia esencial:\n\n"
        "Respuesta normal\n• Le preguntas, te contesta, fin\n\n"
        "Agente\n• Le das un objetivo y trabaja solo: planifica, actua, observa y ajusta hasta cumplirlo\n\n"
        "Un agente no responde una vez: persigue una meta a lo largo de varios pasos."),
    content("Las 'manos' del agente: herramientas",
        "Un agente necesita herramientas para actuar sobre el mundo:\n\n"
        "• Buscar en la web\n• Leer y escribir archivos\n• Consultar una base de datos\n• Llamar a una API\n\n"
        "Sin herramientas, solo piensa; con ellas, hace. Por eso MCP (la leccion siguiente) es tan importante para los agentes."),
    content("El factor seguridad",
        "Cuanto mas autonomo es un agente, mas importan los limites:\n\n"
        "• Permisos minimos: solo lo que necesita\n• Confirmacion humana en acciones sensibles\n• Criterio de parada para que no corra sin fin\n• Registro de lo que hace\n\n"
        "Autonomia sin control es un riesgo; autonomia con limites es una herramienta potente."),
    example("Anatomia de un agente simple",
        "Objetivo: vigilar menciones de mi marca y resumirlas.\n"
        "Herramientas: busqueda web (leer), documento (escribir).\n"
        "Bucle: buscar -> filtrar -> resumir -> guardar.\n"
        "Parada: cuando entrega el resumen del dia.\n"
        "Limite: solo crea borrador; no publica nada."),
    quiz("Que define a un agente?",
        "Cual es la caracteristica clave?",
        [("Da una sola respuesta y termina", False, "Eso es una respuesta normal."),
         ("Planifica y ejecuta varios pasos con herramientas hacia un objetivo", True, "Correcto: actua en bucle de forma autonoma."),
         ("Es un modelo mas pequeno", False, "No es cuestion de tamano.")]),
    content("Resumen de la leccion",
        "• Un agente persigue un objetivo en varios pasos, de forma autonoma\n"
        "• El bucle: planear, actuar, observar, decidir, repetir\n"
        "• Las herramientas son sus 'manos' para actuar\n"
        "• Limites, permisos y parada lo hacen seguro\n\n"
        "Siguiente: MCP en profundidad, el protocolo que da herramientas a los agentes."),
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
    content("La analogia del puerto USB",
        "Antes del USB, cada dispositivo tenia su propio conector: un caos.\n\n"
        "MCP es el 'USB' de la IA: un estandar unico para que cualquier herramienta se conecte a Claude.\n\n"
        "Resultado: una herramienta que habla MCP funciona con cualquier cliente que lo soporte. Se construye una vez y sirve para todos."),
    content("Herramientas vs recursos",
        "Dos cosas que expone un servidor MCP:\n\n"
        "🔧 Herramientas (acciones)\n• 'crear_tarea', 'enviar_email', 'buscar'\n• Hacen algo, cambian el mundo\n\n"
        "📚 Recursos (datos)\n• Un documento, una tabla, un registro\n• Se leen, no actuan\n\n"
        "Las herramientas son verbos; los recursos, sustantivos."),
    content("Seguridad cuando hay 'manos'",
        "Dar acciones a un agente exige control serio:\n\n"
        "• Expon solo las herramientas necesarias\n• Permisos minimos por herramienta\n• Confirmacion en lo sensible (enviar, borrar, pagar)\n• Registro (log) de cada ejecucion\n\n"
        "El estandar facilita la conexion; la seguridad la pones con buen diseno de permisos."),
    example("Idea de un servidor MCP minimo",
        "// Pseudocodigo conceptual\n"
        "servidor.herramienta('crear_tarea', (titulo, fecha) => {\n"
        "  // crea la tarea en tu sistema\n"
        "  return { ok: true };\n"
        "});\n"
        "// Claude descubre 'crear_tarea' y la usa cuando hace falta"),
    quiz("Que expone un servidor MCP?",
        "Que dos cosas principales ofrece?",
        [("Herramientas (acciones) y recursos (datos)", True, "Correcto: acciones que ejecutar y datos que leer."),
         ("Solo imagenes", False, "No se limita a imagenes."),
         ("Modelos de IA nuevos", False, "Sirve herramientas y datos, no modelos.")]),
    content("Resumen de la leccion",
        "• MCP es el estandar 'USB' que conecta Claude con el exterior\n"
        "• Expone herramientas (acciones) y recursos (datos)\n"
        "• Es lo que da 'manos' a los agentes\n"
        "• La seguridad se basa en permisos minimos y confirmacion\n\n"
        "Ultima leccion del curso: construye tu primer agente."),
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
    content("Empieza pequeno de verdad",
        "El error tipico del primer agente: querer que haga demasiado.\n\n"
        "Mejor un agente que haga UNA cosa bien:\n• Resumir tus emails sin leer\n• Vigilar un tema y avisarte\n• Convertir notas en tareas\n\n"
        "Cuando funcione, lo amplias. Un agente pequeno que funciona vale mas que uno ambicioso que falla."),
    content("Disena el bucle y la parada",
        "Define con claridad:\n\n"
        "• Bucle: que pasos repite (planear -> actuar -> observar)\n• Parada: cuando termina (objetivo cumplido o limite de pasos)\n• Controles: donde te pide confirmacion\n\n"
        "Un agente sin criterio de parada es como un grifo sin cierre: hay que ponerselo desde el diseno."),
    content("Mantente en el bucle (tu)",
        "En tu primer agente, supervisa de cerca:\n\n"
        "• Que solo cree borradores, no publique ni envie\n• Revisa lo que hace antes de darle mas permisos\n• Sube la autonomia poco a poco, segun confies\n\n"
        "La confianza en un agente se gana paso a paso, igual que con una persona nueva en el equipo."),
    example("Brief de tu primer agente",
        "Objetivo: resumir novedades del sector y entregar un informe.\n"
        "Herramientas: busqueda web (leer), generador de documentos (escribir).\n"
        "Limites: no publicar nada; solo crear un borrador.\n"
        "Parada: cuando entrega el .docx con 5 fuentes citadas.\n"
        "Control humano: yo reviso antes de compartir."),
    quiz("Como empezar tu primer agente?",
        "Que tipo de objetivo conviene para el primero?",
        [("Algo enorme y abierto", False, "Dificil de controlar y evaluar."),
         ("Algo acotado y repetitivo", True, "Correcto: facil de definir, medir y supervisar."),
         ("Algo sin objetivo claro", False, "Sin objetivo no hay criterio de exito.")]),
    content("Lo lograste: fin del curso",
        "Recorriste los 9 modulos:\n• Fundamentos y modelos\n• Interfaz y organizacion\n• El arte del prompt y tecnicas avanzadas\n• Capacidades, casos de uso y buenas practicas\n• Claude Code, MCP, Skills y agentes\n\n"
        "Ya no eres un usuario casual: entiendes como piensa Claude y como sacarle el maximo con criterio. Ahora, a practicar con tus propios proyectos."),
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
