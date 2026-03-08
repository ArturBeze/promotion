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
    # url = "https://example.com"
    url = "https://yandex.ru/games/app/503306?lang=ru"

    log("Container started")
    log(f"Python executable: {sys.executable}")
    log(f"PID: {os.getpid()}")
    log(f"Target URL: {url}")

    try:
        with sync_playwright() as p:
            log("Launching Chromium...")
            browser = p.chromium.launch(
                channel="chrome",
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                    "--disable-setuid-sandbox"
                ],
            )
            # page = browser.new_page()

            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 720},
                locale="ru-RU"
            )
            page = context.new_page()

            log("Opening page...")
            page.goto(url, wait_until="domcontentloaded", timeout=30000)

            log("Take a shot...")
            filename = f"screenshots/test_screenshot.png"
            page.screenshot(path=filename)

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