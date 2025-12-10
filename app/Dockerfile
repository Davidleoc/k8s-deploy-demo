FROM python:3.11-slim

WORKDIR /app

COPY server.py /app/

RUN pip install --no-cache-dir flask

CMD ["python", "server.py"]
