import os
import uuid
import time
import json
from playwright.sync_api import sync_playwright

# URL = "https://yandex.ru/games/app/288720"
URL = "https://yandex.ru/games/app/240023?lang=ru"
COOKIES_FILE = "cookies.json"
SCREEN_DIR = "screenshots"
ID_FILE = ".container_id"

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



def main():
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

    with sync_playwright() as p:
        browser = p.chromium.launch(
            # headless=True,
            headless=False,
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
            play_button.click()

        time.sleep(3)

        save_cookies(context)

        time.sleep(3)

        fullscreen_btn = page.locator('[data-testid="yandex-fullscreen-render-button"]')
        fullscreen_btn.wait_for(state="visible")
        fullscreen_btn.click()

        time.sleep(3)

        # container_id = os.getenv("HOSTNAME", "unknown_container")
        container_id = cid

        i = 0
        while True:
            page.keyboard.press('KeyA')

            filename = f"{SCREEN_DIR}/{container_id}/screenshot_{i}.png"
            page.screenshot(path=filename)
            print(f"Скриншот сохранён: {filename}")
            i += 1
            time.sleep(2.2)



            fullscreen_btn = page.locator('[data-testid="yandex-fullscreen-render-button"]')

            # if fullscreen_btn.count() > 0:
            # if fullscreen_btn.count():
            if fullscreen_btn.is_visible():
                fullscreen_btn.first.click()
                print("Кнопка фуллскрина нажата")
            else:
                print("Кнопки нет, идём дальше")

if __name__ == "__main__":
    main()
