# src/handler.py
import json, logging
import awsgi
from src.app import app

log = logging.getLogger()
log.setLevel(logging.INFO)

def _normalize(event: dict) -> dict:
    rc_http = event.get("requestContext", {}).get("http", {})

    # v2 -> add v1 keys
    event.setdefault("httpMethod", rc_http.get("method", "GET"))
    event.setdefault("path", event.get("rawPath", "/"))

    # headers must be a dict
    headers = event.setdefault("headers", {})

    # cookies list -> single Cookie header (what many WSGI adapters expect)
    if "cookies" in event and "cookie" not in headers and "Cookie" not in headers:
        headers["cookie"] = "; ".join(event.get("cookies") or [])

    # make sure queryStringParameters exists (aws-wsgi touches it)
    if "queryStringParameters" not in event:
        rqs = event.get("rawQueryString", "")
        event["queryStringParameters"] = {} if not rqs else None

    # sane defaults some adapters assume
    event.setdefault("body", None)
    event.setdefault("isBase64Encoded", False)

    return event

def handler(event, context):
    try:
        event = _normalize(event)
        return awsgi.response(app, event, context)
    except Exception as e:
        log.exception("handler error")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  # debug only
            },
            "body": json.dumps({"error": str(e)}),
        }



"""
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

"""