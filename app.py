# app.py

from flask import Flask, render_template_string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

@app.route('/')
def fetch_scores():
    # Set up Selenium options for headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.espn.com/mlb/scoreboard')
    time.sleep(5)  # Allow time for the page to load

    # Fetch some sample data (update CSS selectors based on the target site)
    try:
        scores = driver.find_elements(By.CLASS_NAME, 'team-score')
        scores_text = [score.text for score in scores if score.text]
    except Exception as e:
        scores_text = [f"Error fetching scores: {e}"]

    # Clean up
    driver.quit()

    # Render the result
    html_template = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Scores</title>
    </head>
    <body>
        <h1>Baseball Scores</h1>
        <ul>
            {% for score in scores %}
                <li>{{ score }}</li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """
    return render_template_string(html_template, scores=scores_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
