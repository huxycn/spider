import os
import csv
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

root = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(root)
import get_article_urls
import get_article
from utils.article import Article


get_article_urls_function_dict = {
    'guizhou': get_article_urls.get_guizhou_atricle_urls,
    'guiyang': get_article_urls.get_guiyang_article_urls,
    'liupanshui': get_article_urls.get_liupanshui_article_urls,
    'zunyi': get_article_urls.get_zunyi_article_urls,
    'anshun': get_article_urls.get_anshun_article_urls,
    'tongren': get_article_urls.get_tongren_article_urls,
    'biejie': get_article_urls.get_bijie_article_urls,
    'qiandongnan': get_article_urls.get_qiandongnan_article_urls,
    'qiannan': get_article_urls.get_qiannan_article_urls
}


get_article_function_dict = {
    'guizhou': get_article.get_guizhou_article,
    'guiyang': get_article.get_guiyang_article,
    'liupanshui': get_article.get_liupanshui_article,
    'zunyi': get_article.get_zunyi_article,
    'anshun': get_article.get_anshun_article,
    'tongren': get_article.get_tongren_article,
    'biejie': get_article.get_bijie_article,
    'qiandongnan': get_article.get_qiandongnan_article,
    'qiannan': get_article.get_qiannan_article
}


class AreaSpider(object):
    def __init__(self, area_config):
        self.area_name = area_config['area_name']
        self.area_code = area_config['area_code']
        self.area_key = area_config['area_key']
        self.publish_organization = area_config['publish_organization']
        self.start_index_urls = area_config['start_index_urls']
        print('='*30, 'AreaSpider', '='*30)
        print('area_name:            ', self.area_name)
        print('area_code:            ', self.area_code)
        print('publish_organization: ', self.publish_organization)
        print('start_index_urls:            ', self.start_index_urls)
        print('='*72)
        print()

    def crawl(self, initial=False):
        if initial:
            from_date = '2020-01-01'
        else:
            from_date = datetime.now().strftime('%Y-%m-%d')

        for start_index_url in self.start_index_urls.split('$$'):
            urls = get_article_urls_function_dict[self.area_key](start_index_url, from_date)
            for url, publish_date in urls:
                title, content = get_article_function_dict[self.area_key](url)
                article = Article(title, content, 1, self.publish_organization,
                                  publish_date, url, self.area_name, self.area_code)
                article.push_to_db('table', 'spider_article')
        print()


if __name__ == "__main__":
    area_config_list = []
    with open(os.path.join(root, 'official_site/area_config.csv'), newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            area_config_list.append(row)
    for area_config in area_config_list:
        if area_config['area_key'] == 'qianxinan' or area_config['area_key'] == 'bijie':
            continue
        AreaSpider(area_config).crawl(initial=True)
