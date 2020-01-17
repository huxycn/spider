#  黔南人力资源社会保障网
# http://rsj.qiannan.gov.cn/gzdt/

import os
import re
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

root = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(root)
from utils.article import Article


def crawl_article(url, publish_date):
    res = requests.get(url)
    html = res.content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    main_container = soup.find('table', id='c')
    trs = main_container.find_all('tr')
    title = trs[1].text.strip()
    content = []
    for p in trs[4].find_all('p'):
        if p.find('img'):
            img_src = urljoin(url, p.find('img').attrs['src'])
            content.append('<img src="{}">'.format(img_src))
            # img_src = '/'.join(url.split('/')[:-1]) + '/' + p.find('img').attrs['src'].split('./')[-1]
            # content.append({'img': img_src})
        else:
            text = p.text.strip()
            if text:
                content.append('<p>{}</p>'.format(text))
                # content.append({'text': text})
    content = '\n'.join(content)
    article = Article(title=title, content=content, source=1,
                      publish_organization='安顺人力资源和社会保障局',
                      publish_date=publish_date,
                      capture_link=url, area_name='安顺市',
                      area_code='520400')
    article.push_to_db('table', 'spider_article')


def crawl(from_date='2020-01-01'):
    start_url = 'http://rsj.anshun.gov.cn/gzdt/xwdt/index.html'
    res = requests.get(start_url)
    html = res.content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    for tr in soup.find('div', class_='default_pgContainer').find_all('tr'):
        print(tr)
        publish_date = tr.find('td', class_='bt_time').text.strip()
        url = tr.find('a').attrs['href']
        print(publish_date, url)

        if publish_date < from_date:
            print('complete.')
            break

        crawl_article(url, publish_date)


if __name__ == '__main__':
    crawl()
