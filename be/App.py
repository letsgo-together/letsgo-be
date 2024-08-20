from flask import Flask
from router.ItemRouter import itemRouter
from router.RoomRouter import roomRouter
import sys
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

app.register_blueprint(itemRouter)
app.register_blueprint(roomRouter)

if __name__ == '__main__':
    app.run()