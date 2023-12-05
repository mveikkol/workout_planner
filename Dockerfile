FROM python:3

COPY app.py . /

COPY templates /templates

EXPOSE 5000

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir flask

CMD [ "python", "./app.py" ]