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

    def findAllByRoomId(self, room_id):
        return self.itemRepository.findAllByRoomId(room_id)

    def saveSelectedItems(self, room_id, selectedItems):
        return self.itemRepository.saveItems(room_id, selectedItems)
