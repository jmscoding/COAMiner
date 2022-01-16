import json

class NewArticle():
    def __init__(self, data=None):
        self.data = data

class RelevantArticle(NewArticle):
    def __init__(self, data=None, id=None):
        super().__init__(data)
        self.id = id
        if id is not None:
            self.data['_id'] = id
    
    def dump_json(self):
        return(self.data)

# Testfunktionen
def load_data(f):
    with open(f, 'r') as fn:
        data = json.load(fn)
        return(data)

if __name__ == "__main__":
    filename = '/home/js/Desktop/COAMiner/Extractor/src/test_extractor_ds.json'
    d = load_data(filename)
    # print(d)
    newest = NewArticle(d[0])
    #print(newest.data)

    n = 0
    test_id = f'thn{n+1}'
    relevant = RelevantArticle(d[1], test_id)
    data = relevant.dump_json()
    print(data)