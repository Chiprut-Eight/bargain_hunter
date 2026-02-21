import requests

url = "https://apps.land.gov.il/MichrazimSite/api/MichrazimApi/Search"
payload = {
    "michrazType": 1,
    "status": 1 # 1 is usually active
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

try:
    print("Fetching RAMI API...")
    res = requests.post(url, json=payload, headers=headers, timeout=10)
    print("Status:", res.status_code)
    print("Response:", res.text[:500])
except Exception as e:
    print("Error:", e)
