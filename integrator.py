from database import Database
import json
import os


class Integrator:
    def __init__(self, 
                test=False):
        self.test = test
        if self.test:
            self.db_name = "testdb"
            self.rel_article_col = "test_rel_article"
            self.coa_col = "test_coa"
        else:
            self.db_name = "coaminer"
            self.rel_article_col = "rel_article"
            self.coa_col = "coa"

        self.db = Database(mongo_db=self.db_name)
    
    def export_coa(self, id=None, path='coa_elems'):
        if id is not None:
            exists = os.path.exists(path)
            if not exists:
                try:
                    os.makedirs(path)
                except Exception as e:
                    print(e)

            query = { "_id": id }
            coa_article = self.db.db[self.coa_col].find_one(query)['article']
            for article in coa_article:
                if len(article['coa']['openc2']) > 0:
                    filename = f'{path}/{id}_openc2.json'
                    data = [x for x in article['openc2']]
                    self.write_data(filename=filename, data=data)
                if len(article['coa']['stix']) > 0:
                    filename = f'{path}/{id}_stix.json'
                    data = [x for x in article['stix']]
                    self.write_data(filename=filename, data=data)

    @staticmethod
    def write_data(filename, data):
        with open(filename, "a", encoding="utf-8") as of:
            json.dump(data, of, indent=4)


if __name__=="__main__":
    integrator = Integrator(test=True)
    integrator.export_coa(id=1)
        