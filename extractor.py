import json
from os import name
# import openc2

import logging

import pandas as pd
import numpy as np

# spacy library
import spacy
from spacy.matcher import PhraseMatcher
from spacy.language import Language
from spacy.tokens import Span
from spacy import displacy

# Preprocessor
from preprocessor import ClassPreprocessor

# Create a logger
logger = logging.getLogger('logs/extractor_logger')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('extractor_logger.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# load Data
def load_data(file):
  with open(file, "r", encoding="utf-8") as f:
    data = json.load(f)
  return(data)

# write Data
def write_data(filename, data):
  with open(filename, "a", encoding="utf-8") as of:
    json.dump(data, of, indent=4)

# custom spacy model
model = spacy.load("en_core_web_lg")
winServices = ["Print Spooler"]

openc2_action_allow = ["allow", "permit", "grant", "accept"]
openc2_action_deny = ["deny", "disallow", "forbid", "prevent"]
openc2_action_update = ["update", "upgrade", "modernize", "adapt", "improve"]
openc2_action_start = ["start", "enable", "activate", "turn on", "switch on", "initiate"]
openc2_action_stop = ["stop", "disable", "shutdown", "deactivate", "turn off", "switch off", "disconnect", "discontinue"]

win_serv_pattern = list(model.pipe(winServices))
win_serv_matcher = PhraseMatcher(model.vocab)
win_serv_matcher.add("WIN_SERV", win_serv_pattern)
logger.debug(str(win_serv_pattern))

openc2_action_stop_pattern = list(model.pipe(openc2_action_stop))
openC2_Stop_matcher = PhraseMatcher(model.vocab)
openC2_Stop_matcher.add("OPENC2_ACTION_STOP", openc2_action_stop_pattern)
logger.debug(str(openc2_action_stop_pattern))


@Language.component("openc2_action_stop_component")
def openc2_action_stop_component_function(doc):
    # Apply the matcher to the doc
    matches = openC2_Stop_matcher(doc)
    # Create a Span for each match and assign the label "WIN_SERV"
    spans = [Span(doc, start, end, label="OPENC2_ACTION_STOP") for match_id, start, end in matches]
    # Overwrite the doc.ents with the matched spans
    doc.ents = spans
    return doc

@Language.component("winserv_component")
def winserv_component_function(doc):
    # Apply the matcher to the doc
    matches = win_serv_matcher(doc)
    # Create a Span for each match and assign the label "WIN_SERV"
    spans = [Span(doc, start, end, label="WIN_SERV") for match_id, start, end in matches]
    # Overwrite the doc.ents with the matched spans
    new_ents = []
    for ent in doc.ents:
        new_ents.append(ent)
    for ent in spans:
        if ent.label_ == "WIN_SERV":
            new_ents.append(ent)
    doc.ents = new_ents
    return doc

model.add_pipe("winserv_component", after="ner")
model.add_pipe("openc2_action_stop_component", after="ner")
print(model.pipe_names)
logger.debug(str(model.pipe_names))


class Extractor:   
    def __init__(self):     
        
        self.prep_model = ClassPreprocessor.load_model()
        self.preprocessor = ClassPreprocessor(spacy_model=self.prep_model, remove_newline_or_tab=True)
    
    def extract(self, text):
        openc2_elems = []

        clean_text = self.preprocessor.preprocess_text(text)
        #print(clean_text)
        # change punct to colon 
        clean_text = clean_text.replace(":", ".")
        doc = model(clean_text)
        print([(ent.text, ent.label_) for ent in doc.ents])
        #displacy.render(doc, style='ent', options={'distance': 90})

        sentences = [i for i in doc.sents]
        for sent in sentences:
            s = model(sent.text)
            #print(s.text)
            #break
            logger.debug("new round")
            win_service_elem = [e.text for e in s.ents if e.label_ == "WIN_SERV"]
            logger.debug(len(win_service_elem))
            openc2_action_stop_elem = [e.text for e in s.ents if e.label_ == "OPENC2_ACTION_STOP"]
            logger.debug(len(openc2_action_stop_elem))
            if (len(win_service_elem) > 0) and (len(openc2_action_stop_elem) > 0):
                logger.debug("is in")    
                targettype = "Process"
                elem = self.__extract_openc2_action_stop(target=win_service_elem[0], targettype=targettype)
                # print(elem)
                openc2_elems.append(elem)
                #print(openc2_elems)
        print(openc2_elems)
        # Test Writing Data to file
        write_data(filename="test.json",data=openc2_elems)

    def __extract_openc2_action_stop(self, target, targettype):
        action = "stop"
        openc2_action_stop_elem = {
            "action": action,
            "target": {
                targettype: {
                    "name": target
                }
            }
        }
        target = target.replace(" ", "")
        '''
        # Test openc2 Serialization
        cmd = openc2.v10.Command(
            action=action,
            target=openc2.v10.Process(name=target),
            )
        #logger.debug(cmd)
        
        '''
        return openc2_action_stop_elem


if __name__=="__main__":
    data = load_data("/home/js/Desktop/COAMiner/Extractor/src/test_extractor_ds.json")
    df = pd.DataFrame(data)
    extractor = Extractor()

    for d in df['text']:
        extractor.extract(d)