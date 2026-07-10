from abc import ABC, abstractmethod
from typing import List
from backend.app.schemas.schemas import SnapshotBase
from datetime import datetime

class BaseCollector(ABC):
    def __init__(self):
        self.exchange = "UNKNOWN"
        
    @abstractmethod
    async def fetch(self) -> dict:
        """Fetch raw data from the exchange."""
        pass
        
    @abstractmethod
    def normalize(self, raw_data: dict) -> List[SnapshotBase]:
        """Normalize raw data into a common Snapshot schema."""
        pass
        
    async def collect(self) -> List[SnapshotBase]:
        raw_data = await self.fetch()
        return self.normalize(raw_data)
