from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lol')
def test():
    pass
    return 'Hello, World!'


def tester():
    pass
