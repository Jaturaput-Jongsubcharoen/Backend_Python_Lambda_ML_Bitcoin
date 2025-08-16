# src/handler.py
import logging
from aws_lambda_wsgi import response as wsgi_response
from src.app import app

logging.getLogger().setLevel(logging.INFO)

def handler(event, context):
    # optional: quick sanity log
    rc = event.get("requestContext", {})
    logging.info("event keys: %s | rc keys: %s", list(event.keys()), list(rc.keys()))
    return wsgi_response(app, event, context)