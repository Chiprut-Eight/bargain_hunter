import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

def test_api(url, name):
    print(f"\n--- Testing API for {name} ---")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.gov.il/he/departments/publications/'
    }
    try:
        res = requests.get(url, headers=headers)
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            data = res.json()
            if "results" in data:
                print(f"Found {len(data['results'])} items.")
                for item in data['results'][:3]:
                    title = item.get('Title', 'No Title')
                    print(f"- {title}")
            elif "Results" in data:
                print(f"Found {len(data['Results'])} items.")
                for item in data['Results'][:3]:
                    print(f"- {item.get('Title')}")
            else:
                print("Keys:", data.keys())
        else:
            print(res.text[:200])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api("https://www.gov.il/he/api/PublicationApi/Index?Skip=0&Limit=10&OfficeId=b723f1dd-b541-4cfd-82d2-c48c9bef4187", "Official Receiver")
    test_api("https://www.gov.il/he/api/PublicationApi/Index?Skip=0&Limit=10&Topic=customs-auctions", "Tax Authority")
