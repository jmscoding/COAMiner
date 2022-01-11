import json

class Coa:
    def __init__(self, data=None, id=None) -> None:
        self.data = data
        if id is not None:
            self.data['_id'] = id

    
