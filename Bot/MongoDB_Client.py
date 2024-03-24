import pymongo
from pymongo import MongoClient
import CarBrandEnum
import re

# Connection details for MongoDB
mongo_host = 'mongodb'  
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
    createDB.run()
    
# Access the FB and CL collections
fb_collection = db['FB']
cl_collection = db['CL']


def update_document(primary_key, collection):
    # Check if the document already exists
    existing_document = collection.find_one({'_id': primary_key})

    if existing_document:
        raise VehicleAdded("This listing is already in the database")
    

def add_car_to_fb(title, price, location, description, link):
    update_document(link, fb_collection)
    car_info = title.split(" ")
    car_year = int(car_info[0])
    matches = find_matches(title)
    if matches is not None:
        car_make = matches
    else:
        car_make = "Unknown Make"
    
    car_model_substring = title.upper().find(car_make)
    
    if car_model_substring != -1:
        car_model = str(title[car_model_substring + len(car_make):]).split()
    else:
        car_model = title[title.find(car_make):]
        car_model = title.replace(car_make, "").replace(str(car_year), "").lstrip()
    if type(car_model) == list:
        print(type(car_model))
        print("Car model list: ", car_model)
        car_model = str(car_model[0])
    
    car_data = {
        "_id" : link,
        "Title": ''.join(title),
        "Price": float(price.replace('$', '').replace(',', '')), 
        "Location": location,
        "Make": car_make,
        "Model": (car_model),
        "Year": car_year,
        "Description": ''.join(description)
    }
    
    fb_collection.insert_one(car_data)
    print("Car added to FB collection successfully!")

def add_car_to_cl(title, price, location, car_attributes, description, link):
    update_document(link, cl_collection)
    car_info = title.split(" ")
    
    words_to_remove = ["super", "low", "mileage", "clean", "project", "mechanic's", "special", "extremely"]
    car_info_lower = [word.lower() for word in car_info]
    car_info_filtered = [word for word in car_info_lower if word not in words_to_remove]
    
    car_year = int(car_info_filtered[0])
    car_make = car_info_filtered[1]
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
        "Vin": car_attributes.get("vin") or "Not Provided",
        "Odometer": int(car_attributes.get("odometer")) or -1,
        "Condition": car_attributes.get("conditioNot Providedn") or "",
        "Drive": car_attributes.get("drive") or "",
        "Fuel": car_attributes.get("fuel") or "Not Provided",
        "Paint Color": car_attributes.get("paint color") or "Not Provided",
        "Size": car_attributes.get("size") or "Not Provided",
        "Title status": car_attributes.get("title status") or "Not Provided",
        "Transmission": car_attributes.get("transmission") or "Not Provided",
        "Type": car_attributes.get("type") or "Not Provided",
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
        print('Document not found on FB.')
        document = cl_collection.find_one({'_id': link})
        if not document:
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
    
    if (average_price_fb == 0):
        total_average = average_price_cl
    elif (average_price_cl == 0):
        total_average = average_price_fb
    else:    
        total_average = (average_price_cl + average_price_fb) / 2
    

    # Compare the prices
    if total_average > 0 and price < total_average:
        return(f"The price of {model} is lower than the average price of {total_average.__round__(2)}")
    
    elif total_average > 0 and price > total_average:
        return(f"The price of {model} is greater than the average price {total_average.__round__(2)}")
        
    else:
        return(f"The price of {model} is equal to the average price {total_average.__round__(2)}")
    
def rateModel(model):
    total_price = 0
    count = 0

    # Create a regular expression pattern for partial matching of the model
    pattern = re.compile(re.escape(model), re.IGNORECASE)

    matching_documents_fb = fb_collection.find({'Model': {'$regex': pattern}})
    for doc_fb in matching_documents_fb:
        total_price += doc_fb['Price']
        count += 1

    matching_documents_cl = cl_collection.find({'Model': {'$regex': pattern}})
    for doc_cl in matching_documents_cl:
        total_price += doc_cl['Price']
        count += 1

    average_price = total_price / count if count > 0 else 0
    return average_price.__round__(2)
        
class VehicleAdded(Exception):
    pass


# Close the MongoDB connection
#client.close()
