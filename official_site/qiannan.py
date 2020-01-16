#  黔南人力资源社会保障网
# http://rsj.qiannan.gov.cn/gzdt/


import re
import json
import requests
from bs4 import BeautifulSoup
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
            img_src = '/'.join(url.split('/')[:-1]) + '/' + p.find('img').attrs['src'].split('./')[-1]
            content.append({'img': img_src})
        else:
            text = p.text.strip()
            if text:
                content.append({'text': text})
    print(title)
    print(content)
    article = Article(title=title, content=content, source=1,
                      publish_organization='黔南人力资源和社会保障局', publish_date=publish_date,
                      capture_link=url, area_name='黔南布依族苗族自治州', area_code='522700')
    article.push_to_db('table', 'spider_article')


def crawl(from_date='2020-01-01'):
    start_url = 'http://rsj.qiannan.gov.cn/gzdt/'
    res = requests.get(start_url)
    html = res.content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    for tr in soup.find('div', id='9296').find_all('tr'):
        script = tr.find('script')
        publish_date = re.findall('str_2 = "(.+)";', str(script))[0]
        url = start_url + re.findall('str_1 = "(.*)";', str(script))[0].split('./')[-1]
        print(publish_date, url)

        if publish_date < from_date:
            print('complete.')
            break

        crawl_article(url, publish_date)


if __name__ == '__main__':
    crawl()

