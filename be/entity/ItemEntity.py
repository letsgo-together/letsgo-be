from dataclasses import dataclass
from typing import Optional


@dataclass
class ItemEntity:
    id: Optional[int]
    room_id: int
    bbox: str
    confidence: float
    class_id: int
    class_name: str
    unique_id: str
