import pandas as pd
import json

from extractor import Extractor
from classificator import ClassClassificator
from articles import NewArticle, RelevantArticle
from database import Database
from scraper import Scraper

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
    
    # Call Scraper
    
    # Check if 1..* new_article in db_new_articles

    # Call Classificator

    # Check if 1..* relevant_article in db_relevant_articles
    
    # Call Extractor
    extractor = Extractor()

    for d in df['text']:
        extractor.extract(d)