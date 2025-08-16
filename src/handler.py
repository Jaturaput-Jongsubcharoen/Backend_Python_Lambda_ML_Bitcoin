# src/handler.py
import awsgi
from src.app import app

def _shim_function_url(event):
    rc_http = event.get("requestContext", {}).get("http", {})
    if "httpMethod" not in event:                 # ← detect v2
        event["httpMethod"] = rc_http.get("method", "GET")
        event["path"] = event.get("rawPath", "/")
        if "cookies" in event:
            headers = event.setdefault("headers", {})
            headers.setdefault("cookie", "; ".join(event["cookies"]))
        if "rawQueryString" in event and "queryStringParameters" not in event:
            event["queryStringParameters"] = {} if not event["rawQueryString"] else None
    return event

def handler(event, context):
    event = _shim_function_url(event)             # normalize to v1 keys
    return awsgi.response(app, event, context)    # adapter now happy
