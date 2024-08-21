from flask import Flask
from router.ItemRouter import itemRouter
import sys
from dotenv import load_dotenv
from flask_cors import CORS


load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(itemRouter)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if __name__ == '__main__':
    app.run()
