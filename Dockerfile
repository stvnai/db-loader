FROM python:3.12.11-slim

WORKDIR /dbloader

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8002

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8002", "--timeout", "900", "--threads", "2", "--worker-class", "gthread", "--preload", "run:app"]
