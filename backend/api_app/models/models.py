from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from backend.app.database.database import Base

class Issue(Base):
    __tablename__ = "issues"
    
    id = Column(Integer, primary_key=True, index=True)
    exchange = Column(String, index=True)
    symbol = Column(String, index=True)
    scripcode = Column(String, index=True, nullable=True)
    name = Column(String)
    status = Column(String)

class Snapshot(Base):
    __tablename__ = "snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), index=True)
    exchange = Column(String, index=True)
    issue = Column(String, index=True)
    investor_type = Column(String, default="NON_RETAIL")
    category = Column(String, index=True)
    price = Column(Float, index=True)
    quantity = Column(Integer)
    bids = Column(Integer, default=0)
    confirmed_qty = Column(Integer, default=0)
    unconfirmed_qty = Column(Integer, default=0)

class Aggregate(Base):
    __tablename__ = "aggregates"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), index=True)
    exchange = Column(String, index=True)
    price = Column(Float, index=True)
    quantity = Column(Integer)

class Change(Base):
    __tablename__ = "changes"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), index=True)
    price = Column(Float, index=True)
    previous_quantity = Column(Integer)
    current_quantity = Column(Integer)
    delta = Column(Integer)
