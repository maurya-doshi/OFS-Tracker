from curl_cffi.requests import AsyncSession
import logging
from typing import List
from datetime import datetime
from schemas.schemas import SnapshotBase
import asyncio

logger = logging.getLogger(__name__)

async def fetch_bse(scripcodes: dict) -> List[SnapshotBase]:
    results = []
    now = datetime.now()
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.bseindia.com/",
        "Origin": "https://www.bseindia.com"
    }

    async with AsyncSession(impersonate="chrome", headers=headers, timeout=15) as client:
        for scrip, symbol in scripcodes.items():
            # Non-Retail
            try:
                resp_nr = await client.get("https://api.bseindia.com/BseIndiaAPI/api/bsebidofs_details/w", params={"scripcode": scrip, "strflag": "NR"})
                resp_nr.raise_for_status()
                if not resp_nr.text.startswith('<'):
                    data = resp_nr.json()
                    items = data.get("Table", []) if isinstance(data, dict) else data
                    if isinstance(items, list):
                        for item in items:
                            raw_price = item.get("OE_PRICE", item.get("Price", item.get("BID_PRICE", 0)))
                            price = 0.0 if str(raw_price).lower() == "cut-off" else float(raw_price)
                            results.append(SnapshotBase(
                                exchange="BSE", issue=symbol, investor_type="NON_RETAIL",
                                price=price, quantity=int(item.get("TOTAL_QTY", item.get("Quantity", item.get("QUANTITY", 0)))),
                                bids=int(item.get("BIDS", 1)), confirmed_qty=int(item.get("CONFIRMEDQTY", item.get("TOTAL_QTY", 0))),
                                unconfirmed_qty=int(item.get("UNC_QTY", 0)), timestamp=now
                            ))
            except Exception as e:
                logger.error(f"Error fetching BSE Non-Retail for scrip {scrip}: {e}")

            # Retail
            try:
                resp_r = await client.get("https://api.bseindia.com/BseIndiaAPI/api/bsebidofsT_details/w", params={"scripcode": scrip, "strFlag": "R", "flag": "T2"})
                resp_r.raise_for_status()
                if not resp_r.text.startswith('<'):
                    data = resp_r.json()
                    items = data.get("Table", []) if isinstance(data, dict) else data
                    if isinstance(items, list):
                        for item in items:
                            raw_price = item.get("OE_PRICE", item.get("Price", item.get("BID_PRICE", 0)))
                            price = 0.0 if str(raw_price).lower() == "cut-off" else float(raw_price)
                            results.append(SnapshotBase(
                                exchange="BSE", issue=symbol, investor_type="RETAIL",
                                price=price, quantity=int(item.get("TOTAL_QTY", item.get("Quantity", item.get("QUANTITY", 0)))),
                                bids=int(item.get("BIDS", 1)), confirmed_qty=int(item.get("CONFIRMEDQTY", item.get("TOTAL_QTY", 0))),
                                unconfirmed_qty=int(item.get("UNC_QTY", 0)), timestamp=now
                            ))
            except Exception as e:
                logger.error(f"Error fetching BSE Retail for scrip {scrip}: {e}")

    return results
