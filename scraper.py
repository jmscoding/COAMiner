from Scraper.TPScraper.TPScraper import TPScraper
from Scraper.TPScraper.TPScraper_element import TPScraper_element
from database import Database

import json
import pymongo

class Scraper:
    def __init__(self):
        self.scraperList = ["TPScraper"]
        self.db = Database(mongo_db="testdb")
        self.last_status_col = self.db['test_laststatus']

        for x in self.last_status_col.find():
            print(x)
    
    def start_sraping(self, last_status):
        for scraper in self.scraperList:
            if scraper == "TPScraper":
                tpscraper = TPScraper()
                new_url_List = tpscraper.monitorSite(last_status['TPScraper'])
                print(len(new_url_List))
                if len(new_url_List) > 0:
                    print(new_url_List)
                    #tpscraper_elem = TPScraper_element(new_url_List)
                    #tpscraper_elements = tpscraper_elem.parse()
                    

                    # write all elements to database
                
# Test Code               
def load_data(file):
  with open(file, "r", encoding="utf-8") as f:
    data = json.load(f)
  return(data)

if __name__ == "__main__":
    # s = Scraper()
    
    # Test Input last status file in database
    fn = "/home/js/Desktop/COAMiner/Scraper/TPScraper/src/last_status.json"
    last_status = load_data(fn)

    db = Database(mongo_db="testdb")
    db.insert_many_elem(col='test_laststatus', elem=last_status)


    # Test Output
    #print(last_status['TPScraper']['old_url'])
    # s.start_sraping()

