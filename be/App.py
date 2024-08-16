from flask import Flask
from router.ItemRouter import itemRouter
import sys


app = Flask(__name__)

app.register_blueprint(itemRouter)

if __name__ == '__main__':
    app.run()