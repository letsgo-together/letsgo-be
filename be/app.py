from flask import Flask
import sys

sys.path.append('..')
from ai.test import printTest
printTest()

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()