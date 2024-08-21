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
        result = []
        for item in selectedItems:
            item["id"] = len(self.items) + 1
            result.append(item)
        self.items = result
        return selectedItems

    def findAll(self):
        return self.items