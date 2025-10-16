from pymongo import MongoClient
from fastapi_demo.utility import get_env_value

#####################################################
MONGO_URI = get_env_value("MONGO_URI")
DB_NAME = get_env_value("DB_NAME")
#####################################################

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
api_call_log = db["api_call_log"]
