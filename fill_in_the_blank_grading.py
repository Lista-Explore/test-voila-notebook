from fill_in_the_blank_questions import get_questions, get_answer_hash

def get_question_for_student(index=0):
    questions = get_questions()
    return questions[index]

def validate_answer(question, user_answer):
    correct_answer_hash = get_answer_hash(question)
    user_answer_hash = hashlib.sha256(user_answer.lower().encode()).hexdigest()
    return user_answer_hash == correct_answer_hash