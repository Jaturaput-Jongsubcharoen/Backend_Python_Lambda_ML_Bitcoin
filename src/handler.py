# src/handler.py
import json, logging
import awsgi
from src.app import app  # REQUIRED

logging.getLogger().setLevel(logging.INFO)

def handler(event, context):
    try:
        where = getattr(awsgi, "__file__", "<built-in>")
        has_resp = hasattr(awsgi, "response")
        logging.info(f"awsgi imported from: {where}; has response: {has_resp}")
        return awsgi.response(app, event, context)
    except Exception as e:
        logging.exception("Unhandled error in Lambda handler")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": str(e),
                "awsgi_file": getattr(awsgi, "__file__", None),
                "has_response": hasattr(awsgi, "response"),
            }),
        }