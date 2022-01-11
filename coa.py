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
            self.data['_id'] = id
        self.enums = {
            "cve": cve
        }
        self.article = {
            "id": article_id,
            "title": title,
            "author": author,
            "date": date,
            "coa": coa
        }

    
