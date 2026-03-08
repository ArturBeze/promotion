# FROM mcr.microsoft.com/playwright/python:v1.52.0-jammy
FROM mcr.microsoft.com/playwright/python:v1.58.0-jammy
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps chrome

COPY app.py .

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "xvfb-run -a python -u app.py"]