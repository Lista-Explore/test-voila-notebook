from IPython.display import display, HTML
import json

# Path to your local HTML file
html_file_path = "drag_and_drop.html"

# Path to your local data file (JSON)
data_file_path = "drag_and_drop_data.json"

# Read the HTML content from the local file
with open(html_file_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Read the data file content
with open(data_file_path, 'r', encoding='utf-8') as f:
    data_json = json.load(f)

# Convert data_json to a JSON string
data_js = json.dumps(data_json)

# Inject the data into the HTML content
# Insert a script tag to set the data variable
script_tag = f'<script>var data = {data_js};</script>'
html_content = html_content.replace(
    '<script>',
    script_tag + '\n<script>'
)

# Display the HTML content
display(HTML(html_content))
