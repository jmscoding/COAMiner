"""
    Title: TPscraper
    Description: Scrapes threatpost blogs totally, with optional limitation
    Author: Johannes Seitz
    Create_Date: 02.10.2021
    Update_Date: []
    Version: 0.01 []
"""

from TPScraper import TPScraper
from TPScraper_element import TPScraper_element
import os.path

import json

def main():
    url = 'https://threatpost.com/'
    # 1x correspond to 5 articles
    count = 101
    
    tpscraper = TPScraper(url)
    url_list = tpscraper.scrapeSite(count=2)
    print(len(url_list))
    
    tpscraper_element = TPScraper_element(url_list)
    elements = tpscraper_element.parse()
    
    # write elements to file
    with open('tpscraperblog.json', 'w', encoding='utf-8') as outfile:
        json.dump(elements, outfile, indent=4)

def scrapeDataset(urllist, isrelevant):
    file_exists = os.path.exists("tpscraperblog_DS.json")
    if file_exists:
        f = open("tpscraperblog_DS.json")
        data = json.load(f)
    else:
        data = []

    tpscraper_element = TPScraper_element(urllist)
    elements = tpscraper_element.parse()

    for element in elements:
        if isrelevant:
            element['label'] = 1
        else:
            element['label'] = 0
        data.append(element)

    if file_exists:
        f.close()

    # write elements to file
    with open('tpscraperblog_DS.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4)

if __name__ == "__main__":
    # scrape whole site until breakpoint
    main()

    # scrape Dataset and label Data
    #f = open("dataset_URL.json")
    #ds = json.load(f)
    #threatpost_URL_rel = ds['threatpost']['relevant']
    # print(zdnet_URL_rel)
    #threatpost_URL_nrel = ds['threatpost']['not relevant']

    #scrapeDataset(threatpost_URL_rel, True)
    #scrapeDataset(threatpost_URL_nrel, False)