###Promotion

Установка кластера
# Linux
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube

# macOS
    brew install minikube

# Windows
    choco install minikube

Старт

    minikube start --cpus=4 --memory=2048

Статус

    minikube status

Стоп

    minikube delete

Собираем образ

    docker build -t my-python-app:latest ./main

Запуск

    kubectl apply -f k8s/deployment.yaml

Проверка

    kubectl get nodes
    kubectl get pods

Масштабирование до 100 контейнеров

    kubectl scale deployment python-workers --replicas=100

Проверка

    kubectl get pods | wc -l

Остановка

    kubectl scale deployment python-workers --replicas=0
