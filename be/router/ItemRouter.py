from flask import Blueprint
from service.ItemService import ItemService

itemRouter = Blueprint('itemRouter', __name__)
itemService = ItemService.getInstance()


@itemRouter.get('/items')
def getItems():
    return itemService.getAllItems()
