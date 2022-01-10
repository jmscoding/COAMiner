import pandas as pd
import json

from extractor import Extractor
from classificator import ClassClassificator
from articles import NewArticle, RelevantArticle
from database import Database
from scraper import Scraper

import sys

# load Data
def load_data(file):
  with open(file, "r", encoding="utf-8") as f:
    data = json.load(f)
  return(data)

# write Data
def write_data(filename, data):
  with open(filename, "a", encoding="utf-8") as of:
    json.dump(data, of, indent=4)

def coaminer():
  pass

if __name__=="__main__":
    # Tests
    data = load_data("/home/js/Desktop/COAMiner/Extractor/src/test_extractor_ds.json")
    df = pd.DataFrame(data)

    # Funktionsbeginn
    db_name = "coaminer"
    new_article_col = "new_article"
    rel_article_col = "rel_article"
    if (len(sys.argv) > 1) and (sys.argv[1] == 'test'):
      test = True
      db_name = "testdb"
      new_article_col = "test_new_article"
      rel_article_col = "test_rel_article"
    else:
      test = False
    print(test)
    # Call DB
    db = Database(mongo_db=db_name)

    # Call Scraper
    #s = Scraper(test=test)
    #s.start_sraping()

    # Check if 1..* new_article in db_new_articles and how many relevant articles at this time
    new_counter = db.db[new_article_col].count_documents({})
    old_rel_counter = db.db[rel_article_col].count_documents({})
    # print(counter)
    if new_counter > 0:
      classifier = ClassClassificator()
      # Call Classificator (classify(article) for doc in col(new_article))
      rel_id = old_rel_counter + 1
      # delete all elements in new_article dab
      db.db[new_article_col].delete_many({})

      # Check if 1..* relevant_article in db_relevant_articles
      new_rel_counter = db.db[rel_article_col].count_documents({})

      if new_rel_counter > old_rel_counter:
        # Call Extractor for new 
        '''
        extractor = Extractor()

        for d in df['text']:
            extractor.extract(d)
        '''
    