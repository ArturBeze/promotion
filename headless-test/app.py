import os
import sys
import time
import socket
from datetime import datetime
from playwright.sync_api import sync_playwright


def log(message: str) -> None:
    hostname = socket.gethostname()
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] [{hostname}] {message}", flush=True)


def main() -> int:
    url = "https://example.com"

    log("Container started")
    log(f"Python executable: {sys.executable}")
    log(f"PID: {os.getpid()}")
    log(f"Target URL: {url}")

    try:
        with sync_playwright() as p:
            log("Launching Chromium...")
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                ],
            )

            page = browser.new_page()
            log("Opening page...")
            page.goto(url, wait_until="domcontentloaded", timeout=30000)

            title = page.title()
            log(f"Page title: {title}")

            browser.close()
            log("Browser closed")
    except Exception as exc:
        log(f"ERROR: {exc}")
        return 1

    log("Sleeping for 30 seconds so logs/container are easy to inspect...")
    time.sleep(30)

    log("Done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())