from flask import Blueprint, request
from be.service.RoomService import RoomService

roomRouter = Blueprint('roomRouter', __name__)
roomService = RoomService.getInstance()


@roomRouter.get('/rooms')
def findAll():
    return roomService.findAll()


@roomRouter.post('/rooms')
def createRoomAndDetectItems():
    imageFile = request.files.get('image')
    return roomService.createRoomAndDetectItems(imageFile)


@roomRouter.get('/rooms/<roomId>/diff')
def getRoomDiff(roomId):
    imageFile = request.files.get('image')
    return roomService.getRoomDiff(roomId, imageFile)
