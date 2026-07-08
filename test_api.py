import asyncio
import httpx
import json

async def fetch_api(client, url, name):
    print(f"\n--- Fetching {name} ---")
    try:
        resp = await client.get(url)
        print("Status:", resp.status_code)
        if resp.status_code == 200:
            text = resp.text
            if text.startswith('<'):
                print("Received HTML, length:", len(text))
                return
            try:
                data = resp.json()
                print("JSON parsed successfully")
                
                # Try to search for "cut-off" or "cutoff" recursively
                def find_cutoff(obj, path=""):
                    if isinstance(obj, dict):
                        for k, v in obj.items():
                            if isinstance(v, str) and "cut-off" in v.lower():
                                print(f"Found cut-off string in {path}.{k} = {v}")
                            elif "cut-off" in k.lower() or "cutoff" in k.lower():
                                print(f"Found cut-off key {path}.{k} = {v}")
                            else:
                                find_cutoff(v, f"{path}.{k}")
                    elif isinstance(obj, list):
                        for i, v in enumerate(obj):
                            find_cutoff(v, f"{path}[{i}]")

                find_cutoff(data)
                
            except Exception as e:
                print("Failed to parse JSON:", e, "Text snippet:", text[:100])
    except Exception as e:
        print("Error fetching:", e)


async def test_apis():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Origin": "https://www.bseindia.com",
        "Referer": "https://www.bseindia.com/"
    }
    
    async with httpx.AsyncClient(headers=headers, timeout=15.0) as client:
        # Get cookies
        await client.get("https://www.nseindia.com")
        await client.get("https://www.bseindia.com")
        
        symbol = "COCHINSHIP"
        scripcode = "540678"
        date_str_non_retail = "07-Jul-2026"
        date_str_retail = "08-Jul-2026"
        
        # Retail (Day 2) summary/details?
        nse_retail = f"https://www.nseindia.com/api/ofs-activeissues-dr?symbol={symbol}&offerdate={date_str_retail}"
        bse_retail = f"https://api.bseindia.com/BseIndiaAPI/api/bsebidofsT_details/w?scripcode={scripcode}&strFlag=R&flag=T2"
        
        await fetch_api(client, nse_retail, "NSE Retail")
        await asyncio.sleep(0.5)
        await fetch_api(client, bse_retail, "BSE Retail")

if __name__ == "__main__":
    asyncio.run(test_apis())
