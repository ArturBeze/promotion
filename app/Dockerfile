# Dockerfile
FROM python:3.13-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    wget curl unzip xvfb libnss3 libatk1.0-0 libatk-bridge2.0-0 libx11-xcb1 libxcomposite1 \
    libxdamage1 libxrandr2 libgbm1 libasound2 libcups2 libxss1 libpangocairo-1.0-0 libpango-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Установка Playwright
RUN pip install playwright
RUN playwright install

# Копируем твой скрипт
WORKDIR /app
COPY . /app

# Команда запуска с виртуальным дисплеем
CMD ["bash", "-c", "xvfb-run --auto-servernum python autoplay.py"]