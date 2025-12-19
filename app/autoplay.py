from playwright.sync_api import sync_playwright
import time

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

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        slow_mo=50,
        args=[
            "--use-gl=swiftshader",
            "--enable-webgl",
            "--disable-web-security",
        ]
    )

    page = browser.new_page()

    # page.goto("http://localhost:8000/game/")
    page.goto("https://yandex.ru/games/app/413034")

    page.wait_for_timeout(2000)

    page.wait_for_selector("iframe", timeout=60000)

    frame = page.frame_locator("iframe")

    time.sleep(2)

    # canvas = frame.locator("canvas")
    # box = canvas.bounding_box()
    # # print(box)
    #
    # click_x = box["width"] / 2 + box["x"]
    # click_y = box["height"] / 2 + box["y"]
    #
    # show_click(page, click_x, click_y)
    # canvas.click(position={"x": click_x, "y": click_y})
    #
    # time.sleep(1)
    #
    # for _ in range(10):
    #     show_click(page, box["width"] / 2 + box["x"], box["height"] / 2 + box["y"])
    #     page.mouse.click(box["width"] / 2 + box["x"], box["height"] / 2 + box["y"])
    #
    #     time.sleep(.25)

    browser.close()









    # # page.goto("https://example.com/game")
    #
    # # Дать игре загрузиться
    # page.wait_for_timeout(5000)
    #
    # # Клик в canvas (фокус)
    # page.mouse.click(600, 400)
    #
    # # Нажать W (движение вперёд)
    # page.keyboard.down("w")
    # time.sleep(2)
    # page.keyboard.up("w")
    #
    # # Прыжок
    # page.keyboard.press("Space")
    #
    # # Поворот мыши
    # page.mouse.move(700, 400)
    # page.mouse.move(800, 400)