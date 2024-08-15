from flask import Blueprint

itemRouter = Blueprint('itemRouter', __name__)


@itemRouter.get('/items')
def getItems():
    return { "test": "test" }
