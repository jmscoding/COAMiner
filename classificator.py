"""
    Title: Module Classificator
    Description: Classifies all input texts with boolean value, if coa-relevant
    Author: Johannes Seitz
    Create_Date: 02.01.2022
    Update_Date: [16.01.2022]
    Version: 0.09 []
"""

import joblib
import json
import pandas as pd
import numpy as np
import spacy
from xgboost import XGBClassifier
from ioc_finder import find_iocs

from preprocessor import ClassPreprocessor

import logging

# Logging
logger = logging.getLogger('logs/classificator_logger')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('classificator_logger.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class ClassClassificator:
    def __init__(self, model=None):
        self.model = model
    
    def classify(self, article):
        X = self.prepare_data(article)
        rel = self.is_relevant(X)

        if rel:
            print("Text ist relevant!!!")
        else:
            print("Text ist nicht relevant!!!")
        return(rel)

    def is_relevant(self, df):
        prediction = self.model.predict(df)
        print(prediction)
        if prediction[0] == 1:
            return(True)
        else:
            return(False)

    def prepare_data(self, article):
        ClassPreprocessor.download_spacy_model()
        spacy_model = ClassPreprocessor.load_model()
        preprocessor = ClassPreprocessor(spacy_model, remove_stopwords=True, lemmatize=True, remove_newline_or_tab=True)

        clean_text = preprocessor.preprocess_text(article['text'])
        p = {
            'text': clean_text,
        }

        logger.debug(str(p['text']))
        p['text_nouns'] = self.only_nouns(clean_text)
        p['text_verbs'] = self.only_verbs(clean_text)
        p['hasMinLen'] = self.has_MinLen(clean_text)
        p['hasIOC'] = self.has_ioc(article['text'])

        df = pd.DataFrame([p])
        X = df[[
            'text_nouns',
            'text_verbs',
            'hasMinLen',
            'hasIOC'
        ]]
        return(X)
    
    @staticmethod
    def load_classifier_model():
        # load model
        pipe = joblib.load('Models/classifier.joblib')
        return pipe
        
    # Feature Extraction
    def has_MinLen(self, text):
        minlen = 320
        nlp = spacy.load('en_core_web_lg')
        doc = nlp(text)
        # word_list = "text"
        print(len(doc))
        label = 0
        if len(doc) >= minlen:
            label = 1
        return label
    
    def has_ioc(self, text):
        iocs = find_iocs(text)
        label = 0
        list_IOCs = np.array([len(iocs["asns"]), 
                        len(iocs['attack_mitigations']['enterprise']),
                        len(iocs['attack_mitigations']['mobile']),
                        len(iocs['attack_techniques']['enterprise']),
                        len(iocs['attack_techniques']['mobile']),
                        len(iocs['attack_techniques']['pre_attack']),
                        len(iocs["authentihashes"]),
                        len(iocs["bitcoin_addresses"]),
                        len(iocs["cves"]),
                        len(iocs["file_paths"]),
                        len(iocs["imphashes"]),
                        len(iocs["ipv4_cidrs"]),
                        len(iocs["ipv4s"]),
                        len(iocs["ipv6s"]),
                        len(iocs["mac_addresses"]),
                        len(iocs["md5s"]),
                        len(iocs["monero_addresses"]),
                        len(iocs["registry_key_paths"]),
                        len(iocs["sha1s"]),
                        len(iocs["sha256s"]),
                        len(iocs["sha512s"]),
                        len(iocs["ssdeeps"]),
                        len(iocs["tlp_labels"]),
                        len(iocs["xmpp_addresses"]),
                        ])
        sum_iocs = np.sum(list_IOCs)
        if sum_iocs > 0:
            label = 1
        return(label)
    
    def only_nouns(self, text):
        nlp = spacy.load("en_core_web_lg")
        docx = nlp(text)
        nouns = [token.lemma_ for token in docx if token.pos_ == 'NOUN']
        t = " ".join(nouns)
        return t
    
    def only_verbs(self, text):
        nlp = spacy.load("en_core_web_lg")
        docx = nlp(text)
        verbs = [token.lemma_ for token in docx if token.pos_ == 'VERB']
        t = " ".join(verbs)
        return t

# Testfunktionen
def load_data(f):
    with open(f, 'r') as fn:
        data = json.load(fn)
        return(data)

if __name__ == "__main__":
    model = ClassClassificator.load_classifier_model()
    classifier = ClassClassificator(model=model)   

    filename = 'src/trainds.json'
    d = load_data(filename)
    print(d)

    for data in d:
        classifier.classify(data)



