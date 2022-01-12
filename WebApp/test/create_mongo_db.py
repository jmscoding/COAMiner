from pymongo import MongoClient
import json

def create_mongo_db(data=None):
    try:
        client = MongoClient('localhost', 27017)
        print("Connected successfully!")
    except:
        print("Could not connect to MongoDB")
    
    creator = client['test_creator']
    mycol = creator['tests']
    
    x = mycol.insert_many(data)
    
    # Check wich Databases exists
    print(client.list_database_names())

    # Check wich Collections exists
    print(mycol.list_collection_names())

    # List ids of inserted items
    print(x.inserted_ids)


if __name__ == "__main__":
    # open Dataset
    fn = "train_DS.json"
    f = open(fn)
    data = json.load(f)

    create_mongo_db(data)