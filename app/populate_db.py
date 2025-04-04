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
            "feedback_a": "",
            "feedback_b": "",
            "feedback_c": "",
            "feedback_d": "",
            "correct_answer": "a",
            "difficulty": 1
        },
        {
            "question_text": "¿Qué figura literaria predomina en 'El murmullo de las abejas'?",
            "option_a": "Metáfora",
            "option_b": "Hipérbole",
            "option_c": "Onomatopeya",
            "option_d": "Aliteración",
            "feedback_a": "",
            "feedback_b": "",
            "feedback_c": "",
            "feedback_d": "",
            "correct_answer": "d",
            "difficulty": 2
        },
        # Agrega más preguntas de lenguaje...
    ]

    # Preguntas de Matemáticas
    questions_matematicas = [
        {
            "question_text": "¿Cuál es el resultado de 3x - 5 = 20?", 
            "option_a": "x = 8.34",
            "option_b": "x = 5",
            "option_c": "x = 7",
            "option_d": "x = 9",
            "feedback_a": "",
            "feedback_b": "",
            "feedback_c": "",
            "feedback_d": "",
            "correct_answer": "b",
            "difficulty": 1
        },
        {
            "question_text": "¿Cuál es el área de un triángulo con base 6 y altura 4?",
            "option_a": "10",
            "option_b": "12",
            "option_c": "24",
            "option_d": "48",
            "feedback_a": "",
            "feedback_b": "",
            "feedback_c": "",
            "feedback_d": "",
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
            "feedback_a": "",
            "feedback_b": "",
            "feedback_c": "",
            "feedback_d": "",
            "correct_answer": "b",
            "difficulty": 1
        },
        {
            "question_text": "¿A qué velocidad cae un objeto en caída libre después de 3 segundos (despreciando la resistencia del aire)?",
            "option_a": "9.8 m/s",
            "option_b": "19.6 m/s",
            "option_c": "29.4 m/s",
            "option_d": "39.2 m/s",
            "feedback_a": "",
            "feedback_b": "",
            "feedback_c": "",
            "feedback_d": "",
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