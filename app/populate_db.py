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
            "question_text": "¿Cuál es el sujeto en la oración 'El niño juega en el parque'?",
            "option_a": "El niño",
            "option_b": "juega",
            "option_c": "en el parque",
            "option_d": "Ninguna de las anteriores",
            "feedback_a": "Correcto. El sujeto es quien realiza la acción.",
            "feedback_b": "Incorrecto. 'Juega' es el verbo, no el sujeto.",
            "feedback_c": "Incorrecto. 'En el parque' es el complemento circunstancial de lugar.",
            "feedback_d": "Incorrecto. La opción a es correcta.",
            "correct_answer": "a",
            "difficulty": 1,
        },
        {
            "question_text": "¿Cuál de las siguientes figuras literarias se encuentra ejemplificada en la expresión 'El murmullo de las abejas'?",
            "option_a": "Metáfora",
            "option_b": "Hipérbole",
            "option_c": "Onomatopeya",
            "option_d": "Aliteración",
            "feedback_a": "Incorrecto. Una metáfora es una comparación implícita, no una imitación de sonido.",
            "feedback_b": "Incorrecto. Una hipérbole es una exageración.",
            "feedback_c": "Incorrecto. La onomatopeya imita un sonido.",
            "feedback_d": "Correcto. 'Murmullo' imita el sonido de las abejas, lo cual es la definición de onomatopeya.",
            "correct_answer": "c",  # Changed to c to match feedback
            "difficulty": 2,
        },
        # Agrega más preguntas de lenguaje...
    ]

    # Preguntas de Matemáticas
    questions_matematicas = [
        {
        "question_text": "Resuelve la siguiente ecuación lineal: 3x - 5 = 20",
        "option_a": "7.33",
        "option_b": "8.33",
        "option_c": "7",
        "option_d": "9",
        "feedback_a": "Incorrecto. Suma 5 a ambos lados y luego divide por 3.",
        "feedback_b": "Correcto. 3x = 25, entonces x = 25/3 ≈ 8.33",
        "feedback_c": "Incorrecto. Revisa tus operaciones.",
        "feedback_d": "Incorrecto. Revisa tus cálculos.",
        "correct_answer": "b",
        "difficulty": 1,
        },
        {
        "question_text": "¿Cuál es el área de un triángulo con base 6 y altura 4?",
        "option_a": "10",
        "option_b": "12",
        "option_c": "24",
        "option_d": "48",
        "feedback_a": "Incorrecto. Recuerda la fórmula del área del triángulo.",
        "feedback_b": "Correcto. Área = (base * altura) / 2 = (6 * 4) / 2 = 12",
        "feedback_c": "Incorrecto. Multiplicaste base por altura, pero olvidaste dividir por 2.",
        "feedback_d": "Incorrecto. Revisa la fórmula.",
        "correct_answer": "b",
        "difficulty": 1
        },
        # Agrega más preguntas de matemáticas...
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
            "question_text": "Un objeto se deja caer desde el reposo en caída libre. Considerando que la aceleración debida a la gravedad es de 9.8 m/s², ¿cuál es su velocidad después de 3.0 segundos? (Desprecia la resistencia del aire).",
            "option_a": "9.8 m/s",
            "option_b": "19.6 m/s",
            "option_c": "29.4 m/s",
            "option_d": "39.2 m/s",
            "feedback_a": "Incorrecto. 9.8 m/s es la aceleración, no la velocidad.",
            "feedback_b": "Incorrecto. Multiplicaste por 2 segundos en lugar de 3.",
            "feedback_c": "Correcto. La velocidad se calcula como v = gt = 9.8 m/s² * 3 s = 29.4 m/s.",
            "feedback_d": "Incorrecto. Revisa tu cálculo.",
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