class ItemMemoryRepository:
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        self.items = []

    def saveItems(self, selectedItems):
        for item in selectedItems:
            item["id"] = len(self.items) + 1
            self.items.append(item)
        return selectedItems

    def findAll(self):
        return self.items