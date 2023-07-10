from pymongo import MongoClient
import palm_chat

connection_string = "mongodb+srv://pp452:5ucu1It8ZFqJWJ8C@cluster0.w41yhpc.mongodb.net/"

client = MongoClient(connection_string)

dbs = client.list_database_names()

bot_db = client.sample_bot_db
collections = bot_db.list_collection_names()

def insert_catalog(catalog):
    collection = bot_db.catalog
    catalog_conversation = catalog
    catalog_id = collection.insert_one(catalog_conversation).inserted_id
    # print(catalog_id)
    return catalog_id


def update_catalog(catalog_id, conversation):
    from bson.objectid import ObjectId

    _id = ObjectId(catalog_id)

    catalog_update = {
        "$set": conversation
    }

    bot_db.catalog.update_one({"_id": _id}, catalog_update)

insert_catalog({'convo1': {'user': 'list 5 flowers.  limit your answer to 5 words please', 'bot': 'Rose, lily, daisy, tulip, orchid.'}})
