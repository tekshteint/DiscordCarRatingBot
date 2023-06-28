import os as installer
try:
    from pymongo import MongoClient
    
except ImportError:
    installer.system("pip install pymongo --user")
    print("All packages successfully installed.")    
    from pymongo import MongoClient


def CreateDB():
    # Connection details for MongoDB
    mongo_host = 'localhost'  
    mongo_port = 27017  
    mongo_db_name = 'CarRatingBotDB'  

    # JSON schemas for FB and CL documents
    fb_schema = {
        "bsonType": "object",
        "properties": {
            "_id": {"bsonType": "string"},
            "Make": {"bsonType": "string", "maxLength": 100},
            "Model": {"bsonType": "string", "maxLength": 100},
            "Year": {"bsonType": "int"},
            "Description": {"bsonType": "string"},
            "Location": {"bsonType": "string", "maxLength": 100},
            "Price": {"bsonType": "double"}
        }
    }

    cl_schema = {
        "bsonType": "object",
        "properties": {
            "_id": {"bsonType": "string"},
            "Make": {"bsonType": "string", "maxLength": 100},
            "Model": {"bsonType": "string", "maxLength": 100},
            "Year": {"bsonType": "int"},
            "Description": {"bsonType": "string"},
            "Location": {"bsonType": "string", "maxLength": 100},
            "Price": {"bsonType": "double"},
            "Vin": {"bsonType": "string", "maxLength": 100},
            "Odometer": {"bsonType": "int"},
            "Condition": {"bsonType": "string", "maxLength": 100},
            "Drive": {"bsonType": "string", "maxLength": 100},
            "Fuel": {"bsonType": "string", "maxLength": 100},
            "paint color": {"bsonType": "string", "maxLength": 100},
            "size": {"bsonType": "string", "maxLength": 100},
            "title status": {"bsonType": "string", "maxLength": 100},
            "transmission": {"bsonType": "string", "maxLength": 100},
            "type": {"bsonType": "string", "maxLength": 100}
        }
    }

    # Connect to MongoDB
    client = MongoClient(mongo_host, mongo_port)

    # Create a new database
    db = client[mongo_db_name]

    # Create collections and apply schemas
    fb_collection = db['FB']
    fb_collection.create_index("Price")
    db.command({"collMod": "FB", "validator": {"$jsonSchema": fb_schema}})

    cl_collection = db['CL']
    cl_collection.create_index("Price")
    db.command({"collMod": "CL", "validator": {"$jsonSchema": cl_schema}})

    # Print the list of available databases
    print(f"List of available databases: {client.list_database_names()}")

    # Close the MongoDB connection
    client.close()
    
if __name__ == "__main__":
    CreateDB()