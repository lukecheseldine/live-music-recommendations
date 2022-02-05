from flask import Flask, render_template
from requests import get

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
