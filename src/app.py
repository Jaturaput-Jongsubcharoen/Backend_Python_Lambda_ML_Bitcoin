import os
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()

app = Flask(__name__)

@app.route("/python")
def home():
    return jsonify({"message": "Hello from Flask Python on Lambda!"})