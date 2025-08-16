import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": [
    os.getenv("FRONTEND_AMPLIFY_URL"), 
    os.getenv("FRONTEND_URL")
]}})

@app.get("/health")
def health():
    return jsonify(ok=True, msg="backend is healthy")

@app.route("/python")
def home():
    print("/python hit from frontend")
    return {"frontend_url": os.getenv("FRONTEND_URL"),
            "message": "Hello from /python that hit from frontend",
            }

#@app.route("/python")
#def home():
#    return jsonify({"message": "Hello from Flask Python on Lambda!"})


if __name__ == "__main__":  
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)