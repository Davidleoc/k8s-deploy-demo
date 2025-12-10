FROM python:3.11-slim
WORKDIR /app
COPY server.py /app/
RUN pip install --no-cache-dir flask
ENV PORT=8080
EXPOSE 8080
CMD ["python", "server.py"]
