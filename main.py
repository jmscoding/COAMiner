import pandas as pd
import json

from extractor import Extractor
from classificator import ClassClassificator
from articles import NewArticle, RelevantArticle
from database import Database
from scraper import Scraper
from coa import Coa

import sys
import time
import schedule

# load Data
def load_data(file):
  with open(file, "r", encoding="utf-8") as f:
    data = json.load(f)
  return(data)

# write Data
def write_data(filename, data):
  with open(filename, "a", encoding="utf-8") as of:
    json.dump(data, of, indent=4)

def coaminer(testarg):
  # Tests
  data = load_data("/home/js/Desktop/COAMiner/Extractor/src/test_extractor_ds.json")
  df = pd.DataFrame(data)

  # Start of Function
  db_name = "coaminer"
  new_article_col = "new_article"
  rel_article_col = "rel_article"
  coa_col = "coa"
  if(testarg):
    test = True
    db_name = "testdb"
    new_article_col = "test_new_article"
    rel_article_col = "test_rel_article"
    coa_col = "test_coa"
  else:
    test = False
  print(test)
  # Call DB
  db = Database(mongo_db=db_name)

  # Call Scraper
  s = Scraper(test=test)
  s.start_sraping()

  # Check if 1..* new_article in db_new_articles and how many relevant articles at this time
  new_counter = db.db[new_article_col].count_documents({})
  old_rel_counter = db.db[rel_article_col].count_documents({})
  # print(counter)
  if new_counter > 0:
    model = ClassClassificator.load_classifier_model()
    classifier = ClassClassificator(model=model)
    # Call Classificator (classify(article) for doc in col(new_article))
    rel_id = old_rel_counter + 1
    rel_article_elems = []
    new_article = db.db[new_article_col]
    for article in new_article.find():
      clf = classifier.classify(article)
      if clf:
        data = {
          'title': article['title'],
          'author': article['author'],
          'date': article['date'],
          'text': article['text'],
          'blog': article['blog'],
          'url': article['url']
        }
        rel_article = RelevantArticle(data=data, id=rel_id)
        rel_article_elems.append(rel_article.dump_json())
        db.db[rel_article_col].insert_one(rel_article.dump_json())
        rel_id += 1
      
    # insert all relevant articles to relevant_articles
    '''
    if len(rel_article_elems) > 0:
      db.db[rel_article_col].insert_many(rel_article_elems)
    '''

    # delete all elements in new_article dab
    db.db[new_article_col].delete_many({})

    # Check if 1..* relevant_article in db_relevant_articles
    new_rel_counter = db.db[rel_article_col].count_documents({})

    if new_rel_counter > old_rel_counter:
      # Call Extractor
      extractor = Extractor()
      rel_article_docs = db.db[rel_article_col]
      old_coa_counter = db.db[coa_col].count_documents({})
      coa_elems = []
      for i in range(old_rel_counter + 1, new_rel_counter + 1):
        rel_query = { "_id": i}
        data = rel_article_docs.find_one(rel_query)
        if data is None:
          continue
        # Test Extractor
        print(data['text'])

        coa_text = extractor.extract(data['text'])
        coa = Coa(id=old_coa_counter+1, 
                  cve=coa_text['enums']['cve'],
                  title=data['title'],
                  article_id=data['_id'],
                  author=data['author'],
                  date=data['date'],
                  blogname=data['blog'],
                  coa=coa_text['coa'])
        # coa_elems.append(coa.dump_json())
        db.db[coa_col].insert_one(coa.dump_json())
        
      


        
      '''
      # Test Extractor
      extractor = Extractor()

      for d in df['text']:
          extractor.extract(d)
      '''

if __name__=="__main__":  
  if (len(sys.argv) > 1) and (sys.argv[1] == 'test'):
    testarg = True
  else:
    testarg = False
  schedule.every().day.at("9:00").do(coaminer(testarg))

  while True:
    schedule.run_pending()
    time.sleep(1)