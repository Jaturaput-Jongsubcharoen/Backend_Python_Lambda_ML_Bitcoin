# src/handler.py
import awsgi
from src.app import app

def handler(event, context):
    # Function URLs use HTTP API v2 shape → add v1 keys if missing
    if "httpMethod" not in event and "requestContext" in event:
        rc_http = event["requestContext"].get("http", {})
        event["httpMethod"] = rc_http.get("method", "GET")
        event["path"] = event.get("rawPath", "/")

    return awsgi.response(app, event, context)
