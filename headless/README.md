docker build -t playwright-xvfb .
docker run -d -it --rm playwright-xvfb

docker compose build
docker compose up -d