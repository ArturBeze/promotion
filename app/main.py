import time
import requests
import os

URL = os.getenv("TARGET_URL", "https://example.com")
INTERVAL = int(os.getenv("INTERVAL", 60))

session = requests.Session()

while True:
    try:
        response = session.get(URL, timeout=10)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] "
              f"Status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(INTERVAL)
