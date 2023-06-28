import pymongo
from pymongo import MongoClient
import CarBrandEnum
import re

# Connection details for MongoDB
mongo_host = 'localhost'  
mongo_port = 27017 
mongo_db_name = 'CarRatingBotDB' 

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
        existing_id = existing_document['_id']
        collection.delete_one({'_id': existing_id})
        print("Existing document deleted.")
    

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

def add_car_to_cl(title, price, location, car_attributes, description, link):
    update_document(link, cl_collection)
    car_info = title.split(" ")
    car_year = int(car_info[0])
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

def rateListing(link: str):
    """rates cars submitted by users in the database

    Args:
        link (str): link (PK) of the car to be rated
    """
    #regex match model
    #verify number of cars present
    #if number of cars present >= 10, give a rating based on mean price
    # Find the document with the provided primary key
    document = fb_collection.find_one({'_id':  link})

    if not document:
        print('Document not found.')
        return

    model = document['Model']
    price = document['Price']

    # Calculate the average price of matching documents in Collection1
    matching_documents_fb = fb_collection.find({'Model': model})
    total_price_fb = 0
    count_fb = 0
    for doc_fb in matching_documents_fb:
        total_price_fb += doc_fb['Price']
        count_fb += 1
    average_price_fb = total_price_fb / count_fb if count_fb > 0 else 0

    # Calculate the average price of matching documents in Collection2
    matching_documents_cl = cl_collection.find({'Model': model})
    total_price_cl = 0
    count_cl = 0
    for doc2 in matching_documents_cl:
        total_price_cl += doc2['Price']
        count_cl += 1
    average_price_cl = total_price_cl / count_cl if count_cl > 0 else 0

    # Compare the prices
    if average_price_fb > 0 and price < average_price_fb:
        return(f"The price of {model} in Facebook is lower than the average price of {average_price_fb.__round__(2)}")
    
    elif average_price_fb > 0 and price > average_price_fb:
        return(f"The price of {model} in Facebook is greater than the average price {average_price_fb.__round__(2)}")

    if average_price_cl > 0 and price < average_price_cl:
        return(f"The price of {model} in Craigslist is lower than the average price {average_price_cl.__round__(2)}") 
        
    elif average_price_cl > 0 and price > average_price_cl:
        return(f"The price of {model} in Craigslist is greater than the average price {average_price_cl.__round__(2)}")
        


# Close the MongoDB connection
#client.close()
