from playwright.sync_api import sync_playwright
import time
import os

STATE_FILE = "state.json"

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

def handler():
    page.evaluate("""
    () => {
        if (document.getElementById('resume-btn')) return;

        const btn = document.createElement('button');
        btn.id = 'resume-btn';
        btn.innerText = '▶ Продолжить (U)';
        btn.style = `
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 99999;
            padding: 10px;
            font-size: 16px;
        `;
        document.body.appendChild(btn);

        window.__resumeAutomation = false;

        btn.onclick = () => {
            window.__resumeAutomation = true;
        };

        document.addEventListener('keydown', e => {
            if (e.key.toLowerCase() === 'u') {
                window.__resumeAutomation = true;
            }
        });
    }
    """)



with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        slow_mo=50,
        args=[
            "--use-gl=swiftshader",
            "--enable-webgl",
            "--disable-web-security",
            "--disable - gpu",
        ]
    )

    if os.path.exists(STATE_FILE):
        print("🔁 Загружаем cookies из файла")
        context = browser.new_context(storage_state=STATE_FILE)
    else:
        print("🆕 Файла нет — создаем новый контекст")
        context = browser.new_context()

    page = context.new_page()

    # page.goto("http://localhost:8000/game/")
    page.goto("https://yandex.ru/games/app/288720")
    # page.goto("https://yandex.ru/games/app/393853")

    page.wait_for_timeout(5000)

    handler()

    if not os.path.exists(STATE_FILE):
        play_button = page.locator('button[data-guard-accept="play_button"]')
        play_button.click()

    time.sleep(3)

    fullscreen_btn = page.locator('[data-testid="yandex-fullscreen-render-button"]')
    fullscreen_btn.wait_for(state="visible")
    fullscreen_btn.click()

    time.sleep(3)

    frame = page.frame_locator('#game-frame')

    page.screenshot(path="frame.png")

    canvas = frame.locator("canvas")
    box = canvas.bounding_box()
    print(box)

    click_x = box["width"] / 2 + box["x"]
    click_y = box["height"] / 2 + box["y"]

    show_click(page, click_x, click_y)
    canvas.click(position={"x": click_x, "y": click_y})

    time.sleep(3)

    for _ in range(10):
        show_click(page, box["width"] / 2 + box["x"], box["height"] / 2 + box["y"])
        page.mouse.click(box["width"] / 2 + box["x"], box["height"] / 2 + box["y"])

        page.keyboard.press('KeyA')

        time.sleep(.25)

    print("🔴 Ручной режим: кнопка или клавиша U")

    # handler()
    page.wait_for_function("() => window.__resumeAutomation === true", timeout = 0)

    print("🟢 Автоматизация продолжается")

    context.storage_state(path=STATE_FILE)

    browser.close()