from pymongo import MongoClient
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from palm_chat import palmChat
from bson.objectid import ObjectId

env_path = Path('.') / '.env'
load_dotenv(find_dotenv())
password = os.environ.get("MONGO_PASSWORD")
connection_string = f"mongodb+srv://pp452:{password}@cluster0.w41yhpc.mongodb.net/"

class DocumentsHandler(palmChat):
    collection_name = 'catalogs'
    current_document_id = None

    @classmethod
    def create_document(cls, document):
        client = MongoClient(connection_string)
        database = client['slackbot']
        collection = database[cls.collection_name]
        result = collection.insert_one(document)
        client.close()
        cls.current_document_id = str(result.inserted_id)
        return cls.current_document_id

    @classmethod
    def update_document(cls, document_id, updated_fields):
        if updated_fields is None:
            print('updated_fields is None')
            return

        client = MongoClient(connection_string)
        database = client['slackbot']
        collection = database[cls.collection_name]

        new_fields = {k: v for k, v in updated_fields.items() if v is not None}

        update_result = collection.update_one(
            {"_id": ObjectId(document_id)},
            {"$set": new_fields}
        )

        print('Update operation result:', update_result)

        client.close()

    @classmethod
    def get_document_id(cls):
        return cls.current_document_id

