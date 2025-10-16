from pymongo import MongoClient

from fastapi_demo.config import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]
api_call_log = db["api_call_log"]
