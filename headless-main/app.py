import os
import sys
import time
import socket
import uuid
import json
import random
from datetime import datetime
from playwright.sync_api import sync_playwright

# URL = "https://yandex.ru/games/app/288720"
# URL = "https://yandex.ru/games/app/240023?lang=ru"
# URL = "https://yandex.ru/games/app/274358?lang=ru"
URL = "https://yandex.ru/games/app/503306?lang=ru"

COOKIES_FILE = "cookies.json"
SCREEN_DIR = "screenshots"
ID_FILE = ".container_id"

def show_click(page, x, y, color="red"):
    page.evaluate(
        """({x, y, color}) => {
            const dot = document.createElement('div');
            dot.style.position = 'fixed';
            dot.style.left = x + 'px';
            dot.style.top = y + 'px';
            dot.style.width = '12px';
            dot.style.height = '12px';
            dot.style.background = color;
            dot.style.borderRadius = '50%';
            dot.style.zIndex = 999999;
            dot.style.pointerEvents = 'none';
            dot.style.transform = 'translate(-50%, -50%)';
            document.body.appendChild(dot);

            setTimeout(() => dot.remove(), 1000);
        }""",
        {"x": x, "y": y, "color": color},
    )

def load_cookies(context):
    if os.path.exists(COOKIES_FILE):
        with open(COOKIES_FILE, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        context.add_cookies(cookies)
        print("🍪 Cookies загружены")

def save_cookies(context):
    cookies = context.cookies()
    with open(COOKIES_FILE, "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    print("🍪 Cookies сохранены")

def log(message: str) -> None:
    hostname = socket.gethostname()
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] [{hostname}] {message}", flush=True)


def main() -> int:
    print("Start --->")
    print("New --->")

    if os.path.exists(ID_FILE):
        with open(ID_FILE) as f:
            cid = f.read().strip()
            print(f"🍪 ID загружен {cid}")
    else:
        cid = str(uuid.uuid4())
        print(f"🍪 ID создан {cid}")
        with open(ID_FILE, "w") as f:
            f.write(cid)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,  # для докера
                # headless=False, # для браузера
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                    "--disable-setuid-sandbox"
                ]
            )

            context = browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                locale="ru-RU"
            )

            load_cookies(context)

            page = context.new_page()
            # page.goto(URL, wait_until="networkidle", timeout=60000)
            page.goto(URL, wait_until="domcontentloaded", timeout=60000)
            # page.goto(URL)

            print("Страница загружена")

            page.wait_for_timeout(5000)

            if not os.path.exists(COOKIES_FILE):
                play_button = page.locator('button[data-guard-accept="play_button"]')
                if play_button.count() > 0:
                    play_button.click(timeout=5000)

            time.sleep(3)

            save_cookies(context)

            time.sleep(6)

            fullscreen_btn = page.locator('[data-testid="yandex-fullscreen-render-button"]')
            # fullscreen_btn.wait_for(state="visible")
            # fullscreen_btn.click()

            if fullscreen_btn.is_visible():
                fullscreen_btn.first.click()
                print("Кнопка фуллскрина нажата")
            else:
                print("Кнопки нет, идём дальше")

            time.sleep(3)

            # container_id = os.getenv("HOSTNAME", "unknown_container")
            container_id = cid

            ############################################################################
            frame = page.frame_locator('#game-frame')
            canvas = frame.locator("canvas")
            box = canvas.bounding_box()
            print(box)

            show_click(page, box["width"] / 2 + box["x"], box["height"] / 2 + box["y"])
            page.mouse.click(box["width"] / 2 + box["x"], box["height"] / 2 + box["y"])

            time.sleep(3)
            ############################################################################

            fullscreen_btn = page.locator('[data-testid="yandex-fullscreen-render-button"]')

            if fullscreen_btn.is_visible():
                fullscreen_btn.first.click()
                print("Кнопка фуллскрина нажата")
            else:
                print("Кнопки нет, идём дальше")

            time.sleep(6)

            ############################################################################
            frame = page.frame_locator('#game-frame')
            canvas = frame.locator("canvas")
            box = canvas.bounding_box()
            print(box)

            show_click(page, box["width"] / 2 + box["x"] + 200, box["height"] / 2 + box["y"] + 160)
            page.mouse.click(box["width"] / 2 + box["x"] + 200, box["height"] / 2 + box["y"] + 160)

            time.sleep(3)
            ############################################################################

            i = 0
            while True:
                page.keyboard.press('KeyA')

                filename = f"{SCREEN_DIR}/{container_id}/screenshot_{i}.png"
                page.screenshot(path=filename)
                print(f"Скриншот сохранён: {filename}")
                i += 1
                time.sleep(12.2)

                fullscreen_btn = page.locator('[data-testid="yandex-fullscreen-render-button"]')

                # if fullscreen_btn.count() > 0:
                # if fullscreen_btn.count():
                if fullscreen_btn.is_visible():
                    fullscreen_btn.first.click()
                    print("Кнопка фуллскрина нажата")
                else:
                    print("Кнопки нет, идём дальше")

                    dx = random.uniform(-100, 100)
                    dy = random.uniform(-100, 100)

                    show_click(page, box["width"] / 2 + box["x"] + dx, box["height"] / 2 + box["y"] + dy)
                    page.mouse.click(box["width"] / 2 + box["x"] + dx, box["height"] / 2 + box["y"] + dy)

    except Exception as exc:
        log(f"ERROR: {exc}")
        return 1

    log("Sleeping for 30 seconds so logs/container are easy to inspect...")
    time.sleep(30)

    log("Done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())