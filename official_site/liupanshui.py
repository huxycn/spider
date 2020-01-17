# 六盘水市人力资源社会保障网
# http://hrss.gzlps.gov.cn/gzdt

import sys
sys.path.append('/home/dcb/PycharmProjects/spider')

import re
import json
import requests
from bs4 import BeautifulSoup
from utils.article import Article
from urllib.parse import urljoin


def crawl_article(url, publish_date):
    res = requests.get(url)
    html = res.content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    body_container = soup.find('div', class_='body_container')
    title = body_container.find('div', class_='title').text.strip()
    publish_date = publish_date
    content = []
    for p in body_container.find('div', class_='view').find_all('p'):
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
    print('get article <{}>'.format(url))
    article = Article(title=title, content=content, source=1,
                      publish_organization='六盘水市人力资源和社会保障局', publish_date=publish_date,
                      capture_link=url, area_name='六盘水市', area_code='520200')
    article.push_to_db('table', 'spider_article')


def crawl(from_date='2020-01-01'):
    start_url = 'http://hrss.gzlps.gov.cn/gzdt_42000/gzdt/index.html'
    res = requests.get(start_url)
    html = res.content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    for li in soup.find('ul', class_='list').find_all('li'):
        publish_date = li.find('span').text
        if publish_date < from_date:
            print('complete.')
            break
        url = li.find('a').attrs['href']
        crawl_article(url, publish_date)


if __name__ == '__main__':
    crawl()

