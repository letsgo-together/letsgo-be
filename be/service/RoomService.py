from be.repository.RoomRepository import RoomRepository
from be.repository.ItemRepository import ItemRepository
from ai.object_comparison import detect_objects
import numpy as np
import cv2


class RoomService:
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        self.roomRepository = RoomRepository.getInstance()
        self.itemRepository = ItemRepository.getInstance()

    def findAll(self):
        return self.roomRepository.findAll()

    def createRoomAndDetectItems(self, imageFile):
        if imageFile is None:
            return "No image file uploaded", 400
        file_bytes = imageFile.read()
        nparr = np.frombuffer(file_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            return "Failed to process the image", 400
        detectedItems = detect_objects(image)

        newRoom = self.roomRepository.save()
        newItems = self.itemRepository.createItem(newRoom.id, detectedItems)

        return newItems
