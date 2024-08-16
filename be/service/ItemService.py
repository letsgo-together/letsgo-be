from typing import List, Optional
from be.entity.ItemEntity import ItemEntity
from be.repository.ItemRepository import ItemRepository


class ItemService:
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        self.itemRepository = ItemRepository.getInstance()

    def createItem(self, name: str, shape: str, location: str) -> Optional[ItemEntity]:
        item = ItemEntity(id=None, name=name, shape=shape, location=location)
        return self.itemRepository.save(item)

    def getItemById(self, itemId: int) -> Optional[ItemEntity]:
        return self.itemRepository.findById(itemId)

    def getAllItems(self) -> List[ItemEntity]:
        return self.itemRepository.findAll()

    def updateItem(self, itemId: int, name: str, shape: str, location: str) -> Optional[ItemEntity]:
        existingItem = self.itemRepository.findById(itemId)
        if existingItem:
            existingItem.name = name
            existingItem.shape = shape
            existingItem.location = location
            return self.itemRepository.update(existingItem)
        return None

    def deleteItemById(self, itemId: int) -> bool:
        return self.itemRepository.deleteById(itemId)
