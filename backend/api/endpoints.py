from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import timezone
from database.database import get_db
from models import models
from schemas import schemas

router = APIRouter()

@router.get("/issues", response_model=List[schemas.Issue])
def get_issues(db: Session = Depends(get_db)):
    return db.query(models.Issue).all()

@router.post("/issues", response_model=schemas.Issue)
def create_issue(issue: schemas.IssueBase, db: Session = Depends(get_db)):
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

@router.get("/combined", response_model=schemas.CombinedLadderResponse)
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

    # Attach UTC timezone info so the frontend can reliably convert to any tz
    def utc(ts):
        return ts.replace(tzinfo=timezone.utc) if ts else None
        
    return schemas.CombinedLadderResponse(
        nse_last_updated=utc(latest_timestamp_nse),
        bse_last_updated=utc(latest_timestamp_bse),
        ladder=ladder
    )

