from flask import Flask
from router.ItemRouter import itemRouter
from router.RoomRouter import roomRouter
import sys
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.register_blueprint(itemRouter)
app.register_blueprint(roomRouter)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if __name__ == '__main__':
    app.run()
