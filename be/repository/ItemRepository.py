import mysql.connector
import os
from mysql.connector import Error as MySQLError
from typing import List, Optional
from be.entity.ItemEntity import ItemEntity


class ItemRepository:
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        if not hasattr(self, 'connection'):  # 중복 초기화를 방지 (클래스에 connection이라는 변수가 없으면)
            self.connection = mysql.connector.connect(
                host=os.environ.get("DB_HOST"),
                port=os.environ.get("DB_PORT"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                database=os.environ.get("DB_DATABASE")
            )
            self.cursor = self.connection.cursor()
            self.createTableIfNotExist()

    def createTableIfNotExist(self):
        query = """
            CREATE TABLE IF NOT EXISTS item (
                id INT AUTO_INCREMENT PRIMARY KEY,
                room_id INT NOT NULL,
                bbox VARCHAR(255) NOT NULL,
                confidence FLOAT NOT NULL,
                class_id INT NOT NULL,
                class_name VARCHAR(255) NOT NULL,
                unique_id VARCHAR(255) NOT NULL
            )
        """
        self.cursor.execute(query)
        self.connection.commit()

    def saveItems(self, room_id: int, items: List[object]) -> List[ItemEntity]:
        query = """
            INSERT INTO item (room_id, bbox, confidence, class_id, class_name, unique_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        savedItems = []
        for item in items:
            self.cursor.execute(query, (
            room_id, item['bbox'], item['confidence'], item['class_id'], item['class_name'], item['unique_id']))
            self.connection.commit()
            savedItems.append(ItemEntity(
                id=self.cursor.lastrowid,
                room_id=room_id,
                bbox=item['bbox'],
                confidence=item['confidence'],
                class_id=item['class_id'],
                class_name=item['class_name'],
                unique_id=item['unique_id']
            ))
        return savedItems

    def findAllByRoomId(self, roomId) -> List[ItemEntity]:
        query = "SELECT * FROM item WHERE room_id = %s"
        self.cursor.execute(query, (roomId,))
        items = []
        for (id, room_id, bbox, confidence, class_id, class_name, unique_id) in self.cursor:
            items.append(ItemEntity(
                id=id,
                room_id=room_id,
                bbox=bbox,
                confidence=confidence,
                class_id=class_id,
                class_name=class_name,
                unique_id=unique_id
            ))
        return items

    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
