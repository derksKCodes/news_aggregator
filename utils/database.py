from pymongo import MongoClient
from config import settings

def get_mongo_client():
    return MongoClient(settings.MONGODB_URI)

def insert_into_mongodb(data):
    client = get_mongo_client()
    db = client[settings.MONGODB_DB]
    collection = db[settings.MONGODB_COLLECTION]
    
    # Insert documents
    result = collection.insert_many(data)
    
    client.close()
    return len(result.inserted_ids)