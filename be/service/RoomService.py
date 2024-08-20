from be.repository.RoomRepository import RoomRepository


class RoomService:
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        self.roomRepository = RoomRepository.getInstance()

    def findAll(self):
        return self.roomRepository.findAll()
