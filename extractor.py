import json
from os import name
# import openc2
from stix2 import CourseOfAction


import logging

import pandas as pd
import numpy as np

# spacy library
import spacy
from spacy.matcher import PhraseMatcher
from spacy.language import Language
from spacy.tokens import Span
from spacy import displacy

# Database
from database import Database

# Preprocessor
from preprocessor import ClassPreprocessor

from ioc_finder import ioc_finder as ioc

# Coa
from coa import Coa

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

def load_bin(file):
  with open(file, "rb") as f:
    data = json.load(f)
  return(data)

# write Data
def write_data(filename, data):
  with open(filename, "a", encoding="utf-8") as of:
    json.dump(data, of, indent=4)

def get_winServiceDN(data):
    list_of_serviceDN = []
    for elem in data:
        list_of_serviceDN.append(elem['DisplayName'])
    return(list_of_serviceDN)


# custom spacy model
model = spacy.load("en_core_web_lg")

# load elems from database
db = Database(mongo_db="knowledgebase")
processCol = db.db['process']
winServices = [elem['DisplayName'] for elem in [x for x in processCol.find({"_id": "win10process"})][0]['data']]
# winServices = get_winServiceDN(load_bin('/home/js/Desktop/COAMiner/src/servicesWin10.json')) #['Print Spooler']

oc2actCol = db.db['openc2action']

openc2_action_allow = [x for x in oc2actCol.find({"_id": "allow"})][0]['data']
#openc2_action_allow = ["allow", "permit", "grant", "accept"]

openc2_action_deny = [x for x in oc2actCol.find({"_id": "deny"})][0]['data']
#openc2_action_deny = ["deny", "disallow", "forbid", "prevent"]

openc2_action_update = [x for x in oc2actCol.find({"_id": "update"})][0]['data']
#openc2_action_update = ["update", "upgrade", "modernize", "adapt", "improve"]

openc2_action_start = [x for x in oc2actCol.find({"_id": "start"})][0]['data']
#openc2_action_start = ["start", "enable", "activate", "turn on", "switch on", "initiate"]

openc2_action_stop = [x for x in oc2actCol.find({"_id": "stop"})][0]['data']
#openc2_action_stop = ["stop", "disable", "shutdown", "deactivate", "turn off", "switch off", "disconnect", "discontinue"]


win_serv_pattern = list(model.pipe(winServices))
win_serv_matcher = PhraseMatcher(model.vocab)
win_serv_matcher.add("WIN_SERV", win_serv_pattern)
logger.debug(str(win_serv_pattern))

#OpenC2 Actions
openc2_action_stop_pattern = list(model.pipe(openc2_action_stop))
openC2_Stop_matcher = PhraseMatcher(model.vocab)
openC2_Stop_matcher.add("OPENC2_ACTION_STOP", openc2_action_stop_pattern)
logger.debug(str(openc2_action_stop_pattern))

openc2_action_start_pattern = list(model.pipe(openc2_action_start))
openC2_Start_matcher = PhraseMatcher(model.vocab)
openC2_Start_matcher.add("OPENC2_ACTION_START", openc2_action_start_pattern)
logger.debug(str(openc2_action_start_pattern))

openc2_action_allow_pattern = list(model.pipe(openc2_action_allow))
openC2_Allow_matcher = PhraseMatcher(model.vocab)
openC2_Allow_matcher.add("OPENC2_ACTION_ALLOW", openc2_action_allow_pattern)
logger.debug(str(openc2_action_allow_pattern))

openc2_action_deny_pattern = list(model.pipe(openc2_action_deny))
openC2_Deny_matcher = PhraseMatcher(model.vocab)
openC2_Deny_matcher.add("OPENC2_ACTION_DENY", openc2_action_deny_pattern)
logger.debug(str(openc2_action_deny_pattern))

openc2_action_update_pattern = list(model.pipe(openc2_action_update))
openC2_Update_matcher = PhraseMatcher(model.vocab)
openC2_Update_matcher.add("OPENC2_ACTION_UPDATE", openc2_action_update_pattern)
logger.debug(str(openc2_action_update_pattern))

@Language.component("openc2_action_stop_component")
def openc2_action_stop_component_function(doc):
    # Apply the matcher to the doc
    matches = openC2_Stop_matcher(doc)
    # Create a Span for each match and assign the label "WIN_SERV"
    spans = [Span(doc, start, end, label="OPENC2_ACTION_STOP") for match_id, start, end in matches]
    # Overwrite the doc.ents with the matched spans
    doc.ents = spans
    return doc

@Language.component("openc2_action_start_component")
def openc2_action_start_component_function(doc):
    # Apply the matcher to the doc
    matches = openC2_Start_matcher(doc)
    # Create a Span for each match and assign the label "OPENC2_ACTION_START"
    spans = [Span(doc, start, end, label="OPENC2_ACTION_START") for match_id, start, end in matches]
    # Overwrite the doc.ents with the matched spans
    new_ents = []
    for ent in doc.ents:
        new_ents.append(ent)
    for ent in spans:
        if ent.label_ == "OPENC2_ACTION_START":
            new_ents.append(ent)
    doc.ents = new_ents
    return doc

@Language.component("openc2_action_allow_component")
def openc2_action_allow_component_function(doc):
    # Apply the matcher to the doc
    matches = openC2_Allow_matcher(doc)
    # Create a Span for each match and assign the label "OPENC2_ACTION_ALLOW"
    spans = [Span(doc, start, end, label="OPENC2_ACTION_ALLOW") for match_id, start, end in matches]
    # Overwrite the doc.ents with the matched spans
    new_ents = []
    for ent in doc.ents:
        new_ents.append(ent)
    for ent in spans:
        if ent.label_ == "OPENC2_ACTION_ALLOW":
            new_ents.append(ent)
    doc.ents = new_ents
    return doc

@Language.component("openc2_action_deny_component")
def openc2_action_deny_component_function(doc):
    # Apply the matcher to the doc
    matches = openC2_Deny_matcher(doc)
    # Create a Span for each match and assign the label "OPENC2_ACTION_DENY"
    spans = [Span(doc, start, end, label="OPENC2_ACTION_DENY") for match_id, start, end in matches]
    # Overwrite the doc.ents with the matched spans
    new_ents = []
    for ent in doc.ents:
        new_ents.append(ent)
    for ent in spans:
        if ent.label_ == "OPENC2_ACTION_DENY":
            new_ents.append(ent)
    doc.ents = new_ents
    return doc

@Language.component("openc2_action_update_component")
def openc2_action_update_component_function(doc):
    # Apply the matcher to the doc
    matches = openC2_Update_matcher(doc)
    # Create a Span for each match and assign the label "OPENC2_ACTION_UPDATE"
    spans = [Span(doc, start, end, label="OPENC2_ACTION_UPDATE") for match_id, start, end in matches]
    # Overwrite the doc.ents with the matched spans
    new_ents = []
    for ent in doc.ents:
        new_ents.append(ent)
    for ent in spans:
        if ent.label_ == "OPENC2_ACTION_UPDATE":
            new_ents.append(ent)
    doc.ents = new_ents
    return doc


# Process
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

# Network Connection

model.add_pipe("winserv_component", after="ner")
model.add_pipe("openc2_action_stop_component", after="ner")
model.add_pipe("openc2_action_start_component", after="ner")
model.add_pipe("openc2_action_deny_component", after="ner")
model.add_pipe("openc2_action_allow_component", after="ner")
model.add_pipe("openc2_action_update_component", after="ner")
print(model.pipe_names)
logger.debug(str(model.pipe_names))


class Extractor:   
    def __init__(self):     
        
        self.prep_model = ClassPreprocessor.load_model()
        self.preprocessor = ClassPreprocessor(spacy_model=self.prep_model, remove_newline_or_tab=True)
    
    def extract(self, text):        
        coa = {}
        coa_elems = {}
        cve = []
        coa_enums = {}
        openc2_elems = []
        stix = []
        stix_elems = []
        stix_elems_buff = []
        stix_pre = False

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

            # find custom labels
            win_service_elem = [e.text for e in s.ents if e.label_ == "WIN_SERV"]
            logger.debug(len(win_service_elem))
            openc2_action_stop_elem = [e.text for e in s.ents if e.label_ == "OPENC2_ACTION_STOP"]
            logger.debug(len(openc2_action_stop_elem))
            openc2_action_start_elem = [e.text for e in s.ents if e.label_ == "OPENC2_ACTION_START"]
            logger.debug(len(openc2_action_start_elem))
            openc2_action_allow_elem = [e.text for e in s.ents if e.label_ == "OPENC2_ACTION_ALLOW"]
            logger.debug(len(openc2_action_allow_elem))
            openc2_action_deny_elem = [e.text for e in s.ents if e.label_ == "OPENC2_ACTION_DENY"]
            logger.debug(len(openc2_action_deny_elem))
            openc2_action_update_elem = [e.text for e in s.ents if e.label_ == "OPENC2_ACTION_UPDATE"]
            logger.debug(len(openc2_action_update_elem))

            # find iocs enums
            cves = ioc.parse_cves(sent.text)
            if len(cves) > 0:
                for enum in cves:
                    cve.append(enum)

            # find iocs network
            urls = ioc.parse_urls(sent.text)
            domains = ioc.parse_domain_names(sent.text)
            ipv4 = ioc.parse_ipv4_addresses(sent.text)
            mac_addr = ioc.parse_ipv4_addresses(sent.text)

            # Check stix
            stix_act = False
            
            # stop process
            if (len(win_service_elem) > 0) and (len(openc2_action_stop_elem) > 0):
                stix_act = True
                logger.debug("is in")    
                targettype = "Process"
                elem = self.__extract_openc2_action_stop(target=win_service_elem[0], targettype=targettype)
                # print(elem)
                openc2_elems.append(elem)
                #print(openc2_elems)
            
            # deny iri
            if ((len(urls) > 0) and (len(openc2_action_deny_elem) > 0)):
                stix_act = True
                logger.debug("is in")    
                targettype = "iri"
                elem = self.__extract_openc2_action_deny(target=urls[0], targettype=targettype)
                # print(elem)
                openc2_elems.append(elem)
                #print(openc2_elems)

            # deny domain name
            if ((len(domains) > 0) and (len(openc2_action_deny_elem) > 0)):
                stix_act = True
                logger.debug("is in")    
                targettype = "domain_name"
                elem = self.__extract_openc2_action_deny(target=domains[0], targettype=targettype)
                # print(elem)
                openc2_elems.append(elem)
                #print(openc2_elems)

            # deny ipv4
            if ((len(ipv4) > 0) and (len(openc2_action_deny_elem) > 0)):
                stix_act = True
                logger.debug("is in")    
                targettype = "ipv4_net"
                elem = self.__extract_openc2_action_deny(target=ipv4[0], targettype=targettype)
                # print(elem)
                openc2_elems.append(elem)
                #print(openc2_elems)

            # deny mac_addr
            if ((len(ipv4) > 0) and (len(openc2_action_deny_elem) > 0)):
                stix_act = True
                logger.debug("is in")    
                targettype = "mac_addr"
                elem = self.__extract_openc2_action_deny(target=mac_addr[0], targettype=targettype)
                # print(elem)
                openc2_elems.append(elem)
                #print(openc2_elems)

            '''
                Beliebige Ergänzung möglich

                z.B. nur openC2 Action oder nur Target dann stix_act = True
            '''

            # STIX other coa
            if ((stix_pre is False) and (stix_act is True)) or ((stix_pre is True) and (stix_act is True)):
                stix_elems_buff.append(sent.text)
                stix_pre = True
            if (stix_act is False):
                if(len(stix_elems_buff) >= 2):
                    stix_elems.append(' '.join(stix_elems_buff))
                else:
                    stix_elems_buff = []
            
        print(stix_elems)
        if len(stix_elems) > 0:
            stix = self.__extract_stix(stix_elems)
        coa_elems['stix'] = stix

        print(openc2_elems)
        # Test Writing Data to file
        write_data(filename="test.json",data=openc2_elems)
        coa_elems['openc2'] = openc2_elems

        coa_enums['cve'] = cve

        coa['enums'] = coa_enums
        coa['coa'] = coa_elems
        
        return(coa)

        

    def __extract_stix(self, stix_elems):
        stix = []
        for i, v in enumerate(stix_elems):
            name = f"stix element {i}"
            coa = CourseOfAction(name=name,
                                description=v)
            stix.append(coa)
        return(stix)

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
        return openc2_action_stop_elem
    
    def __extract_openc2_action_start(self, target, targettype):
        action = "start"
        openc2_action_start_elem = {
            "action": action,
            "target": {
                targettype: {
                    "name": target
                }
            }
        }
        return openc2_action_start_elem

    def __extract_openc2_action_allow(self, target, targettype):
        action = "allow"
        openc2_action_allow_elem = {
            "action": action,
            "target": {
                targettype: {
                    "name": target
                }
            }
        }
        return openc2_action_allow_elem
    
    def __extract_openc2_action_deny(self, target, targettype):
        action = "deny"
        openc2_action_deny_elem = {
            "action": action,
            "target": {
                targettype: {
                    "name": target
                }
            }
        }
        return openc2_action_deny_elem
    
    def __extract_openc2_action_update(self, target, targettype):
        action = "update"
        openc2_action_update_elem = {
            "action": action,
            "target": {
                targettype: {
                    "name": target
                }
            }
        }
        return openc2_action_update_elem
 

if __name__=="__main__":
    data = load_data("/home/js/Desktop/COAMiner/Extractor/src/test_extractor_ds.json")
    df = pd.DataFrame(data)
    
    # Test load_bin Function
    '''
    ws = load_bin('/home/js/Desktop/COAMiner/src/servicesWin10.json')
    print(ws)
    for elem in ws:
        print(elem['DisplayName'])
    '''

    # Test Extractor
    #'''
    extractor = Extractor()

    for d in df['text']:
        extractor.extract(d)
    #'''