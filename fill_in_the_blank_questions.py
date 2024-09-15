# questions.py
import hashlib

questions = {
    "Python was created by ____ van Rossum.": hashlib.sha256("Guido".lower().encode()).hexdigest(),
    "The capital of France is _____.": hashlib.sha256("Paris".lower().encode()).hexdigest(),
}

def get_questions():
    return list(questions.keys())

def get_answer_hash(question):
    return questions.get(question, None)
