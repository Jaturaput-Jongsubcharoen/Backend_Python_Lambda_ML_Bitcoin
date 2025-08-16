# src/handler.py
import awsgi
from src.app import app

def handler(event, context):
    return awsgi.response(app, event, context)