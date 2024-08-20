from dataclasses import dataclass
from typing import Optional


@dataclass
class RoomEntity:
    id: Optional[int]
    default_image_url: str
