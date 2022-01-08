from pymongo.errors import ConnectionFailure
from pymongo import MongoClient

class Database:
    def __init__(self, host='localhost', port=27017, mongo_db='coaminer'):
        self.host = host
        self.port = port
        self.mongo_db = mongo_db
        try:
            self.client = MongoClient(self.host, self.port)
            print("Connected successfully!")
        except ConnectionFailure:
            print("Could not connect to MongoDB Server")
        
        self.db = self.client[self.mongo_db]

    def create_collection(self, col):
        pass

    def insert_one_elem(self, col, elem):
        in_col_one = self.db[col]
        x = in_col_one.insert_one(elem)

    def insert_many_elem(self, col, elem):
        in_col_many = self.db[col]
        x = in_col_many.insert_many(elem)

    def drop_col(self, col):
        drop_col = self.db[col]
        drop_col.drop()
