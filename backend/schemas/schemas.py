from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone

class IssueBase(BaseModel):
    exchange: str
    symbol: str
    scripcode: Optional[str] = None
    name: str
    status: str

class Issue(IssueBase):
    id: int

    class Config:
        from_attributes = True

class SnapshotBase(BaseModel):
    exchange: str
    issue: str
    investor_type: str = "NON_RETAIL"
    category: str
    price: float
    quantity: int
    bids: int = 0
    confirmed_qty: int = 0
    unconfirmed_qty: int = 0
    timestamp: datetime

class Aggregate(BaseModel):
    id: int
    exchange: str
    price: float
    quantity: int
    timestamp: datetime

    class Config:
        from_attributes = True
    
class CombinedLadderEntry(BaseModel):
    price: float
    nse_quantity: int
    bse_quantity: int
    total_quantity: int
    bids: int = 0
    confirmed_qty: int = 0
    unconfirmed_qty: int = 0
    cumulative_total: int = 0
    cumulative_confirmed: int = 0
    cumulative_unconfirmed: int = 0

class CombinedLadderResponse(BaseModel):
    nse_last_updated: Optional[datetime] = None
    bse_last_updated: Optional[datetime] = None
    ladder: List[CombinedLadderEntry]
