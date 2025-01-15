# Используем альтернативный образ Python
FROM python:3.11-alpine

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DEFAULT_TIMEOUT=100

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости для сборки и curl для healthcheck
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    curl

# Копируем только requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости с увеличенным таймаутом
RUN pip install --no-cache-dir -r requirements.txt --timeout 100

# Копируем код проекта
COPY . .

# Создаем непривилегированного пользователя
RUN adduser -D botuser && chown -R botuser:botuser /app
USER botuser

# Добавляем healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Запускаем бот
CMD ["python", "main.py"]
