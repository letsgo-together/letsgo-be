from flask import Blueprint

itemRouter = Blueprint('itemRouter', __name__)
itemService = ItemService.getInstance()


@itemRouter.get('/items')
def getItems():
    return itemService.getAllItems()
