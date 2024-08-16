import mysql.connector
import os
from mysql.connector import Error as MySQLError
from typing import List, Optional
from be.entity.ItemEntity import ItemEntity


class ItemRepository:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_DATABASE")
        )
        self.cursor = self.connection.cursor()
        self.createTableIfNotExist()  # 테이블이 없으면 생성

    def createTableIfNotExist(self):
        query = """
            CREATE TABLE IF NOT EXISTS items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                shape VARCHAR(255) NOT NULL,
                location VARCHAR(255) NOT NULL
            )
        """
        self.cursor.execute(query)
        self.connection.commit()

    def save(self, item: ItemEntity) -> Optional[ItemEntity]:
        query = """
            INSERT INTO items (name, shape, location) VALUES (%s, %s, %s)
        """
        try:
            self.cursor.execute(query, (item.name, item.shape, item.location))
            self.connection.commit()
            item.id = self.cursor.lastrowid
            return item
        except MySQLError as e:
            print(f"Error creating item: {e}")
            return None

    def findById(self, itemId: int) -> Optional[ItemEntity]:
        query = "SELECT * FROM items WHERE id = %s"
        try:
            self.cursor.execute(query, (itemId,))
            result = self.cursor.fetchone()
            if result:
                return ItemEntity(id=result[0], name=result[1], shape=result[2], location=result[3])
            return None
        except MySQLError as e:
            print(f"Error reading item: {e}")
            return None

    def findAll(self) -> List[ItemEntity]:
        query = "SELECT * FROM items"
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return [ItemEntity(id=row[0], name=row[1], shape=row[2], location=row[3]) for row in results]
        except MySQLError as e:
            print(f"Error listing items: {e}")
            return []

    def update(self, item: ItemEntity) -> Optional[ItemEntity]:
        query = """
            UPDATE items SET name = %s, shape = %s, location = %s WHERE id = %s
        """
        try:
            self.cursor.execute(query, (item.name, item.shape, item.location, item.id))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                return item
            return None
        except MySQLError as e:
            print(f"Error updating item: {e}")
            return None

    def deleteById(self, itemId: int) -> bool:
        query = "DELETE FROM items WHERE id = %s"
        try:
            self.cursor.execute(query, (itemId,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except MySQLError as e:
            print(f"Error deleting item: {e}")
            return False

    def __del__(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
