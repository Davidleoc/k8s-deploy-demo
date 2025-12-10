# Código da aplicação exemplo
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return jsonify({"message": os.environ.get("WELCOME_MSG", "Hello from kind cluster!")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
