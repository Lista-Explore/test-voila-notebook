import requests
from IPython.display import display, HTML

def render_drag_and_drop(questions_url):
    # GitHub raw URL for the HTML file
    html_template_url = "https://raw.githubusercontent.com/your-username/your-repo/main/drag_and_drop.html"
    
    # Fetch the HTML content from the URL
    response = requests.get(html_template_url)
    html_content = response.text
    
    # Insert the questions_url into the HTML
    html_with_url = html_content.replace('</head>', f'<script>var questions_url="{questions_url}";</script></head>')
    
    # Display the HTML content
    display(HTML(html_with_url))
