"""
    Title: Fill MongoDB
    Description: Fill automated data to MongoDB
    Author: Johannes Seitz
    Create_Date: 23.11.2021
    Update_Date: []
    Version: 0.01 []
"""

from pymongo import MongoClient
import json

def fill_mongo(data):
    try:
        client = MongoClient('localhost', 27017)
        print("Connected successfully!")
    except:
        print("Could not connect to MongoDB")
    
    traindb = client.traindb

    traincollection = traindb.trainds

    for i in data:
        traindb.trainds.insert(i)

    # Debug
    cursor = traincollection.find()
    for record in cursor:
        print(record)


if __name__ == "__main__":
    # open Dataset
    fn = "train_DS.json"
    f = open(fn)
    data = json.load(f)

    fill_mongo(data)