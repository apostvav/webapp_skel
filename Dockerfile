FROM python:3.6-alpine

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
RUN mkdir -p /app
COPY webapp_skel /app/webapp_skel
COPY migrations /app/migrations
COPY test /app/test
COPY app.py /app/app.py

WORKDIR /app

ENV FLASK_APP app.py
EXPOSE 5000

CMD ["gunicorn", "-b", ":5000", "app:app"]
