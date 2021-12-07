from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["*"])  # allow it from todos los lugares

from backend.app import views


