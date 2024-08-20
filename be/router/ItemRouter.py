from flask import Blueprint
from be.service.ItemService import ItemService

itemRouter = Blueprint('itemRouter', __name__)
itemService = ItemService.getInstance()


@itemRouter.get('/items/<roomId>')
def findAllByRoomId(roomId):
    return itemService.findAllByRoomId(roomId)
