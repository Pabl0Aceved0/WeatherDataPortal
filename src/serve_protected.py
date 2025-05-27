from flask import Flask, send_from_directory
import os

app = Flask(__name__)
# It's good practice to have a secret key, though not strictly necessary for serving a static file.
# For production, consider setting this from an environment variable.
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))

@app.route('/')
def index():
    print("Serving index.html from static directory")
    return send_from_directory('static', 'index.html')  # Serve from the static directory
