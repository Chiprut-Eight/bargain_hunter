"""
Find correct Gov.il API parameters using requests with a session.
"""
import requests, json

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Referer': 'https://www.gov.il/'
})

BASE = "https://www.gov.il/he/api/PublicationApi/Index"

def search(label, **params):
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{BASE}?{qs}"
    r = session.get(url, timeout=15)
    if r.status_code == 200:
        data = r.json()
        total = data.get('total', 0)
        results = data.get('results', [])
        print(f"\n=== {label} === total: {total}")
        for item in results[:5]:
            print(f"  [{item.get('PubDate','')[:10]}] {str(item.get('Title',''))[:60]}")
            print(f"    OfficeId={item.get('OfficeId')} Topic={item.get('Topic')}")
    else:
        print(f"\n=== {label} === HTTP {r.status_code}")

# Generic
search("All publications (no filter)", Skip=0, Limit=5)

# call_for_bids
search("PublicationType=call_for_bids", Skip=0, Limit=10, PublicationType="call_for_bids")

# keyword searches (URL encoded Hebrew)
import urllib.parse
search("Query=מכס", Skip=0, Limit=5, Query=urllib.parse.quote("מכס"))
search("Query=כונס", Skip=0, Limit=5, Query=urllib.parse.quote("כונס"))
search("Query=מכרז", Skip=0, Limit=5, Query=urllib.parse.quote("מכרז"))
search("Query=פומבי", Skip=0, Limit=5, Query=urllib.parse.quote("פומבי"))
