import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# CORS: start permissive while debugging. Later, restrict with origins=[...].
CORS(app)

@app.get("/health")
def health():
    app.logger.info("Health endpoint hit")
    return jsonify(ok=True, msg="backend is healthy")

@app.get("/python")
def home():
    app.logger.info("/python endpoint hit")
    return {
        "frontend_url": os.getenv("FRONTEND_URL"),
        "message": "Hello from /python that hit from frontend",
    }

# NOTE: no `if __name__ == "__main__": ...` block for Lambda.

#if __name__ == "__main__":  
#    port = int(os.getenv("PORT", 8000))
#    app.run(host="0.0.0.0", port=port, debug=True)