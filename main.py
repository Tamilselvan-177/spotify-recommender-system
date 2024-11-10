import flask
from flask import Flask, request, render_template
from model import collect_song_data
from urllib.parse import urlparse


app = Flask(__name__)


def is_valid_url(url):
    """Check if the input string is a valid URL."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])  # Check if both scheme and netloc are present
    except ValueError:
        return False

@app.route('/')
def index():
    return render_template('sopfity.html')  # Ensure this is your index.html

@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form['user_input']
    
    # Validate the input URL 
    
    if not is_valid_url(user_input):
        return render_template('sopfity.html', error="Invalid URL. Please enter a valid Spotify link.")
    
    # Process the valid URL
    indexdata = collect_song_data(user_input)

    return render_template('result.html', items=indexdata)

@app.route('/about')
def about():
    return render_template('about.html')  # About page

@app.route('/model-details')
def model_details():
    return render_template('model_details.html')

if __name__ == '__main__':
    app.run()
