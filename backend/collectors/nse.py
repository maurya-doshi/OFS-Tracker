from curl_cffi.requests import AsyncSession
import logging
from typing import List
from datetime import datetime
from schemas.schemas import SnapshotBase
import asyncio

logger = logging.getLogger(__name__)

async def fetch_nse(symbols: List[str]) -> List[SnapshotBase]:
    results = []
    now = datetime.now()
    date_str = now.strftime("%d-%b-%Y")
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.nseindia.com/",
    }

    async with AsyncSession(impersonate="chrome", headers=headers, timeout=15) as client:
        try:
            await client.get("https://www.nseindia.com")
        except Exception as e:
            logger.error(f"Error fetching NSE base URL for cookies: {e}")
            
        for symbol in symbols:
            for inv_type, suffix in [("NON_RETAIL", "dd"), ("RETAIL", "dr")]:
                try:
                    url = f"https://www.nseindia.com/api/ofs-activeissues-{suffix}?symbol={symbol}&offerdate={date_str}"
                    resp = await client.get(url)
                    resp.raise_for_status()
                    data = resp.json()
                    
                    items = data if isinstance(data, list) else data.get("data", []) if isinstance(data, dict) else []
                    if not isinstance(items, list):
                        continue
                        
                    for item in items:
                        raw_price = item.get("pri", 0)
                        price = 0.0 if str(raw_price) == "-1" or str(raw_price).lower() == "cut-off" else float(raw_price)
                        results.append(SnapshotBase(
                            exchange="NSE",
                            issue=str(symbol),
                            investor_type=inv_type,
                            price=price,
                            quantity=int(item.get("totQty", 0)),
                            bids=int(item.get("bids", 0)),
                            confirmed_qty=int(item.get("conQty", 0)),
                            unconfirmed_qty=int(item.get("uCQty", 0)),
                            timestamp=now
                        ))
                except Exception as e:
                    logger.error(f"Error fetching NSE {inv_type} for {symbol}: {e}")
                
                await asyncio.sleep(0.5)
                
    return results
