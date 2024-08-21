from flask import Blueprint, request
from be.service.ItemService import ItemService

itemRouter = Blueprint('itemRouter', __name__)
itemService = ItemService.getInstance()


@itemRouter.get('/items/detect')
def detectItems():
    imageFile = request.files.get('image')
    return itemService.detectItems(imageFile)


@itemRouter.get('/items/<room_id>')
def findAllByRoomId(room_id):
    return itemService.findAllByRoomId(room_id)


@itemRouter.post('/items/<room_id>')
def saveSelectedItems(room_id):
    data = request.get_json()
    if data is None:
        return "No data provided", 400

    requestData = []
    for item in data:
        requestData.append({
            'bbox': item.get('bbox'),
            'confidence': item.get('confidence'),
            'class_id': item.get('class_id'),
            'class_name': item.get('class_name'),
            'unique_id': item.get('unique_id')
        })

    return itemService.saveSelectedItems(room_id, requestData)
