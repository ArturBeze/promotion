FROM python:3.12-slim

# Установим зависимости для Playwright и Xvfb
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    xvfb \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    fonts-liberation \
    libwoff1 \
    && rm -rf /var/lib/apt/lists/*

# Установим Python-зависимости
RUN pip install --no-cache-dir playwright

# Установим движки Playwright
RUN playwright install

WORKDIR /app
COPY . /app

# Команда по умолчанию
CMD ["python", "main.py"]
