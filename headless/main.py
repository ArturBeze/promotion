import asyncio
from playwright.async_api import async_playwright
import os


async def main():
	# Запуск Xvfb через команду в Docker
	display = os.environ.get("DISPLAY", ":99")
	os.system(f"Xvfb {display} -screen 0 1920x1080x24 &")

	async with async_playwright() as p:
		# Запускаем Chromium в headless=False, чтобы Xvfb "видел" окно
		browser = await p.chromium.launch(headless=False)
		context = await browser.new_context()
		page = await context.new_page()

		# Открываем страницу с iframe
		await page.goto("http://example.com/page-with-iframe")

		# Получаем iframe
		frame = page.frame(name="game_frame")  # или по селектору: page.frame_locator("iframe#game")

		if frame:
			# Пример: клик по кнопке внутри iframe
			await frame.click("#startButton")

			# Пример: ввод текста
			await frame.fill("#nameInput", "Player1")

			# Делаем паузу, чтобы увидеть действие
			await asyncio.sleep(5)
		else:
			print("Iframe не найден!")

		await browser.close()


asyncio.run(main())
