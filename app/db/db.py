from pymongo import MongoClient

from app.db.user_schema import user_schema

client: MongoClient = MongoClient("mongodb://127.0.0.1:27017/")
db = client.FastAPI

if "users" not in db.list_collection_names():
    db.create_collection("users", validator={
        "$jsonSchema": user_schema
    })
    print("Collection created successfully")