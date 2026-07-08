from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter()

@router.get("/issues", response_model=List[schemas.Issue])
def get_issues(db: Session = Depends(get_db)):
    return db.query(models.Issue).all()

@router.post("/issues", response_model=schemas.Issue)
def create_issue(issue: schemas.IssueCreate, db: Session = Depends(get_db)):
    db_issue = models.Issue(**issue.dict())
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue

@router.delete("/issues/{issue_id}")
def delete_issue(issue_id: int, db: Session = Depends(get_db)):
    db_issue = db.query(models.Issue).filter(models.Issue.id == issue_id).first()
    if not db_issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    db.delete(db_issue)
    db.commit()
    return {"message": "Issue deleted"}

@router.get("/ladder", response_model=List[schemas.LadderEntry])
def get_ladder(exchange: str, issue: str, db: Session = Depends(get_db)):
    latest_timestamp = db.query(func.max(models.Snapshot.timestamp)).filter(
        models.Snapshot.exchange == exchange,
        models.Snapshot.issue == issue
    ).scalar()
    
    if not latest_timestamp:
        return []
        
    results = db.query(
        models.Snapshot.price,
        func.sum(models.Snapshot.quantity).label("quantity")
    ).filter(
        models.Snapshot.exchange == exchange,
        models.Snapshot.issue == issue,
        models.Snapshot.timestamp == latest_timestamp
    ).group_by(models.Snapshot.price).order_by(models.Snapshot.price.desc()).all()
    
    return results

@router.get("/combined", response_model=List[schemas.CombinedLadderEntry])
def get_combined_ladder(issue: str, investor_type: str = "NON_RETAIL", db: Session = Depends(get_db)):
    # Simple combined ladder implementation
    latest_timestamp_nse = db.query(func.max(models.Snapshot.timestamp)).filter(
        models.Snapshot.exchange == "NSE", 
        models.Snapshot.issue == issue,
        models.Snapshot.investor_type == investor_type
    ).scalar()
    
    latest_timestamp_bse = db.query(func.max(models.Snapshot.timestamp)).filter(
        models.Snapshot.exchange == "BSE", 
        models.Snapshot.issue == issue,
        models.Snapshot.investor_type == investor_type
    ).scalar()
    

    latest_snapshots = db.query(models.Snapshot).filter(
        models.Snapshot.issue == issue,
        models.Snapshot.investor_type == investor_type,
        ((models.Snapshot.exchange == "NSE") & (models.Snapshot.timestamp == latest_timestamp_nse)) |
        ((models.Snapshot.exchange == "BSE") & (models.Snapshot.timestamp == latest_timestamp_bse))
    ).all()

    combined_data = {}
    for s in latest_snapshots:
        if s.price not in combined_data:
            combined_data[s.price] = {
                "price": s.price,
                "nse_quantity": 0,
                "bse_quantity": 0,
                "total_quantity": 0,
                "bids": 0,
                "confirmed_qty": 0,
                "unconfirmed_qty": 0
            }
        
        if s.exchange == "NSE":
            combined_data[s.price]["nse_quantity"] += s.quantity
        else:
            combined_data[s.price]["bse_quantity"] += s.quantity
            
        combined_data[s.price]["total_quantity"] += s.quantity
        combined_data[s.price]["bids"] += s.bids
        combined_data[s.price]["confirmed_qty"] += s.confirmed_qty
        combined_data[s.price]["unconfirmed_qty"] += s.unconfirmed_qty

    sorted_prices = sorted(combined_data.keys(), reverse=True)
    
    ladder = []
    cum_total = 0
    cum_conf = 0
    cum_unc = 0
    
    for price in sorted_prices:
        data = combined_data[price]
        cum_total += data["total_quantity"]
        cum_conf += data["confirmed_qty"]
        cum_unc += data["unconfirmed_qty"]
        
        ladder.append(schemas.CombinedLadderEntry(
            price=price,
            nse_quantity=data["nse_quantity"],
            bse_quantity=data["bse_quantity"],
            total_quantity=data["total_quantity"],
            bids=data["bids"],
            confirmed_qty=data["confirmed_qty"],
            unconfirmed_qty=data["unconfirmed_qty"],
            cumulative_total=cum_total,
            cumulative_confirmed=cum_conf,
            cumulative_unconfirmed=cum_unc
        ))
        
    return ladder

@router.get("/history", response_model=List[schemas.Aggregate])
def get_history(exchange: str, issue: str, limit: int = 100, db: Session = Depends(get_db)):
    # Returns latest aggregates
    return db.query(models.Aggregate).filter(
        models.Aggregate.exchange == exchange
    ).order_by(models.Aggregate.timestamp.desc()).limit(limit).all()

@router.get("/analytics", response_model=schemas.AnalyticsResponse)
def get_analytics(issue: str, exchange: str = "BOTH", db: Session = Depends(get_db)):
    query = db.query(models.Snapshot).filter(models.Snapshot.issue == issue)
    
    if exchange != "BOTH":
        query = query.filter(models.Snapshot.exchange == exchange)
        
    latest_timestamp = db.query(func.max(models.Snapshot.timestamp)).filter(models.Snapshot.issue == issue).scalar()
    
    if not latest_timestamp:
        return schemas.AnalyticsResponse(
            weighted_average=0, highest_bid=0, lowest_bid=0, total_quantity=0, cumulative_demand=[]
        )
        
    snapshots = query.filter(models.Snapshot.timestamp == latest_timestamp).all()
    
    if not snapshots:
        return schemas.AnalyticsResponse(
            weighted_average=0, highest_bid=0, lowest_bid=0, total_quantity=0, cumulative_demand=[]
        )
        
    total_qty = sum(s.quantity for s in snapshots)
    weighted_sum = sum(s.quantity * s.price for s in snapshots)
    wa = weighted_sum / total_qty if total_qty > 0 else 0
    highest = max(s.price for s in snapshots)
    lowest = min(s.price for s in snapshots)
    
    # Cumulative demand
    price_groups = {}
    for s in snapshots:
        price_groups[s.price] = price_groups.get(s.price, 0) + s.quantity
        
    sorted_prices = sorted(price_groups.keys(), reverse=True)
    cumulative = []
    running_total = 0
    for p in sorted_prices:
        running_total += price_groups[p]
        cumulative.append({"price": p, "cumulative_quantity": running_total})
        
    return schemas.AnalyticsResponse(
        weighted_average=wa,
        highest_bid=highest,
        lowest_bid=lowest,
        total_quantity=total_qty,
        cumulative_demand=cumulative
    )

@router.get("/timeseries", response_model=List[schemas.TimeSeriesResponse])
def get_timeseries(issue: str, exchange: str = "BOTH", db: Session = Depends(get_db)):
    query = db.query(
        models.Snapshot.timestamp,
        models.Snapshot.price,
        func.sum(models.Snapshot.quantity).label("quantity")
    ).filter(models.Snapshot.issue == issue)
    
    if exchange != "BOTH":
        query = query.filter(models.Snapshot.exchange == exchange)
        
    return query.group_by(models.Snapshot.timestamp, models.Snapshot.price).order_by(models.Snapshot.timestamp.asc()).all()
