# Imports
from pymongo import MongoClient
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from bson.objectid import ObjectId

# Creating a path to Mongodb
env_path = Path('.') / '.env'
load_dotenv(find_dotenv())
password = os.environ.get("MONGO_PASSWORD")
connection_string = f"mongodb+srv://pp452:{password}@cluster0.w41yhpc.mongodb.net/"

# Class to handle document exports to MongoDB
class DocumentsHandler:
    collection_name = 'catalogs'
    user_id = None

    @classmethod
    def _get_collection(cls):
        client = MongoClient(connection_string)
        database = client['slack']
        collection = database[cls.collection_name]
        return collection, client
    
    @classmethod
    def create_document(cls, document):
        collection, client = cls._get_collection()
        collection.insert_one(document)
        client.close()

    @classmethod
    def update_document(cls, user_id, updated_fields):
        if updated_fields is None:
            print('updated_fields is None')
            return

        collection, client = cls._get_collection()

        new_fields = {k: v for k, v in updated_fields.items() if v is not None}

        update_result = collection.update_one(
            {"user_id": user_id},
            {"$set": new_fields}
        )

        print('Update operation result:', update_result)
        client.close()
    
    @classmethod
    def get_document_by_user(cls, user_id):
        collection, client = cls._get_collection()
        document = collection.find_one({"user_id": user_id})
        client.close()
        return document
    
    @classmethod
    def check_user_id_exists(cls, user_id):
        collection, client = cls._get_collection()
        document = collection.find_one({"user_id": user_id})
        client.close()
        return document is not None
