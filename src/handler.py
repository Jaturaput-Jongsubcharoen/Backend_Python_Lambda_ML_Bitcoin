# src/handler.py
import json, logging
import awsgi
from src.app import app  # make sure src/__init__.py exists so 'src' is a package

logging.getLogger().setLevel(logging.INFO)

def _shim_function_url(event: dict) -> dict:
    """
    Function URLs use a shape similar to API Gateway HTTP API v2,
    but some WSGI adapters expect REST (v1) keys like 'httpMethod' and 'path'.
    This shim adds them if missing.
    """
    if "httpMethod" not in event and "requestContext" in event:
        rc_http = event.get("requestContext", {}).get("http", {})
        # method / path
        event["httpMethod"] = rc_http.get("method", "GET")
        event["path"] = event.get("rawPath", "/")
        # queryStringParameters
        if "rawQueryString" in event and "queryStringParameters" not in event:
            event["queryStringParameters"] = {} if not event["rawQueryString"] else None
        # cookies list -> headers["cookie"]
        if "cookies" in event:
            headers = event.setdefault("headers", {})
            if "cookie" not in headers and "Cookie" not in headers:
                headers["cookie"] = "; ".join(event["cookies"])

    return event

def handler(event, context):
    try:
        # quick debug to verify event shape
        rc = event.get("requestContext", {})
        logging.info("event keys=%s rc keys=%s", list(event.keys()), list(rc.keys()))
        event = _shim_function_url(event)
        return awsgi.response(app, event, context)
    except Exception as e:
        logging.exception("Unhandled error")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                # helpful while debugging CORS from the browser
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"error": str(e)}),
        }