# Модель: Математичне моделювання перехідних процесів в електричному ланцюзі (RLC)
# Автор: Борейчук Б.М., група АІ-235

FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 5000

CMD ["python", "main.py"]
