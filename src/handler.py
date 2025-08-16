# src/handler.py
import json
import logging
import awsgi  # Lambda HTTP adapter for Flask
from src.app import app

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    try:
        return awsgi.response(app, event, context)
    except Exception as e:
        # Make errors visible instead of silent 502s
        logger.exception("Unhandled error in Lambda handler")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)}),
        }