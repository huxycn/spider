import re
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_article_urls(start_index_url, container_tag, container_attr, item_list_tag, publish_date_rule, from_date):
    page = 0
    up_to_date = False
    while not up_to_date:
        if page == 0:
            index_url = start_index_url
        else:
            index_url = start_index_url.replace('index', 'index_{}'.format(page))
        res = requests.get(index_url)
        html = res.content.decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        container = soup.find(container_tag, container_attr)
        urls = []
        for item in container.find_all(item_list_tag):
            if publish_date_rule == 1:
                publish_date = item.find('td', class_='bt_time').text.strip()
                url = item.find('a').attrs['href']
            elif publish_date_rule == 2:
                publish_date = item.find('span').text.strip()
                url = item.find('a').attrs['href']
            elif publish_date_rule == 3:
                publish_date = item.find_all('td')[1].text.strip()
                url = item.find('a').attrs['href']
            elif publish_date_rule == 4:
                publish_date = item.find_all('td')[2].text.strip()
                url = item.find('a').attrs['href']
            elif publish_date_rule == 5:
                script = item.find('script')
                publish_date = re.findall('str_2 = "(.+)";', str(script))[0]
                url = urljoin(index_url, re.findall('str_1 = "(.+)"', str(script))[0])
            else:
                raise ValueError('publish date rule value error.')

            if publish_date < from_date:
                up_to_date = True
                break
            else:
                urls.append((url, publish_date_rule))
        page += 1

    print('=' * 100)
    logging.warning('  Get Article Urls  : {}'.format(start_index_url))
    logging.warning('  Article Urls count: {}'.format(len(urls)))
    for url, publish_date_rule in urls:
        logging.warning('  Publish Date/Url  : {} / {}'.format(publish_date, url))
    print('=' * 100)
    print()
    return urls


def get_guizhou_atricle_urls(start_index_url, from_date='2020-01-01'):
    return get_article_urls(start_index_url,
                            container_tag='div',
                            container_attr={'class': 'default_pgContainer'},
                            item_list_tag='tr',
                            publish_date_rule=1,
                            from_date=from_date)


def get_guiyang_article_urls(start_index_url, from_date='2020-01-01'):
    return get_article_urls(start_index_url,
                            container_tag='table',
                            container_attr={'id': 'ajaxpage-list'},
                            item_list_tag='tr',
                            publish_date_rule=3,
                            from_date=from_date)


def get_liupanshui_article_urls(start_index_url, from_date='2020-01-01'):
    return get_article_urls(start_index_url,
                            container_tag='ul',
                            container_attr={'class': 'list'},
                            item_list_tag='li',
                            publish_date_rule=2,
                            from_date=from_date)


def get_zunyi_article_urls(start_index_url, from_date='2020-01-01'):
    return get_article_urls(start_index_url,
                            container_tag='div',
                            container_attr={'class': 'NewsList'},
                            item_list_tag='li',
                            publish_date_rule=2,
                            from_date=from_date)


def get_anshun_article_urls(start_index_url, from_date='2020-01-01'):
    return get_article_urls(start_index_url,
                            container_tag='div',
                            container_attr={'class': 'default_pgContainer'},
                            item_list_tag='tr',
                            publish_date_rule=4,
                            from_date=from_date)


def get_tongren_article_urls(start_index_url, from_date='2020-01-01'):
    return get_article_urls(start_index_url,
                            container_tag='div',
                            container_attr={'class': 'default_pgContainer'},
                            item_list_tag='tr',
                            publish_date_rule=5,
                            from_date=from_date)


def get_bijie_article_urls(start_index_url, from_date='2020-01-01'):
    return get_article_urls(start_index_url,
                            container_tag='div',
                            container_attr={'class': 'default_pgContainer'},
                            item_list_tag='tr',
                            publish_date_rule=3,
                            from_date=from_date)


def get_qiandongnan_article_urls(start_index_url, from_date='2020-01-01'):
    return get_article_urls(start_index_url,
                            container_tag='div',
                            container_attr={'class': 'default_pgContainer'},
                            item_list_tag='tr',
                            publish_date_rule=5,
                            from_date=from_date)


def get_qiannan_article_urls(start_index_url, from_date='2020-01-01'):
    return get_article_urls(start_index_url,
                            container_tag='div',
                            container_attr={'class': 'default_pgContainer'},
                            item_list_tag='tr',
                            publish_date_rule=5,
                            from_date=from_date)


if __name__ == "__main__":
    guihzou_start_index_url = 'http://rst.guizhou.gov.cn/gzdt/xwdt/index.html'
    get_guizhou_atricle_urls(guihzou_start_index_url)

    guiyang_start_index_url = 'http://rsj.guiyang.gov.cn/zxzx/zxzxgzdt/zxzxgzdtyw/index.html'
    guiyang_start_index_url2 = 'http://rsj.guiyang.gov.cn/dwgk4036/dwgk4036dwgknr/dwgk4036dwgknrgzdt/index.html'
    get_guiyang_article_urls(guiyang_start_index_url)
    get_guiyang_article_urls(guiyang_start_index_url2)

    liupanshui_start_index_url = 'http://hrss.gzlps.gov.cn/gzdt_42000/gzdt/index.html'
    get_liupanshui_article_urls(liupanshui_start_index_url)

    zunyi_start_index_url = 'http://rsj.zunyi.gov.cn/gzdt/ywdt/index.html'
    get_zunyi_article_urls(zunyi_start_index_url)

    anshun_start_index_url = 'http://rsj.anshun.gov.cn/gzdt/xwdt/index.html'
    get_anshun_article_urls(anshun_start_index_url)

    tongren_start_index_url = 'http://rsj.trs.gov.cn/gzdt/xwdt/index.html'
    get_tongren_article_urls(tongren_start_index_url)

    bijie_start_index_url = 'http://rsj.bijie.gov.cn/gzdt/index.html'
    # get_bijie_article_urls(bijie_start_index_url)

    qiandongnan_start_index_url = 'http://rsj.qdn.gov.cn/gzdt/xwdt/index.html'
    get_qiandongnan_article_urls(qiandongnan_start_index_url)

    qiannan_start_index_url = 'http://rsj.qiannan.gov.cn/gzdt/index.html'
    get_qiannan_article_urls(qiannan_start_index_url)
