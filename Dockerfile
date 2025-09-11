FROM python:3.12.11-slim


WORKDIR /dbloader

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8002

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8002", "--timeout", "900", "--threads", "2", "--worker-class", "gthread", "run:app"]









