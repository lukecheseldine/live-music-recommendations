from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
<<<<<<< HEAD
    return render_template('index.html')

@app.route('/lol')
def test():
    pass
=======
    return 'Hello, World!'


def tester():
    pass
>>>>>>> fcd780a8cc8e421913b9dcfd3715f7fd852943ee
