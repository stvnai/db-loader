FROM python:3.12.11-slim


WORKDIR /dbloader

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8001

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8001", "run:app"]









