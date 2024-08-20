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

    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
