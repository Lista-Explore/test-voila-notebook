# drag_and_drop.py
import json
import urllib.request
from urllib.error import URLError, HTTPError
from IPython.display import display, HTML
import hashlib

def load_questions(file_url):
    try:
        response = urllib.request.urlopen(file_url)
        data = response.read().decode('utf-8')
        questions = json.loads(data)
    except (URLError, HTTPError) as e:
        print(f"Error accessing questions file at URL: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from URL: {e}")
        return None
    return questions

def generate_html(questions):
    # Extract data
    image_url = questions.get('image', '')
    items = questions.get('items', [])
    dropzones = questions.get('dropzones', [])

    # Generate draggable items HTML
    draggable_html = ''
    for item in items:
        draggable_html += f'<div class="draggable" draggable="true" id="{item["id"]}">{item["content"]}</div>\n'

    # Generate dropzones HTML
    dropzone_html = ''
    for dz in dropzones:
        dropzone_html += f'<div class="dropzone" id="{dz["id"]}">{dz["content"]}</div>\n'

    # HTML Template
    html_template = f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Drag-and-Drop Activity</title>
    <style>
        /* Your CSS styles */
        #drag-container, #drop-container {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }
        .draggable, .dropzone {
            width: 100px;
            height: 60px;
            border: 2px solid #ccc;
            border-radius: 5px;
            text-align: center;
            line-height: 60px;
            font-weight: bold;
            user-select: none;
        }
        .draggable {
            background-color: #f0f0f0;
            cursor: grab;
        }
        .dropzone {
            background-color: #fafafa;
        }
        .dropzone.correct {
            background-color: #c8e6c9;
            border-color: #2e7d32;
        }
        .dropzone.incorrect {
            background-color: #ffcdd2;
            border-color: #c62828;
        }
    </style>
</head>
<body>
    <p>Drag each item into its corresponding space:</p>

    <div id="drag-container"></div>
    <div id="drop-container"></div>

    <script>
        // Fetch the questions file
        fetch('questions.json') // This will be replaced with the actual URL in the notebook
            .then(response => response.json())
            .then(data => {
                const dragContainer = document.getElementById('drag-container');
                const dropContainer = document.getElementById('drop-container');

                // Create draggable items
                data.items.forEach(item => {
                    const draggable = document.createElement('div');
                    draggable.className = 'draggable';
                    draggable.draggable = true;
                    draggable.id = item.id;
                    draggable.textContent = item.label;
                    dragContainer.appendChild(draggable);
                });

                // Create dropzones
                data.items.forEach(item => {
                    const dropzone = document.createElement('div');
                    dropzone.className = 'dropzone';
                    dropzone.id = item.correct_space;
                    dropzone.textContent = item.correct_space;
                    dropContainer.appendChild(dropzone);
                });

                // Set up drag-and-drop functionality
                setUpDragAndDrop();
            });

        function setUpDragAndDrop() {
            const draggables = document.querySelectorAll('.draggable');
            const dropzones = document.querySelectorAll('.dropzone');

            draggables.forEach(draggable => {
                draggable.addEventListener('dragstart', e => {
                    e.dataTransfer.setData('text/plain', e.target.id);
                });
            });

            dropzones.forEach(dropzone => {
                dropzone.addEventListener('dragover', e => {
                    e.preventDefault(); // Allow dropping
                });

                dropzone.addEventListener('drop', e => {
                    e.preventDefault();
                    const draggableId = e.dataTransfer.getData('text/plain');
                    const draggableElement = document.getElementById(draggableId);

                    if (!dropzone.hasChildNodes()) {
                        dropzone.appendChild(draggableElement);
                    }

                    const correctSpaceId = data.items.find(item => item.id === draggableId).correct_space;
                    if (correctSpaceId === dropzone.id) {
                        dropzone.classList.add('correct');
                        dropzone.classList.remove('incorrect');
                    } else {
                        dropzone.classList.add('incorrect');
                        dropzone.classList.remove('correct');
                    }
                });
            });
        }
    </script>
</body>
</html>

    """
    return html_template

def display_drag_and_drop(questions_file_url):
    questions = load_questions(questions_file_url)
    if not questions:
        print("Failed to load questions.")
        return
    html_content = generate_html(questions)
    display(HTML(html_content))
