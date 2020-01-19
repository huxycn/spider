import os
import sys
import re
import time
import json
import random
import logging
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup, element
from json.decoder import JSONDecodeError

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.article import Article
from weibo import spider_config

logging.basicConfig(level=logging.INFO)

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    'cookie': 'ALF=1581470966; _T_WM=66105093185; SCF=AgXcvSJlDq_Em0pyh7HbrakjNELjgFmx7BykGudyv3-FHKaHozMzHplJJihgv5wcmiBMfp58zzcxloSha43rt4Y.; SUB=_2A25zGGT4DeThGeNM71ES9i7MyTyIHXVQ4wywrDV6PUJbktANLUX6kW1NSWOYkQRi_KGeF4HD9xgfWIt-GEPsI4Tm; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWO1NK5FUVAcgG1WfVGscq85JpX5K-hUgL.Fo-EShe0So57eo52dJLoI798Uo2Ndf.t; SUHB=04W-zhXBo-ahYN; SSOLoginState=1578898600; MLOGIN=1; XSRF-TOKEN=11b16a; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=oid%3D4448437980321868%26luicode%3D20000061%26lfid%3D4448437980321868%26uicode%3D10000891'
}


def get_std_date(date_string):
    if '刚刚' in date_string:
        date = datetime.now()
    elif '分钟前' in date_string:
        minutes = int(re.findall('\d+', date_string)[0])
        date = datetime.now() - timedelta(minutes=minutes)
    elif '小时前' in date_string:
        hours = int(re.findall('\d+', date_string)[0])
        date = datetime.now() - timedelta(hours=hours)
    elif '昨天' in date_string:
        date = datetime.now() - timedelta(days=1)
    elif len(date_string) <= 5:
        month = int(re.findall('(\d+)-', date_string)[0])
        day = int(re.findall('-(\d+)', date_string)[0])
        date = datetime(year=datetime.now().year, month=month, day=day)
    else:
        year, month, day = [int(item) for item in date_string.split('-')]
        date = datetime(year=year, month=month, day=day)
    return date.strftime('%Y-%m-%d')


def time_cmp(first_time, second_time):
    ret = int(time.strftime("%Y-%m-%d", first_time)) - int(time.strftime("%Y-%m-%d", second_time))
    print('\033[1;35m {} compare to {}: {} \033[0m!'.format(first_time, second_time, ret))
    return ret


def construct_url(config, since_id=None):
    url_schema = 'https://m.weibo.cn/api/container/getIndex?' \
                 'uid={uid}&luicode=10000011&lfid=100103type=0&q={name}&type=uid&value={uid}&containerid={containerid}'
    if since_id is None:
        return url_schema.format(uid=config['uid'], name=config['name'], containerid=config['containerid'])
    else:
        return url_schema.format(uid=config['uid'], name=config['name'], containerid=config['containerid']) + \
               '&since_id={since_id}'.format(since_id=since_id)


def crawl_weibo(weibo_config, from_date='2020-01-01'):
    since_id = None
    stop_flag = False
    while not stop_flag:
        pause_time = random.random() * 3
        print('pause: {}'.format(pause_time))
        time.sleep(pause_time)
        url = construct_url(weibo_config, since_id=since_id)
        print('{:<12}: <{}>'.format('GET', url))
        res = requests.get(url, headers=headers)
        print('{:<12}: <{}>'.format('STATUS_CODE', res.status_code))
        res_json_obj = res.json()
        print(json.dumps(res_json_obj))
        for card in res_json_obj['data']['cards']:
            if 'mblog' in card:
                try:
                    publish_date = get_std_date(card['mblog']['created_at'])
                    if publish_date < from_date:
                        stop_flag = True
                        break
                    html = '<div>{}</div>'.format(card['mblog']['text'])
                    title = []
                    content = []
                    for t in BeautifulSoup(html, 'lxml').find('div').contents:
                        if type(t) == element.NavigableString:
                            title.append(t.strip())
                        else:
                            print(type(t))
                            content.append(str(t))
                    title = ''.join(title)
                    content = ''.join(content)
                    article = Article(title=title,
                                      content=content,
                                      source=2,
                                      publish_organization=card['mblog']['user']['screen_name'],
                                      publish_date=publish_date,
                                      capture_link=card['scheme'],
                                      area_name=weibo_config['area_name'],
                                      area_code=weibo_config['area_code'])
                    print('get article, title: {} publish_date: {}'.format(title, publish_date))
                    article.push_to_db(coll_name='spider_article')
                except JSONDecodeError as jde:
                    print('\n', '=' * 100)
                    print(jde, card)
                    print('=' * 100, '\n')

        if 'since_id' in res_json_obj['data']['cardlistInfo']:
            since_id = res_json_obj['data']['cardlistInfo']['since_id']
        else:
            print('all done.')
            break


if __name__ == '__main__':
    print('===> Start crawling qiandongnan...')
    crawl_weibo(spider_config.qiandongnan)

    print('===> Start crawling liupanshui...')
    crawl_weibo(spider_config.liupanshui)

    print('===> Start crawling anshun...')
    crawl_weibo(spider_config.anshun)

    print('===> Start crawling guizhou...')
    crawl_weibo(spider_config.guizhou)
