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
    
    def update_one(self, col, query, new):
        up_col_one = self.db[col]
        x = up_col_one(query, new)

    def find_one(self, col):
        fin_one = self.db[col]
        elems = [x for x in fin_one.find()]
        return(elems)


# Test Database Class
#'''
import json

def load_bin(file):
  with open(file, "rb") as f:
    data = json.load(f)
  return(data)


if __name__ ==  "__main__":
    test_db = Database(mongo_db="knowledgebase")

    # Test include new elem to knowledgebase
    '''
    d = load_bin('/home/js/Desktop/COAMiner/src/servicesWin10.json')
    win_10_processes = {
        "_id": "win10process",
        "data": d
    }
    test_db.insert_one_elem(col="process", elem=win_10_processes)
    '''

# '''