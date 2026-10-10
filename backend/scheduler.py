import logging
import asyncio
import os
from database.database import SessionLocal
from models import models
from collectors.nse import fetch_nse
from collectors.bse import fetch_bse

logger = logging.getLogger(__name__)

async def poll_exchanges():
    logger.info("Starting polling cycle")
    db = SessionLocal()
    try:
        active_issues = db.query(models.Issue).filter(models.Issue.status == "ACTIVE").all()
        nse_symbols = [i.symbol for i in active_issues if i.symbol]
        bse_scripcodes = {i.scripcode: i.symbol for i in active_issues if i.scripcode}
        
        nse_snapshots = await fetch_nse(nse_symbols)
        bse_snapshots = await fetch_bse(bse_scripcodes)
        
        all_snapshots = nse_snapshots + bse_snapshots
        
        if not all_snapshots:
            logger.info("No snapshots collected.")
            return

        snapshot_records = [models.Snapshot(**s.model_dump()) for s in all_snapshots]
        db.bulk_save_objects(snapshot_records)
        db.commit()

        logger.info(f"Polling cycle completed. Stored {len(snapshot_records)} snapshots.")
    except Exception as e:
        logger.error(f"Error during polling cycle: {e}")
    finally:
        db.close()

_scheduler_task = None

async def _scheduler_loop(interval: int):
    while True:
        await poll_exchanges()
        await asyncio.sleep(interval)

def start_scheduler():
    global _scheduler_task
    interval = int(os.environ.get("POLL_INTERVAL", 15))
    loop = asyncio.get_running_loop()
    _scheduler_task = loop.create_task(_scheduler_loop(interval))
    logger.info(f"Scheduler started natively with {interval} seconds interval.")

def shutdown_scheduler():
    global _scheduler_task
    if _scheduler_task and not _scheduler_task.done():
        _scheduler_task.cancel()
        logger.info("Scheduler shut down.")

