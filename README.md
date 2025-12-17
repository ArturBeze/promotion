###Promotion

Собираем образ

    docker build -t my-python-app:latest ./app

Запуск

    kubectl apply -f deployment.yaml

Проверка

    kubectl get pods

Масштабирование до 100 контейнеров

    kubectl scale deployment python-workers --replicas=100

Проверка

    kubectl get pods | wc -l

