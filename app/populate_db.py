import sys
import os
from pathlib import Path

# Añadir el directorio raíz del proyecto al path de Python
project_root = Path(__file__).parent.parent  # Sube dos niveles desde el archivo actual
sys.path.insert(0, str(project_root))

from app import create_app, db
from app.models import Question # type: ignore

# app = create_app()

def add_questions():
    
    app = create_app()
    # Preguntas de Lenguaje
    questions_lenguaje = [
        {
        "question_text": "Identifica el predicado en: 'La científica escribió un artículo revolucionario'",
        "option_a": "La científica",
        "option_b": "escribió un artículo revolucionario",
        "option_c": "un artículo",
        "option_d": "revolucionario",
        "feedback_a": "Incorrecto. Es el sujeto (quien realiza la acción).",
        "feedback_b": "Correcto. Describe la acción del sujeto (verbo + complementos).",
        "feedback_c": "Incorrecto. Es solo parte del predicado.",
        "feedback_d": "Incorrecto. Es un adjetivo que modifica al sustantivo.",
        "correct_answer": "b",
        "difficulty": 1
        },
        {
        "question_text": "¿Qué figura literaria aparece en 'El tiempo es oro'?",
        "option_a": "Hipérbole",
        "option_b": "Metáfora",
        "option_c": "Personificación",
        "option_d": "Anáfora",
        "feedback_a": "Incorrecto. No hay exageración.",
        "feedback_b": "Correcto. Compara tiempo y oro sin usar 'como'.",
        "feedback_c": "Incorrecto. No se atribuyen cualidades humanas.",
        "feedback_d": "Incorrecto. No hay repetición de palabras al inicio.",
        "correct_answer": "b",
        "difficulty": 2
        },
        {
        "question_text": "En 'Los estudiantes entregaron sus trabajos a la profesora', ¿qué función tiene 'a la profesora'?",
        "option_a": "Complemento directo",
        "option_b": "Complemento indirecto",
        "option_c": "Complemento circunstancial",
        "option_d": "Atributo",
        "feedback_a": "Incorrecto. El CD es 'sus trabajos' (qué entregaron).",
        "feedback_b": "Correcto. Indica el destinatario (a quién se entrega).",
        "feedback_c": "Incorrecto. No expresa tiempo, lugar o modo.",
        "feedback_d": "Incorrecto. Solo aparece con verbos copulativos (ser/estar).",
        "correct_answer": "b",
        "difficulty": 2
        },
        {
        "question_text": "¿En qué tiempo verbal está 'Habrían estudiado'?",
        "option_a": "Condicional simple",
        "option_b": "Condicional compuesto",
        "option_c": "Pluscuamperfecto",
        "option_d": "Futuro perfecto",
        "feedback_a": "Incorrecto. El condicional simple es 'estudiarían'.",
        "feedback_b": "Correcto. 'Habrían' (auxiliar) + participio ('estudiado').",
        "feedback_c": "Incorrecto. Usa 'había' + participio ('habían estudiado').",
        "feedback_d": "Incorrecto. Usa 'habrá' + participio ('habrá estudiado').",
        "correct_answer": "b",
        "difficulty": 3
        },
        {
        "question_text": "Si un texto dice 'El protagonista, a pesar de las advertencias, decidió adentrarse en el bosque', ¿qué rasgo del personaje se destaca?",
        "option_a": "Obstinación",
        "option_b": "Miedo",
        "option_c": "Generosidad",
        "option_d": "Ignorancia",
        "feedback_a": "Correcto. Insiste en su decisión contra advertencias.",
        "feedback_b": "Incorrecto. No hay evidencia de temor.",
        "feedback_c": "Incorrecto. No actúa para beneficiar a otros.",
        "feedback_d": "Incorrecto. No se sugiere que desconozca los riesgos.",
        "correct_answer": "a",
        "difficulty": 2
        },
        {
        "question_text": "¿Cuál palabra lleva tilde diacrítica?",
        "option_a": "Solo",
        "option_b": "Aun",
        "option_c": "Té",
        "option_d": "Dios",
        "feedback_a": "Incorrecto. 'Solo' ya no lleva tilde según RAE.",
        "feedback_b": "Incorrecto. 'Aun' solo la lleva en casos específicos ('aún').",
        "feedback_c": "Correcto. La tilde distingue el sustantivo ('té') del pronombre ('te').",
        "feedback_d": "Incorrecto. No cumple función diacrítica.",
        "correct_answer": "c",
        "difficulty": 1
        },
        {
        "question_text": "¿Qué obra es un ejemplo de narrativa épica?",
        "option_a": "La Odisea",
        "option_b": "Romeo y Julieta",
        "option_c": "Veinte poemas de amor",
        "option_d": "La casa de Bernarda Alba",
        "feedback_a": "Correcto. Narra hazañas heroicas (género épico).",
        "feedback_b": "Incorrecto. Es drama teatral.",
        "feedback_c": "Incorrecto. Pertenece a la lírica.",
        "feedback_d": "Incorrecto. Es teatro dramático.",
        "correct_answer": "a",
        "difficulty": 2
        },
        {
        "question_text": "¿Qué opción es sinónimo de 'lúgubre'?",
        "option_a": "Alegre",
        "option_b": "Tenebroso",
        "option_c": "Rápido",
        "option_d": "Pequeño",
        "feedback_a": "Incorrecto. Antónimo de 'lúgubre'.",
        "feedback_b": "Correcto. Ambos implican oscuridad o tristeza.",
        "feedback_c": "Incorrecto. No relacionado con el tempo.",
        "feedback_d": "Incorrecto. No refiere a tamaño.",
        "correct_answer": "b",
        "difficulty": 1
        },
        {
        "question_text": "En 'Volverán las oscuras golondrinas', ¿qué representa las golondrinas?",
        "option_a": "La primavera",
        "option_b": "La memoria",
        "option_c": "La libertad",
        "option_d": "La muerte",
        "feedback_a": "Incorrecto. Aunque vuelven en primavera, el poema habla de pérdida.",
        "feedback_b": "Correcto. Simbolizan recuerdos que persisten (Bécquer).",
        "feedback_c": "Incorrecto. No es el tema central del poema.",
        "feedback_d": "Incorrecto. El tono es nostálgico, no fúnebre.",
        "correct_answer": "b",
        "difficulty": 3
        },
        {
        "question_text": "¿Qué conector usarías para contrastar ideas en: 'Quería ir al cine, ___ estaba lloviendo'?",
        "option_a": "porque",
        "option_b": "además",
        "option_c": "pero",
        "option_d": "es decir",
        "feedback_a": "Incorrecto. 'Porque' indica causa, no contraste.",
        "feedback_b": "Incorrecto. 'Además' añade información, no contrasta.",
        "feedback_c": "Correcto. 'Pero' introduce una idea opuesta.",
        "feedback_d": "Incorrecto. 'Es decir' explica, no contrasta.",
        "correct_answer": "c",
        "difficulty": 1
        }
        # Agrega más preguntas de lenguaje...
        ]

    # Preguntas de Matemáticas
    questions_matematicas = [
        {
        "question_text": "Si a = 5 y b = 3, ¿cuál es el valor de 2a + b²?",
        "option_a": "13",
        "option_b": "19",
        "option_c": "25",
        "option_d": "31",
        "feedback_a": "Incorrecto. Calculaste 2a + b en lugar de b².",
        "feedback_b": "Correcto. 2(5) + 3² = 10 + 9 = 19.",
        "feedback_c": "Incorrecto. Sumaste 5² + 3² en lugar de 2a + b².",
        "feedback_d": "Incorrecto. Multiplicaste todos los términos.",
        "correct_answer": "b",
        "difficulty": 1
        },
        {
        "question_text": "Resuelve: 3x - 7 = 14",
        "option_a": "x = 7",
        "option_b": "x = 9",
        "option_c": "x = 21",
        "option_d": "x = 5",
        "feedback_a": "Correcto. 3(7) - 7 = 21 - 7 = 14.",
        "feedback_b": "Incorrecto. 3(9) - 7 = 20 ≠ 14.",
        "feedback_c": "Incorrecto. No dividiste el resultado entre 3.",
        "feedback_d": "Incorrecto. 3(5) - 7 = 8 ≠ 14.",
        "correct_answer": "a",
        "difficulty": 1
        },
        {
        "question_text": "¿Cuál es el perímetro de un rectángulo con lados de 6 cm y 4 cm?",
        "option_a": "10 cm",
        "option_b": "20 cm",
        "option_c": "24 cm",
        "option_d": "28 cm",
        "feedback_a": "Incorrecto. Sumaste solo un lado de cada longitud (6 + 4).",
        "feedback_b": "Correcto. P = 2(6) + 2(4) = 12 + 8 = 20 cm.",
        "feedback_c": "Incorrecto. Calculaste el área (6 × 4).",
        "feedback_d": "Incorrecto. Sumaste todos los lados sin duplicar.",
        "correct_answer": "b",
        "difficulty": 1
        },
        {
        "question_text": "¿Cuál es el resultado de 3/4 + 1/2?",
        "option_a": "4/6",
        "option_b": "5/4",
        "option_c": "1 1/4",
        "option_d": "3/8",
        "feedback_a": "Incorrecto. Sumaste numeradores y denominadores directamente.",
        "feedback_b": "Correcto. 3/4 + 2/4 = 5/4.",
        "feedback_c": "Correcto (alternativa). 5/4 equivale a 1 1/4.",
        "feedback_d": "Incorrecto. Multiplicaste en lugar de sumar.",
        "correct_answer": "b",
        "difficulty": 2
        },
        {
        "question_text": "Resuelve el sistema: 2x + y = 8; x - y = 1",
        "option_a": "x=3, y=2",
        "option_b": "x=2, y=4",
        "option_c": "x=4, y=0",
        "option_d": "x=1, y=6",
        "feedback_a": "Correcto. 2(3) + 2 = 8 y 3 - 2 = 1.",
        "feedback_b": "Incorrecto. 2(2) + 4 = 8, pero 2 - 4 ≠ 1.",
        "feedback_c": "Incorrecto. 2(4) + 0 = 8, pero 4 - 0 ≠ 1.",
        "feedback_d": "Incorrecto. 2(1) + 6 = 8, pero 1 - 6 ≠ 1.",
        "correct_answer": "a",
        "difficulty": 2
        },
        {
        "question_text": "Si un producto cuesta $80 y tiene un descuento del 15%, ¿cuál es su precio final?",
        "option_a": "$12",
        "option_b": "$68",
        "option_c": "$65",
        "option_d": "$92",
        "feedback_a": "Incorrecto. Calculaste solo el descuento (15% de 80).",
        "feedback_b": "Correcto. 80 - (0.15 × 80) = 80 - 12 = 68.",
        "feedback_c": "Incorrecto. Restaste el 20% en lugar del 15%.",
        "feedback_d": "Incorrecto. Sumaste el 15% en lugar de restarlo.",
        "correct_answer": "b",
        "difficulty": 2
        },
        {
        "question_text": "En un triángulo rectángulo, si el cateto opuesto mide 3 y la hipotenusa 5, ¿cuál es sen(θ)?",
        "option_a": "3/5",
        "option_b": "4/5",
        "option_c": "3/4",
        "option_d": "5/3",
        "feedback_a": "Correcto. sen(θ) = opuesto/hipotenusa = 3/5.",
        "feedback_b": "Incorrecto. 4/5 sería el coseno si el cateto adyacente es 4.",
        "feedback_c": "Incorrecto. 3/4 es la tangente, no el seno.",
        "feedback_d": "Incorrecto. La hipotenusa no puede ser menor que el cateto.",
        "correct_answer": "a",
        "difficulty": 3
        },
        {
        "question_text": "Al lanzar un dado, ¿cuál es la probabilidad de obtener un número par?",
        "option_a": "1/6",
        "option_b": "1/2",
        "option_c": "1/3",
        "option_d": "2/3",
        "feedback_a": "Incorrecto. Es la probabilidad de un número específico.",
        "feedback_b": "Correcto. Pares: 2, 4, 6 → 3/6 = 1/2.",
        "feedback_c": "Incorrecto. Solo consideraste 2 números pares.",
        "feedback_d": "Incorrecto. Incluiste números impares.",
        "correct_answer": "b",
        "difficulty": 1
        },
        {
        "question_text": "¿Cuál es el vértice de la parábola y = x² - 4x + 3?",
        "option_a": "(2, -1)",
        "option_b": "(-2, 15)",
        "option_c": "(1, 0)",
        "option_d": "(4, 3)",
        "feedback_a": "Correcto. Vértice en x = -b/(2a) = 4/2 = 2; y(2) = -1.",
        "feedback_b": "Incorrecto. Usaste x = -b en lugar de -b/(2a).",
        "feedback_c": "Incorrecto. Es una raíz, no el vértice.",
        "feedback_d": "Incorrecto. Evaluaste en x=4, no en el vértice.",
        "correct_answer": "a",
        "difficulty": 3
        },
        {
        "question_text": "Si log₂(x) = 3, ¿cuál es el valor de x?",
        "option_a": "6",
        "option_b": "8",
        "option_c": "9",
        "option_d": "1.5",
        "feedback_a": "Incorrecto. Confundiste log₂(x) con 2x.",
        "feedback_b": "Correcto. log₂(8) = 3 porque 2³ = 8.",
        "feedback_c": "Incorrecto. log₂(9) ≈ 3.17 ≠ 3.",
        "feedback_d": "Incorrecto. log₂(1.5) ≈ 0.585 ≠ 3.",
        "correct_answer": "b",
        "difficulty": 2
        },
    ]

    # Preguntas de Física
    questions_fisica = [
        {
            "question_text": "¿Cuál es la unidad de medida de la fuerza en el sistema internacional?",
            "option_a": "Julio",
            "option_b": "Newton",
            "option_c": "Vatio",
            "option_d": "Pascal",
            "feedback_a": "Incorrecto. El julio es la unidad de energía.",
            "feedback_b": "Correcto. El newton es la unidad de fuerza.",
            "feedback_c": "Incorrecto. El vatio es la unidad de potencia.",
            "feedback_d": "Incorrecto. El pascal es la unidad de presión.",
            "correct_answer": "b",
            "difficulty": 1
        },
        {
        "question_text": "Según la Primera Ley de Newton, un objeto en reposo:",
        "option_a": "Acelera constantemente",
        "option_b": "Permanece en reposo a menos que actúe una fuerza",
        "option_c": "Se mueve en círculos",
        "option_d": "Pierde masa gradualmente",
        "feedback_a": "Incorrecto. Esto violaría la Primera Ley (Ley de Inercia).",
        "feedback_b": "Correcto. La Primera Ley establece que un objeto no cambia su estado de movimiento sin fuerza externa.",
        "feedback_c": "Incorrecto. Requeriría una fuerza centrípeta.",
        "feedback_d": "Incorrecto. La masa es independiente del estado de movimiento.",
        "correct_answer": "b",
        "difficulty": 1
        },
        {
        "question_text": "Si duplicas la velocidad de un objeto, su energía cinética:",
        "option_a": "Se duplica",
        "option_b": "Se cuadruplica",
        "option_c": "Se reduce a la mitad",
        "option_d": "Permanece igual",
        "feedback_a": "Incorrecto. La energía cinética depende del cuadrado de la velocidad (K = ½mv²).",
        "feedback_b": "Correcto. K ∝ v² → (2v)² = 4v².",
        "feedback_c": "Incorrecto. Aumenta, no disminuye.",
        "feedback_d": "Incorrecto. Cambia con la velocidad.",
        "correct_answer": "b",
        "difficulty": 2
        },
        {
        "question_text": "En un circuito en serie con tres resistencias iguales, la resistencia total es:",
        "option_a": "Igual a una de ellas",
        "option_b": "La suma de las tres",
        "option_c": "Un tercio de una resistencia",
        "option_d": "Cero",
        "feedback_a": "Incorrecto. En serie, las resistencias se suman.",
        "feedback_b": "Correcto. R_total = R₁ + R₂ + R₃.",
        "feedback_c": "Incorrecto. Esto sería cierto en paralelo.",
        "feedback_d": "Incorrecto. Solo ocurre en cortocircuitos.",
        "correct_answer": "b",
        "difficulty": 2
        },
        {
        "question_text": "¿Cuál proceso termodinámico ocurre a temperatura constante?",
        "option_a": "Isocórico",
        "option_b": "Isotérmico",
        "option_c": "Adiabático",
        "option_d": "Isobárico",
        "feedback_a": "Incorrecto. Isocórico = volumen constante.",
        "feedback_b": "Correcto. Isotérmico implica temperatura constante.",
        "feedback_c": "Incorrecto. Adiabático = sin transferencia de calor.",
        "feedback_d": "Incorrecto. Isobárico = presión constante.",
        "correct_answer": "b",
        "difficulty": 3
        },
        {
        "question_text": "El fenómeno donde la luz cambia de dirección al pasar de un medio a otro se llama:",
        "option_a": "Reflexión",
        "option_b": "Difracción",
        "option_c": "Refracción",
        "option_d": "Dispersión",
        "feedback_a": "Incorrecto. La reflexión ocurre en superficies.",
        "feedback_b": "Incorrecto. La difracción es el rodeo de obstáculos.",
        "feedback_c": "Correcto. Refracción = cambio de dirección por cambio de medio.",
        "feedback_d": "Incorrecto. La dispersión separa la luz en colores.",
        "correct_answer": "c",
        "difficulty": 1
        },
        {
        "question_text": "En un lanzamiento horizontal, la componente vertical de la velocidad:",
        "option_a": "Permanece constante",
        "option_b": "Aumenta linealmente con el tiempo",
        "option_c": "Disminuye exponencialmente",
        "option_d": "Es siempre cero",
        "feedback_a": "Incorrecto. La gravedad acelera la componente vertical.",
        "feedback_b": "Correcto. v_y = gt (aceleración constante).",
        "feedback_c": "Incorrecto. Aumenta, no disminuye.",
        "feedback_d": "Incorrecto. El movimiento horizontal no afecta la vertical.",
        "correct_answer": "b",
        "difficulty": 3
        },
        {
        "question_text": "Si el voltaje en un resistor aumenta al doble y su resistencia se mantiene igual, la corriente:",
        "option_a": "Se duplica",
        "option_b": "Se reduce a la mitad",
        "option_c": "Permanece igual",
        "option_d": "Se cuadruplica",
        "feedback_a": "Correcto. V = IR → si V se duplica, I también (R constante).",
        "feedback_b": "Incorrecto. La corriente aumenta con el voltaje.",
        "feedback_c": "Incorrecto. Cambia proporcionalmente al voltaje.",
        "feedback_d": "Incorrecto. La relación es lineal, no cuadrática.",
        "correct_answer": "a",
        "difficulty": 2
        },
        {
        "question_text": "Si la distancia entre dos masas se triplica, la fuerza gravitacional:",
        "option_a": "Se triplica",
        "option_b": "Se reduce a un tercio",
        "option_c": "Se reduce a un noveno",
        "option_d": "No cambia",
        "feedback_a": "Incorrecto. La fuerza gravitacional es inversamente proporcional al cuadrado de la distancia.",
        "feedback_b": "Incorrecto. F ∝ 1/r², no 1/r.",
        "feedback_c": "Correcto. F_final = F_original / (3)² = F/9.",
        "feedback_d": "Incorrecto. Depende críticamente de la distancia.",
        "correct_answer": "c",
        "difficulty": 3
        },
        {
        "question_text": "Un objeto flota si:",
        "option_a": "Su peso es mayor que el empuje",
        "option_b": "Su densidad es mayor que el fluido",
        "option_c": "Su peso es igual al empuje",
        "option_d": "Su volumen es muy pequeño",
        "feedback_a": "Incorrecto. Se hundiría en ese caso.",
        "feedback_b": "Incorrecto. La densidad del objeto debe ser menor para flotar.",
        "feedback_c": "Correcto. Equilibrio entre peso y fuerza de flotación.",
        "feedback_d": "Incorrecto. El volumen no determina flotación por sí solo.",
        "correct_answer": "c",
        "difficulty": 2
        },
          
        # Agrega más preguntas de física...
    ]

    with app.app_context():

        db.create_all()  # Create all tables

        # Agregar preguntas de lenguaje
        for q in questions_lenguaje:
            question = Question(subject='lenguaje', **q)
            db.session.add(question)
        
        # Agregar preguntas de matemáticas
        for q in questions_matematicas:
            question = Question(subject='matematicas', **q)
            db.session.add(question)
        
        # Agregar preguntas de física
        for q in questions_fisica:
            question = Question(subject='fisica', **q)
            db.session.add(question)
        
        db.session.commit()
        print("Preguntas agregadas exitosamente.")

add_questions()
# if __name__ == '__main__':