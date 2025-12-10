# Código da aplicação exemplo
from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    msg = os.getenv("WELCOME_MSG", "Hello from Kubernetes!")
    return f"<h1>{msg}</h1>"

app.run(host="0.0.0.0", port=8080)
