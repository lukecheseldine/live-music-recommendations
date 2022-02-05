from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
<<<<<<< HEAD
=======


@app.route('/lol')
def test():
    pass
    return 'Hello, World!'


def tester():
    pass
>>>>>>> a3e0e40839116b9f4a410f4388d024d307b6e68f
