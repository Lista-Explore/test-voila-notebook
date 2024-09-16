# fill_in_the_blank.py
import hashlib
from ipywidgets import widgets
from IPython.display import display, clear_output, HTML
import json
import urllib.request
from urllib.error import URLError, HTTPError

# Function to load questions from a URL
def load_questions(file_url):
    try:
        response = urllib.request.urlopen(file_url)
        data = response.read().decode('utf-8')
        questions = json.loads(data)
    except (URLError, HTTPError) as e:
        print(f"Error accessing questions file at URL: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from URL: {e}")
        return []

    # For each question, compute the hash of the answers
    for q in questions:
        if 'blanks' in q:
            # Multiple blanks
            answer_hashes = []
            for answers in q['blanks']:
                if isinstance(answers, list):
                    # Multiple acceptable answers for this blank
                    hashes = [hashlib.sha256(ans.lower().encode()).hexdigest() for ans in answers]
                else:
                    hashes = [hashlib.sha256(answers.lower().encode()).hexdigest()]
                answer_hashes.append(hashes)
            q['answer_hashes'] = answer_hashes
        elif 'answer' in q:
            # Single blank
            if isinstance(q['answer'], list):
                # Multiple acceptable answers
                hashes = [hashlib.sha256(ans.lower().encode()).hexdigest() for ans in q['answer']]
            else:
                hashes = [hashlib.sha256(q['answer'].lower().encode()).hexdigest()]
            q['answer_hashes'] = hashes
        else:
            print("Error: Question without 'answer' or 'blanks' key.")
            return []
    return questions

# Function to validate the answers
def validate_answers(answer_hashes, user_answers):
    if isinstance(answer_hashes[0], list):
        # Multiple blanks
        for user_answer, acceptable_hashes in zip(user_answers, answer_hashes):
            user_answer_hash = hashlib.sha256(user_answer.lower().encode()).hexdigest()
            if user_answer_hash not in acceptable_hashes:
                return False
        return True
    else:
        # Single blank
        user_answer_hash = hashlib.sha256(user_answers[0].lower().encode()).hexdigest()
        return user_answer_hash in answer_hashes

# Function to display questions one at a time
def display_questions(questions_file):
    questions_list = load_questions(questions_file)
    if not questions_list:
        return
    index = 0
    num_questions = len(questions_list)

    # Widgets
    question_widget = widgets.HTML()
    answer_widgets = []
    submit_button = widgets.Button(description='Submit')
    feedback_widget = widgets.Output()
    navigation_widget = widgets.HBox()
    prev_button = widgets.Button(description='Previous')
    next_button = widgets.Button(description='Next')
    progress_widget = widgets.Label()
    complete_widget = widgets.Output()

    def update_question():
        nonlocal answer_widgets
        question_data = questions_list[index]
        num_blanks = question_data['question'].count('____')

        # Prepare the question text
        question_html = f"<b>Question {index + 1}/{num_questions}:</b> {question_data['question']}"
        if 'image' in question_data:
            question_html += f"<br><img src='{question_data['image']}' width='400'>"

        question_widget.value = question_html

        # Clear previous answer widgets
        answer_widgets = []
        answer_widget_container.children = []

        # Create input fields
        if num_blanks > 0:
            for _ in range(num_blanks):
                ans_widget = widgets.Text(placeholder='Type your answer here')
                answer_widgets.append(ans_widget)
            answer_widget_container.children = answer_widgets
        else:
            ans_widget = widgets.Text(placeholder='Type your answer here')
            answer_widgets.append(ans_widget)
            answer_widget_container.children = answer_widgets

        submit_button.disabled = False
        for w in answer_widgets:
            w.disabled = False
        with feedback_widget:
            clear_output()
        progress_widget.value = f"Question {index + 1} of {num_questions}"

    def on_submit(b):
        user_answers = [w.value.strip() for w in answer_widgets]
        correct = validate_answers(questions_list[index]['answer_hashes'], user_answers)
        with feedback_widget:
            clear_output()
            if correct:
                print("✅ Correct!")
                for w in answer_widgets:
                    w.disabled = True
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
    answer_widget_container = widgets.VBox()

    display(widgets.VBox([
        question_widget,
        answer_widget_container,
        submit_button,
        feedback_widget,
        navigation_widget,
        progress_widget,
        complete_widget
    ]))

    update_question()
