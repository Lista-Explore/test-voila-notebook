# fill_in_the_blank.py
import hashlib
from ipywidgets import widgets
from IPython.display import display, clear_output

# List of questions and their hashed answers
questions_list = [
    {
        "question": "Python was created by ____ van Rossum.",
        "answer_hash": hashlib.sha256("Guido".lower().encode()).hexdigest()
    },
    {
        "question": "The capital of France is _____.",
        "answer_hash": hashlib.sha256("Paris".lower().encode()).hexdigest()
    },
    # Add more questions here
]

# Function to validate the answer
def validate_answer(answer_hash, user_answer):
    user_answer_hash = hashlib.sha256(user_answer.lower().encode()).hexdigest()
    return user_answer_hash == answer_hash

# Function to display questions one at a time
def display_questions():
    index = 0
    num_questions = len(questions_list)

    # Widgets
    question_widget = widgets.Label()
    answer_widget = widgets.Text(placeholder='Type your answer here')
    submit_button = widgets.Button(description='Submit')
    feedback_widget = widgets.Output()
    navigation_widget = widgets.HBox()
    prev_button = widgets.Button(description='Previous')
    next_button = widgets.Button(description='Next')
    progress_widget = widgets.Label()
    complete_widget = widgets.Output()

    def update_question():
        question_data = questions_list[index]
        question_widget.value = f"Question {index + 1}/{num_questions}: {question_data['question']}"
        answer_widget.value = ''
        answer_widget.disabled = False
        submit_button.disabled = False
        with feedback_widget:
            clear_output()
        progress_widget.value = f"Question {index + 1} of {num_questions}"

    def on_submit(b):
        user_answer = answer_widget.value.strip()
        correct = validate_answer(questions_list[index]['answer_hash'], user_answer)
        with feedback_widget:
            clear_output()
            if correct:
                print("✅ Correct!")
                answer_widget.disabled = True
                submit_button.disabled = True
            else:
                print("❌ Incorrect. Please try again.")

    def on_prev(b):
        nonlocal index
        if index > 0:
            index -= 1
            update_question()

    def on_next(b):
        nonlocal index
        if index < num_questions - 1:
            index += 1
            update_question()
        else:
            with complete_widget:
                clear_output()
                print("🎉 You've completed all questions!")

    submit_button.on_click(on_submit)
    prev_button.on_click(on_prev)
    next_button.on_click(on_next)

    navigation_widget.children = [prev_button, next_button]

    display(widgets.VBox([
        question_widget,
        answer_widget,
        submit_button,
        feedback_widget,
        navigation_widget,
        progress_widget,
        complete_widget
    ]))

    update_question()
