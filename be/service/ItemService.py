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

    def findAllByRoomId(self, roomId):
        return self.itemRepository.findAllByRoomId(roomId)
