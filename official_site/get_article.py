import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


logging.basicConfig()


def get_title(article_container, rule):
    if rule == 1:
        title = article_container.find(['div', 'td'], class_='title').text.strip()
    elif rule == 2:
        title = article_container.find(['div', 'td'], class_='title').find('h1').text.strip()
    elif rule == 3:
        title = article_container.find_all('tr')[1].text.strip()
    else:
        raise ValueError('rule value list: [1, 2, 3]')
    return title


def get_content(article_container, base_url):
    content_list = []
    for p in article_container.find('div', class_='view').find_all('p'):
        if p.find('img'):
            img_src = urljoin(base_url, p.find('img').attrs['src'])
            content_list.append('<img src="{}">'.format(img_src))
        else:
            text = p.text.strip()
            if text:
                content_list.append('<p>{}</p>'.format(text))
    content = '\n'.join(content_list)
    return content


def get_article(url, container_tag, container_attr, title_rule):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    article_container = soup.find(container_tag, container_attr)
    title = get_title(article_container, title_rule)
    content = get_content(article_container, url)
    print('=' * 100)
    logging.warning('  Get Article: {}'.format(url))
    logging.warning('  Title      : {}'.format(title))
    logging.warning('  Content    : {}...'.format(content[:50]))
    print('=' * 100)
    print()
    return title, content


def get_guizhou_article(url):
    return get_article(url, 'div', {'id': 'c'}, 1)


def get_guiyang_article(url):
    return get_article(url, 'div', {'class': 'Art_left'}, 1)


def get_liupanshui_article(url):
    return get_article(url, 'div', {'class': 'body_container'}, 1)


def get_zunyi_article(url):
    return get_article(url, 'div', {'id': 'c'}, 2)


def get_anshun_article(url):
    return get_article(url, 'table', {'id': 'c'}, 3)


def get_tongren_article(url):
    return get_article(url, 'table', {'id': 'c'}, 3)


def get_bijie_article(url):
    return get_article(url, 'table', {'id': 'c'}, 3)


def get_qiandongnan_article(url):
    return get_article(url, 'div', {'id': 'c'}, 1)


def get_qiannan_article(url):
    return get_article(url, 'table', {'id': 'c'}, 3)


if __name__ == "__main__":
    guizhou_url_example = 'http://rst.guizhou.gov.cn/gzdt/xwdt/202001/t20200116_43328705.html'
    get_guizhou_article(guizhou_url_example)

    guiyang_yaowen_url_example = 'http://rsj.guiyang.gov.cn/zxzx/zxzxgzdt/zxzxgzdtyw/202001/t20200117_43529798.html'
    guiyang_gongzuo_url_example = 'http://rsj.guiyang.gov.cn/dwgk4036/dwgk4036dwgknr/dwgk4036dwgknrgzdt/201911/t20191129_17408646.html'
    get_guiyang_article(guiyang_yaowen_url_example)
    get_guiyang_article(guiyang_gongzuo_url_example)

    liupanshui_url_example = 'http://hrss.gzlps.gov.cn/gzdt_42000/gzdt/202001/t20200114_43050220.html'
    get_liupanshui_article(liupanshui_url_example)

    zunyi_url_example = 'http://rsj.zunyi.gov.cn/gzdt/ywdt/202001/t20200110_42356536.html'
    get_zunyi_article(zunyi_url_example)

    anshun_url_example = 'http://rsj.anshun.gov.cn/gzdt/xwdt/202001/t20200109_42094703.html'
    get_anshun_article(anshun_url_example)

    tongren_url_example = 'http://rsj.trs.gov.cn/ztzl/bwcxljsm/202001/t20200117_43540986.html'
    get_tongren_article(tongren_url_example)

    # bijie_url_example = 'http://rsj.bijie.gov.cn/gzdt/202001/t20200117_43564395.html'
    # get_bijie_article(bijie_url_example)

    qiandongnan_url_example = 'http://rsj.qdn.gov.cn/gzdt/xwdt/202001/t20200110_42351995.html'
    get_qiandongnan_article(qiandongnan_url_example)

    qiannan_url_example = 'http://rsj.qiannan.gov.cn/gzdt/202001/t20200117_43546060.html'
    get_qiannan_article(qiannan_url_example)
