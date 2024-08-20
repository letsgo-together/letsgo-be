from flask import Blueprint
from be.service.ItemService import ItemService

itemRouter = Blueprint('itemRouter', __name__)
itemService = ItemService.getInstance()
