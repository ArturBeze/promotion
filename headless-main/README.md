docker compose up -d --build --scale scraper=5
docker compose -p mygroup up -d --build --scale scraper=5

docker build -t my-app .
docker run -v $(pwd)/screenshots:/app/screenshots my-app
docker run -v ${PWD}/screenshots:/app/screenshots my-app
