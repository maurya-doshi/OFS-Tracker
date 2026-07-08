import httpx
import logging
from typing import List, Optional
from datetime import datetime
from app.collectors.base import BaseCollector
from app.schemas.schemas import SnapshotBase
from app.config import settings

logger = logging.getLogger(__name__)

class BSECollector(BaseCollector):
    def __init__(self, scripcodes: dict = None):
        super().__init__()
        self.exchange = "BSE"
        self.base_url = "https://api.bseindia.com/BseIndiaAPI/api/bsebidofs_details/w"
        # scripcodes is a dict of {scripcode: symbol}
        self.scripcodes = scripcodes or {}
        self.flags = ["NR", "R"] # Can be extended in config or dynamically
        self.headers = {
            "User-Agent": settings.USER_AGENT,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.bseindia.com/",
            "Origin": "https://www.bseindia.com"
        }
        self.client = httpx.AsyncClient(headers=self.headers, timeout=15.0)

    async def fetch(self) -> dict:
        results = {}
        for scrip, symbol in self.scripcodes.items():
            results[scrip] = {"NON_RETAIL": None, "RETAIL": None}
            
            # Non-Retail
            try:
                params_nr = {"scripcode": scrip, "strflag": "NR"}
                resp_nr = await self.client.get(self.base_url, params=params_nr)
                resp_nr.raise_for_status()
                # Use a basic check to prevent parsing empty/HTML
                if resp_nr.text.startswith('<'):
                    raise Exception("Received HTML instead of JSON")
                results[scrip]["NON_RETAIL"] = resp_nr.json()
            except Exception as e:
                logger.error(f"Error fetching BSE Non-Retail for scrip {scrip}: {e}")

            # Retail (different endpoint base conceptually but we can just use the provided full url params)
            try:
                url_r = "https://api.bseindia.com/BseIndiaAPI/api/bsebidofsT_details/w"
                params_r = {"scripcode": scrip, "strFlag": "R", "flag": "T2"}
                resp_r = await self.client.get(url_r, params=params_r)
                resp_r.raise_for_status()
                if resp_r.text.startswith('<'):
                    raise Exception("Received HTML instead of JSON")
                results[scrip]["RETAIL"] = resp_r.json()
            except Exception as e:
                logger.error(f"Error fetching BSE Retail for scrip {scrip}: {e}")

        return results

    def normalize(self, raw_data: dict) -> List[SnapshotBase]:
        snapshots = []
        now = datetime.now()
        
        for scrip, inv_data in raw_data.items():
            for inv_type, data in inv_data.items():
                if not data:
                    continue
                    
                items = data.get("Table", []) if isinstance(data, dict) else data
                if not isinstance(items, list):
                    continue
                    
                for item in items:
                    try:
                        raw_price = item.get("OE_PRICE", item.get("Price", item.get("BID_PRICE", 0)))
                        if isinstance(raw_price, str) and raw_price.lower() == "cut-off":
                            price = 0.0
                        else:
                            price = float(raw_price)
                            
                        quantity = int(item.get("TOTAL_QTY", item.get("Quantity", item.get("QUANTITY", 0))))
                        bids = int(item.get("BIDS", 1))
                        confirmed_qty = int(item.get("CONFIRMEDQTY", quantity))
                        unconfirmed_qty = int(item.get("UNC_QTY", 0))
                        symbol = self.scripcodes.get(scrip, str(scrip))
                        
                        # Category can just map to inv_type conceptually, or retain old logic
                        category = "NR" if inv_type == "NON_RETAIL" else "R"
                        
                        snapshots.append(SnapshotBase(
                            exchange=self.exchange,
                            issue=symbol,
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
                        logger.warning(f"Failed to parse BSE record {item}: {e}")
                        continue
                        
        return snapshots
