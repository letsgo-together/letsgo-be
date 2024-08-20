from flask import Blueprint
from be.service.RoomService import RoomService

roomRouter = Blueprint('roomRouter', __name__)
roomService = RoomService.getInstance()


@roomRouter.get('/rooms')
def findAll():
    return roomService.findAll()
