from Scraper.TPScraper.TPScraper import TPScraper
from Scraper.TPScraper.TPScraper_element import TPScraper_element
from database import Database

import json
import pymongo

class Scraper:
    def __init__(self, test=True):
      self.test = test
      self.scraperList = ["TPScraper"]
      self.last_status = []
        
      if self.test:
        self.db = Database(mongo_db="testdb")
        self.db_col = "test_new_article"
        self.last_status_col = 'test_laststatus'
      else:
        self.db = Database(mongo_db="coadb")
        self.db_col = "new_article"
        self.last_status_col = 'laststatus'

      self.last_status = self.db.find_one(col=self.last_status_col)
    
    def start_sraping(self):
        for scraper in self.scraperList:
            if scraper == "TPScraper":
                tpscraper = TPScraper()
                #print([item for item in self.last_status if item["_id"] == "tpscraper"][0])
                #'''
                new_url_List = tpscraper.monitorSite([item for item in self.last_status if item["_id"] == "tpscraper"][0])
                print(len(new_url_List))
                if len(new_url_List) > 0:
                    print(new_url_List)
                    tpscraper_elem = TPScraper_element(new_url_List)
                    tpscraper_elements = tpscraper_elem.parse()
                    tp_last_element = tpscraper_elements[0]

                    # write all elements to database
                    self.db.insert_many_elem(col=self.db_col, elem=tpscraper_elements)

                    # update last_status
                    tp_query = { "_id": "tpscraper" }
                    tp_new_values = {"$set": {
                                             "old_url": tp_last_element['url'],
                                             "old_title": tp_last_element['title'],
                                             "old_author": tp_last_element['author'],
                                             "old_datetime": tp_last_element['date']
                    }}
                    self.db.update_one(col=self.last_status_col, query=tp_query, new=tp_new_values)
                #'''
                
# Test Code               
def load_data(file):
  with open(file, "r", encoding="utf-8") as f:
    data = json.load(f)
  return(data)

if __name__ == "__main__":
    s = Scraper()
    s.start_sraping()
    
    # Test Input last status file in database
    '''
    fn = "/home/js/Desktop/COAMiner/Scraper/TPScraper/src/last_status.json"
    last_status = load_data(fn)

    db = Database(mongo_db="testdb")
    db.insert_many_elem(col='test_laststatus', elem=last_status)
    '''

    # Test Output
    #print(last_status['TPScraper']['old_url'])
    # s.start_sraping()

