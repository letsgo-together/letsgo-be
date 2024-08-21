from be.repository.ItemMemoryRepository import ItemMemoryRepository
from ai.de import detect_objects, find_and_describe_object
from be.util.util import changeClassNameToKor
from flask import jsonify
import numpy as np
import cv2


class ItemService:
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        self.itemRepository = ItemMemoryRepository.getInstance()

    def detectItems(self, imageFile):
        if imageFile is None:
            return "No image file uploaded", 400
        file_bytes = imageFile.read()
        nparr = np.frombuffer(file_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            return "Failed to process the image", 400
        detectedItems = detect_objects(image)
        for item in detectedItems:
            item.update({"class_name": changeClassNameToKor(item.get("class_name"))})
        return detectedItems

    def findAll(self):
        return self.itemRepository.findAll()

    def saveSelectedItems(self, selectedItems):
        return self.itemRepository.saveItems(selectedItems)

    def findItemsPosition(self, imageFile, class_names):
        if imageFile is None:
            return "No image file uploaded", 400
        file_bytes = imageFile.read()
        nparr = np.frombuffer(file_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            return "Failed to process the image", 400
        descriptions = []
        for class_name in class_names:
            description = find_and_describe_object(image, class_name)
            descriptions.append({
                class_name: description
            })

        return jsonify(descriptions)
