# Используем базовый образ Python
FROM python:3.12.2

# Устанавливаем переменные окружения
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Создаем и переходим в директорию /app
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . .

# Экспортируем порт 5000, который будет использоваться Flask
EXPOSE 5000

# Команда для запуска приложения
CMD ["flask", "run"]
