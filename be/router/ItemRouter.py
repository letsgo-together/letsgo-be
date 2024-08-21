from flask import Blueprint, request
from be.service.ItemService import ItemService

itemRouter = Blueprint('itemRouter', __name__)
itemService = ItemService.getInstance()


@itemRouter.post('/items/detect')
def detectItems():
    imageFile = request.files.get('image')
    return itemService.detectItems(imageFile)


@itemRouter.get('/items')
def findAllByRoomId():
    return itemService.findAll()


@itemRouter.post('/items')
def saveSelectedItems():
    data = request.get_json()
    if data is None:
        return "No data provided", 400

    selectedItems = []
    for item in data['selectedItems']:
        selectedItems.append({
            'bbox': item.get('bbox'),
            'confidence': item.get('confidence'),
            'class_id': item.get('class_id'),
            'class_name': item.get('class_name'),
            'unique_id': item.get('unique_id')
        })

    return itemService.saveSelectedItems(selectedItems)


@itemRouter.post("/items/find")
def findItemsPosition():
    imageFile = request.files.get('image')
    class_names = request.args.get('class_names').split(',')
    return itemService.findItemsPosition(imageFile, class_names)

