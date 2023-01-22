from pymongo import MongoClient

from app.db.signup_schema import signup_schema

client: MongoClient = MongoClient("mongodb://127.0.0.1:27017/")
db = client.FastAPI

if "users" not in db.list_collection_names():
    db.create_collection("users", validator={
        "$jsonSchema": signup_schema
    })
    print("Collection created successfully")