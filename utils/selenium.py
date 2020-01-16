from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Browser(object):
    def __init__(self, driver_path='/home/dcb/PycharmProjects/spider/chromedriver'):
        self.driver = webdriver.Chrome(driver_path)

    def get(self, url):
        self.driver.get(url)

    def close(self):
        self.driver.close()
