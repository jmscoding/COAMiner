from selenium import webdriver
# from selenium.common import exceptions
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

import time

class TPScraper():
    def __init__(self, url='https://threatpost.com/'): 
        self.url = url

    def monitorSite(self, last_status):
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get(self.url)
        new_url_list = []

        articles = driver.find_elements_by_xpath('.//html/body/div[3]/div[1]/div[4]/div/div/div[1]/div[1]/article')

        for article in articles:
            try:
                next_url = article.find_element_by_xpath('.//div/div[2]/h2/a').get_attribute("href")
                print(next_url)
                # check if old url new url
                if next_url in last_status['old_url']:
                    print("Found last status!!!")
                    return(new_url_list)
                new_url_list.append(next_url)
            except NoSuchElementException:
                try:
                    next_url = article.find_element_by_xpath('.//div/div[1]/h2/a').get_attribute("href")
                    print(next_url)
                    if next_url in last_status['old_url']:
                        print("Found last status!!!")
                        return(new_url_list)
                    new_url_list.append(next_url)
                except NoSuchElementException:
                    print("Kein Element gefunden!!!")
                    continue
        
        driver.quit()
        return new_url_list
        

    def scrapeSite(self, count=1):
        # add options options=options, than browser won't show up
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get(self.url)
        url_list =[] 

        delay = 5
        # each click action adds 5 more Articles - 19(100) 199(1000) 
        for i in range(0, count-1):
            button = driver.find_element_by_xpath('//*[@id="load_more_news"]')
            driver.execute_script("arguments[0].click();", button)
            time.sleep(delay)
            print("wait")

        articles = driver.find_elements_by_xpath('.//html/body/div[3]/div[1]/div[4]/div/div/div[1]/div[1]/article')
        print(len(articles))

        for article in articles:
            try:
                next_url = article.find_element_by_xpath('.//div/div[2]/h2/a').get_attribute("href")
                # print(next_url)
                url_list.append(next_url)
            except NoSuchElementException:
                try:
                    next_url = article.find_element_by_xpath('.//div/div[1]/h2/a').get_attribute("href")
                    # print(next_url)
                    url_list.append(next_url)
                except NoSuchElementException:
                    print("Kein Element gefunden!!!")
                    continue
        
        driver.quit()
        return url_list
            

    