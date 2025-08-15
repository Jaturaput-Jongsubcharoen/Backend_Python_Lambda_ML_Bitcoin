from mangum import Mangnum
from src.app import app

handler = Mangum(app)