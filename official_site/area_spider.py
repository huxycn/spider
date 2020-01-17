import os
import csv
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.article import Article


# area_name_code_dict = {
#     '贵州省': '520000',
#     '贵阳市': '520100',
#     '六盘水市': '520200',
#     '遵义市': '520300',
#     '安顺市': '520400',
#     '铜仁地区': '522200',
#     '黔西南布依族苗族自治州': '522300',
#     '毕节地区': '522400',
#     '黔东南苗族侗族自治州': '522600',
#     '黔南布依族苗族自治州': '522700'
# }


# anshun = dict()
# bijie = dict(area_name='毕节市', area_code='522200',
#              publish_organization='毕节市人力资源和社会保障局',
#              index_url='http://rsj.bijie.gov.cn/gzdt/',
#              crawl_type=1)

# area_config = {
#     'anshun': anshun,
# }


area_config_list = []
with open('/home/dcb/PycharmProjects/spider/official_site/area_config.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        area_config_list.append(row)


class AreaSpider(object):
    def __init__(self, area_config):
        self.area_name = area_config['area_name']
        self.area_code = area_config['area_code']
        self.publish_organization = area_config['publish_organization']
        self.index_url = area_config['index_url']
        self.crawl_type = area_config['crawl_type']
        print('='*30, 'AreaSpider', '='*30)
        print('area_name:            ', self.area_name)
        print('area_code:            ', self.area_code)
        print('publish_organization: ', self.publish_organization)
        print('index_url:            ', self.index_url)
        print('crawl_type:           ', self.crawl_type)
        print('='*72)
        print()

    def __crawl_article(self, url, publish_date):
        res = requests.get(url)
        html = res.content.decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')

        # crawl type 1
        if self.crawl_type == '1':
            print('crawl type 1 ok!')
            # article_container = soup.find('div', id='c')
            # title = article_container.find('div', class_='title').text.strip()
            # content = []
            # for p in article_container.find('div', class_='view').find_all('p'):
            #     if p.find('img'):
            #         img_src = urljoin(url, p.find('img').attrs['src'])
            #         # img_src = '/'.join(url.split('/')[:-1]) + '/' + p.find('img').attrs['src'].split('./')[-1]
            #         # content.append({'img': img_src})
            #         content.append('<img src="{}">'.format(img_src))
            #     else:
            #         text = p.text.strip()
            #         if text:
            #             # content.append({'text': text})
            #             content.append('<p>{}</p>'.format(text))
            # content = '\n'.join(content)
        else:
            print('crawl type other...')
            article_container = soup.find('div', class_='body_container')
            print(article_container)
            title = article_container.find('div', class_='title').text.strip()
            content = []
            for p in article_container.find('div', class_='view').find_all('p'):
                if p.find('img'):
                    img_src = urljoin(url, p.find('img').attrs['src'])
                    # img_src = '/'.join(url.split('/')[:-1]) + '/' + p.find('img').attrs['src'].split('./')[-1]
                    # content.append({'img': img_src})
                    content.append('<img src="{}">'.format(img_src))
                else:
                    text = p.text.strip()
                    if text:
                        # content.append({'text': text})
                        content.append('<p>{}</p>'.format(text))
            content = '\n'.join(content)
        # else:
        #     article_container = soup.find('div', class_='body_container')
        #     title = article_container.find('div', class_='title').text.strip()
        #     trs = article_container.find_all('tr')
        #     title = trs[1].text.strip()
        #     publish_date = publish_date
        #     content = []
        #     for p in trs[4].find_all('p'):
        #         if p.find('img'):
        #             img_src = urljoin(url, p.find('img').attrs['src'])
        #             content.append('<img src="{}">'.format(img_src))
        #             # img_src = '/'.join(url.split('/')[:-1]) + '/' + p.find('img').attrs['src'].split('./')[-1]
        #             # content.append({'img': img_src})
        #         else:
        #             text = p.text.strip()
        #             if text:
        #                 content.append('<p>{}</p>'.format(text))
        #                 # content.append({'text': text})
        #     content = '\n'.join(content)
        if self.crawl_type != '1':
            article = Article(title=title, content=content, source=1,
                              publish_organization=self.publish_organization,
                              publish_date=publish_date,
                              capture_link=url, area_name=self.area_name,
                              area_code=self.area_code)
            article.push_to_db('table', 'spider_article')
            print('>>> crawl article:', publish_date, url, '[push to database: OK]')

    def __crawl_article_list(self, from_date='2020-01-01'):
        res = requests.get(self.index_url)
        html = res.content.decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        if self.crawl_type == '1':
            print('>>> crawl type 1')
            container = soup.find('div', class_='default_pgContainer')
            for tr in container.find_all('tr'):
                publish_date = tr.find('td', class_='bt_time').text.strip()
                url = tr.find('a').attrs['href']
                if publish_date < from_date:
                    print('up to date.')
                    break
                self.__crawl_article(url, publish_date)
        elif self.crawl_type == '2':



    def initial_crawl(self):
        print('Initial Crawl ===>')
        self.__crawl_article_list()
        print()

    def daily_crawl(self):
        print('Daily Crawl ===>')
        currnet_date = datetime.now().strftime('%Y-%m-%d')
        self.__crawl_article_list(from_date=currnet_date)
        print()


anshun = dict(area_name='安顺市', aera_code='520400', index_url='http://rsj.anshun.gov.cn/gzdt/xwdt/index.html')
bijie = dict(area_name='')


if __name__ == "__main__":
    for area_config in area_config_list:
        AreaSpider(area_config).initial_crawl()
