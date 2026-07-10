from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class IssueBase(BaseModel):
    exchange: str
    symbol: str
    scripcode: Optional[str] = None
    name: str
    status: str

class IssueCreate(IssueBase):
    pass

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

class Snapshot(SnapshotBase):
    id: int

    class Config:
        from_attributes = True

class AggregateBase(BaseModel):
    exchange: str
    price: float
    quantity: int
    timestamp: datetime

class Aggregate(AggregateBase):
    id: int

    class Config:
        from_attributes = True

class AnalyticsResponse(BaseModel):
    weighted_average: float
    highest_bid: float
    lowest_bid: float
    total_quantity: int
    cumulative_demand: List[dict]

class TimeSeriesResponse(BaseModel):
    timestamp: datetime
    price: float
    quantity: int

class LadderEntry(BaseModel):
    price: float
    quantity: int
    
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
