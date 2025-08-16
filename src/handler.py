# src/handler.py
import awsgi # type: ignore
from src.app import app

def handler(event, context):
    return awsgi.response(app, event, context)