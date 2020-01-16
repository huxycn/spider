import time
from bs4 import BeautifulSoup

from weibo.general_utils import get_html, get_fm_view_dict

from utils.selenium import Browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('/trash/chromedriver')


url = 'https://weibo.com/u/5044288957?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=1#feedtop'


if __name__ == '__main__':

    from selenium.webdriver.support import expected_conditions as EC

    driver.get(url)
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'Pl_Official_MyProfileFeed__24')))
    print('loading completed')

    time.sleep(10)

    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        print('scroll down')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height





    # html = get_html(url)
    # fm_view_dict = get_fm_view_dict(html)
    # for k, v in fm_view_dict.items():
    #     print(k)
    #
    # print('-'*50)
    #
    # weibo_list_html = fm_view_dict['Pl_Official_MyProfileFeed__24']
    # weibo_list_soup = BeautifulSoup(weibo_list_html, 'lxml')
    # weibo_detail_list = weibo_list_soup.find_all('div', class_='WB_detail')
    # print('LENGTH:', len(weibo_detail_list))
    # for idx, weibo_detail in enumerate(weibo_detail_list):
    #     print(idx, weibo_detail)
    while True:
        key = input('input:')
        if key == 'close':
            driver.close()
