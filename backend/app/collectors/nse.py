import httpx
import logging
from typing import List
from datetime import datetime
from app.collectors.base import BaseCollector
from app.schemas.schemas import SnapshotBase
from app.config import settings
import asyncio

logger = logging.getLogger(__name__)

class NSECollector(BaseCollector):
    def __init__(self, symbols: List[str] = None):
        super().__init__()
        self.exchange = "NSE"
        self.base_url = "https://www.nseindia.com"
        self.symbols = symbols or []
        self.headers = {
            "User-Agent": settings.USER_AGENT,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.nseindia.com/",
        }
        self.client = httpx.AsyncClient(headers=self.headers, timeout=15.0)

    async def fetch(self) -> dict:
        results = {}
        now = datetime.now()
        date_str = now.strftime("%d-%b-%Y") # e.g. 07-Jul-2026
        
        try:
            # Fetch base URL to get cookies
            await self.client.get(self.base_url)
        except Exception as e:
            logger.error(f"Error fetching NSE base URL for cookies: {e}")
            
        for symbol in self.symbols:
            results[symbol] = {"NON_RETAIL": None, "RETAIL": None}
            # Non-Retail
            try:
                url_nr = f"https://www.nseindia.com/api/ofs-activeissues-dd?symbol={symbol}&offerdate={date_str}"
                response_nr = await self.client.get(url_nr)
                response_nr.raise_for_status()
                results[symbol]["NON_RETAIL"] = response_nr.json()
            except Exception as e:
                logger.error(f"Error fetching NSE Non-Retail for {symbol}: {e}")
                
            await asyncio.sleep(0.5)
            
            # Retail
            try:
                url_r = f"https://www.nseindia.com/api/ofs-activeissues-dr?symbol={symbol}&offerdate={date_str}"
                response_r = await self.client.get(url_r)
                response_r.raise_for_status()
                results[symbol]["RETAIL"] = response_r.json()
            except Exception as e:
                logger.error(f"Error fetching NSE Retail for {symbol}: {e}")
                
            await asyncio.sleep(0.5)
        return results

    def normalize(self, raw_data: dict) -> List[SnapshotBase]:
        snapshots = []
        now = datetime.now()
        
        for symbol, inv_data in raw_data.items():
            for inv_type, data in inv_data.items():
                if not data:
                    continue
                
                items = data if isinstance(data, list) else data.get("data", []) if isinstance(data, dict) else []
                if not isinstance(items, list):
                    continue
    
                for item in items:
                    try:
                        raw_price = item.get("pri", 0)
                        if str(raw_price) == "-1" or (isinstance(raw_price, str) and raw_price.lower() == "cut-off"):
                            price = 0.0
                        else:
                            price = float(raw_price)
                            
                        quantity = int(item.get("totQty", 0))
                        bids = int(item.get("bids", 0))
                        confirmed_qty = int(item.get("conQty", 0))
                        unconfirmed_qty = int(item.get("uCQty", 0))
                        category = item.get("ser", "Unknown")
                        
                        snapshots.append(SnapshotBase(
                            exchange=self.exchange,
                            issue=str(symbol),
                            investor_type=inv_type,
                            category=category,
                            price=price,
                            quantity=quantity,
                            bids=bids,
                            confirmed_qty=confirmed_qty,
                            unconfirmed_qty=unconfirmed_qty,
                            timestamp=now
                        ))
                    except (ValueError, TypeError) as e:
                        logger.warning(f"Failed to parse NSE record {item}: {e}")
                        continue
                        
        return snapshots
