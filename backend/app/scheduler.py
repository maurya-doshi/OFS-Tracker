import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.config import settings
from app.database.database import SessionLocal
from app.models import models
from app.collectors.nse import NSECollector
from app.collectors.bse import BSECollector
from sqlalchemy import func

logger = logging.getLogger(__name__)

async def poll_exchanges():
    logger.info("Starting polling cycle")
    db = SessionLocal()
    try:
        # 1. Fetch active issues
        active_issues = db.query(models.Issue).filter(models.Issue.status == "ACTIVE").all()
        nse_symbols = [i.symbol for i in active_issues if i.symbol]
        bse_scripcodes = {i.scripcode: i.symbol for i in active_issues if i.scripcode}
        
        # 2. Fetch NSE
        nse_collector = NSECollector(symbols=nse_symbols)
        nse_snapshots = await nse_collector.collect()
        
        # 3. Fetch BSE
        bse_collector = BSECollector(scripcodes=bse_scripcodes)
        bse_snapshots = await bse_collector.collect()
        
        all_snapshots = nse_snapshots + bse_snapshots
        
        if not all_snapshots:
            logger.info("No snapshots collected.")
            return

        # 3. Validation & 4. Normalize (Handled in collectors)
        # 5. Store snapshot
        snapshot_records = []
        for s in all_snapshots:
            record = models.Snapshot(**s.model_dump())
            snapshot_records.append(record)
            
        db.bulk_save_objects(snapshot_records)
        db.commit()

        # 6. Update aggregates
        for s in all_snapshots:
            # Aggregate logic: aggregate quantities by price per exchange per timestamp
            pass
            
        # Simplistic aggregation: group by exchange, timestamp, price
        # Actually, we should aggregate everything we just fetched.
        from collections import defaultdict
        agg_map = defaultdict(int)
        for s in all_snapshots:
            key = (s.exchange, s.timestamp, s.price)
            agg_map[key] += s.quantity
            
        agg_records = []
        for (exc, ts, px), qty in agg_map.items():
            agg_records.append(models.Aggregate(
                timestamp=ts,
                exchange=exc,
                price=px,
                quantity=qty
            ))
            
        db.bulk_save_objects(agg_records)
        db.commit()

        # 7. Compute diff
        # Compare with previous snapshot
        # For simplicity, we can do this per exchange and price
        # skipping complex diff for now to keep it straightforward
        # or implement a basic version:
        
        logger.info(f"Polling cycle completed. Stored {len(snapshot_records)} snapshots and {len(agg_records)} aggregates.")

    except Exception as e:
        logger.error(f"Error during polling cycle: {e}")
    finally:
        db.close()

_scheduler = None

def start_scheduler():
    global _scheduler
    _scheduler = AsyncIOScheduler()
    _scheduler.add_job(poll_exchanges, 'interval', seconds=settings.POLL_INTERVAL)
    _scheduler.start()
    logger.info(f"Scheduler started with {settings.POLL_INTERVAL} seconds interval.")

def shutdown_scheduler():
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
        logger.info("Scheduler shut down.")

