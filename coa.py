import json

class Coa:
    def __init__(self, 
                id=None, 
                cve=None, 
                title=None, 
                article_id=None, 
                author=None, 
                date=None, 
                blogname=None, 
                coa=None) -> None:
        if id is not None:
            self.id = id
        self.enums = {
            "cve": cve
        }
        self.article = {
            "id": article_id,
            "title": title,
            "author": author,
            "date": date,
            "blog": blogname,
            "coa": coa
        }

        self.article_elems = []
        self.article_elems.append(self.article)

    def dump_json(self):
        data = {
            '_id': self.id,
            'enums': self.enums,
            'article': self.article_elems
        }
        return(data)

    
