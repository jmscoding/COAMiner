from selenium import webdriver
# from selenium.common import exceptions
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

import time
from datetime import datetime

class TPScraper_element():
    def __init__(self, url_list):
        self.url_list = url_list
        self.blogname = "threat post"

    def parse(self):
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        list_elements = []  
        for element in self.url_list:
            driver.get(element)
            
            try:
                title = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/div/div/div[1]/article/header/h1').text
            except NoSuchElementException:
                title = "None"
            try:
                author = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/div/div/div[1]/article/div/div[1]/div[1]/div[2]/div[1]/a').text
            except NoSuchElementException:
                author = "None"
            try:
                date = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/div/div/div[1]/article/div/div[1]/div[1]/div[2]/div[2]/time').get_attribute("datetime")
            except NoSuchElementException:
                date = "None"
            try:
                text = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/div/div/div[1]/article/div/div[2]/div').text
            except NoSuchElementException:
                text = "None"

            e = {
                'title': title,
                'author': author,
                'date': date,
                'text': text,
                'blog': self.blogname,
                'url': element
            }
            list_elements.append(e)
             
        driver.close()
        return list_elements
