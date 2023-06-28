import pymongo
from pymongo import MongoClient
import CarBrandEnum
import re

# Connection details for MongoDB
mongo_host = 'localhost'  # MongoDB host
mongo_port = 27017  # MongoDB port
mongo_db_name = 'CarRatingBotDB'  # Name of the database

# Connect to MongoDB
client = MongoClient(mongo_host, mongo_port)

# Access the database
db = client[mongo_db_name]

try:
    db.validate_collection("CL")  # Try to validate a collection
except pymongo.errors.OperationFailure:  # If the collection doesn't exist
    print("This collection doesn't exist, creating DB")
    import createDB
    createDB.CreateDB()
    
    

# Access the FB and CL collections
fb_collection = db['FB']
cl_collection = db['CL']


def update_document(primary_key, collection):
    # Check if the document already exists
    existing_document = collection.find_one({'_id': primary_key})

    if existing_document:
        # Retrieve the _id value
        existing_id = existing_document['_id']

        # Delete the existing document
        collection.delete_one({'_id': existing_id})
        print("Existing document deleted.")
    

   

# Function to add a car to the FB collection
def add_car_to_fb(title, price, location, description, link):
    update_document(link, fb_collection)
    car_info = title.split(" ")
    car_year = int(car_info[0])
    matches = find_matches(title)
    if matches is not None:
        car_make = matches
    else:
        pass
    
    car_model_substring = title.upper().find(car_make)
    
    if car_model_substring != -1:
        car_model = str(title[car_model_substring + len(car_make):]).split()
    else:
        car_model = title[title.find(car_make):]
        car_model = title.replace(car_make, "").replace(str(car_year), "").lstrip()
    
    car_data = {
        "_id" : link,
        "Title": ''.join(title),
        "Price": float(price.replace('$', '').replace(',', '')), 
        "Location": location,
        "Make": car_make,
        "Model": car_model,
        "Year": car_year,
        "Description": ''.join(description)
    }
    
    fb_collection.insert_one(car_data)
    print("Car added to FB collection successfully!")

# Function to add a car to the CL collection
def add_car_to_cl(title, price, location, car_attributes, description, link):
    update_document(link, cl_collection)
    car_info = title.split(" ")
    car_year = int(car_info[0])
    #car_make = str(CarBrandEnum.CarBrand[str(car_info[1]).upper()].name)
    car_make = car_info[1]
    car_model_substring = title.upper().find(car_make)
    
    if car_model_substring != -1:
        car_model = str(title[car_model_substring + len(car_make):]).split()
    else:
        car_model = title[title.find(car_make):]
        car_model = title.replace(car_make, "").replace(str(car_year), "").lstrip()
    
    try:
        car_data = {
        "_id" : link,
        "Title": ''.join(title),
        "Price": float(price.replace('$', '').replace(',', '')), 
        "Location": location,
        "Make": car_make,
        "Model": ''.join(car_model),
        "Year": car_year,
        "Vin": car_attributes.get("vin") or "",
        "Odometer": int(car_attributes.get("odometer")),
        "Condition": car_attributes.get("condition"),
        "Drive": car_attributes.get("drive") or "",
        "Fuel": car_attributes.get("fuel"),
        "Paint Color": car_attributes.get("paint color"),
        "Size": car_attributes.get("size"),
        "Title status": car_attributes.get("title status"),
        "Transmission": car_attributes.get("transmission"),
        "Type": car_attributes.get("type"),
        "Description": ''.join(description)
    }
        cl_collection.insert_one(car_data)
        print("Car added to CL collection successfully!")
        
        
    except KeyError:
        pass
    
def find_matches(string):
    matches = None
    for car_brand in CarBrandEnum.CarBrand:
        pattern = re.compile(re.escape(car_brand.value), re.IGNORECASE)
        match = pattern.search(string)
        if match:
            return match.group(0)
    return None
        
    


# Close the MongoDB connection
client.close()
