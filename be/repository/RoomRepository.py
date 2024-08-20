import mysql.connector
import os
from mysql.connector import Error as MySQLError
from typing import List, Optional
from be.entity.RoomEntity import RoomEntity


class RoomRepository:
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        if not hasattr(self, 'connection'):
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
            CREATE TABLE IF NOT EXISTS room (
                id INT AUTO_INCREMENT PRIMARY KEY
            )
        """
        self.cursor.execute(query)
        self.connection.commit()

    def findAll(self) -> List[RoomEntity]:
        query = "SELECT * FROM room"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return [RoomEntity(id=row[0]) for row in rows]

    def save(self) -> Optional[RoomEntity]:
        query = "INSERT INTO room VALUES (NULL)"
        self.cursor.execute(query)
        self.connection.commit()
        return RoomEntity(id=self.cursor.lastrowid)

    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
