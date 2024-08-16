from dataclasses import dataclass
from typing import Optional


@dataclass
class ItemEntity:
    name: str
    shape: str  # TODO: AI를 위한 물건 이미지 데이터
    location: str  # TODO: AI를 위한 물건 위치 데이터
    id: Optional[int] = None
