FROM python:3.10

COPY requirements.in /tmp/requirements.in
RUN python -m pip install --no-cache-dir -r /tmp/requirements.in

WORKDIR /app
COPY run.sh .
COPY deploy/gunicorn_conf.py /gunicorn_conf.py
COPY ./counter /app/counter

CMD ["./run.sh"]
