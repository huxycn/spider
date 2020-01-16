import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from weibo.general_utils import get_html, get_fm_view_dict
from weibo.liupanshui.extractor import extract_title, extract_time, extract_reading, extract_content_with_img

weibo_host = 'https://weibo.com'





def get_article(url):
    if 'ttarticle' in url:
        return get_article_new(url)
    else:
        return get_article_old(url)


def get_article_new(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    title = extract_title(soup, 'div', 'title')
    try:
        time = extract_time(soup, 'span', 'time', '%Y-%m-%d')
    except Exception as e:
        pass
    try:
        time = extract_time(soup, 'span', 'time', '%m-%d %H:%M')
    except Exception as e:
        pass
    reading = extract_reading(soup, 'span', 'num')

    try:
        content = extract_content_with_img(soup, 'div', 'WB_editor_iframe_new')
    except Exception as e:
        pass
    try:
        content = extract_content_with_img(soup, 'div', 'WB_editor_iframe')
    except Exception as e:
        pass

    article = {
        'title': title,
        'pub_time': time,
        'reading': reading,
        'content': content,
        'crawled_time': current_time()
    }
    return article


def get_article_old(url):
    html = get_html(url)
    fm_view_dict = get_fm_view_dict(html)
    article_html = fm_view_dict['Pl_Official_CardLongFeedv6__2']
    article_soup = BeautifulSoup(article_html, 'lxml')
    title = extract_title(article_soup, 'h1', 'title')
    pub_time = extract_time(article_soup, 'span', 'time', '%Y年%m月%d日 %H:%M')
    reading = extract_reading(article_soup, 'span', 'num')
    content = extract_content_with_img(article_soup, 'div', 'WBA_content')

    article = {
        'title': title,
        'pub_time': pub_time,
        'reading': reading,
        'content': content,
        'crawled_time': current_time()
    }
    return article


def get_article_url_list_and_next_page_url(article_list_page_url):
    article_url_list = []
    html = get_html(article_list_page_url)
    fm_view_dict = get_fm_view_dict(html)
    target_html = fm_view_dict['Pl_Core_ArticleList__43']

    target_soup = BeautifulSoup(target_html, 'lxml')
    article_list = target_soup.find_all('li', class_='pt_li')
    for article in article_list:
        a = article.find('a', class_='W_autocut')
        article_url = urljoin(weibo_host, a['href'])
        article_url_list.append(article_url)
        print('  get article url <{}>'.format(article_url))
    next_page = target_soup.find_all('a', class_='next')
    try:
        next_page_url = urljoin(weibo_host, next_page[0]['href'])
        print('  get next page url <{}>'.format(next_page_url))
    except Exception as e:
        next_page_url = ''
        print('  No Next Page. {}'.format(e))
    return article_url_list, next_page_url


def get_article_url_list(start_artilce_list_page_url):
    to_crawl_url = start_artilce_list_page_url
    total_article_url_list = []
    counter = 1
    while to_crawl_url:
        print('== Crawl loop [{}]'.format(counter))
        counter += 1
        article_url_list, next_page_url = get_article_url_list_and_next_page_url(to_crawl_url)
        total_article_url_list.extend(article_url_list)
        print('== Crawl loop complete.')
        to_crawl_url = next_page_url
    return total_article_url_list


if __name__ == '__main__':
    from pprint import pprint
    test_url_new = 'https://weibo.com/ttarticle/p/show?id=2309404420706354987086&mod=zwenzhang'
    test_url_old = 'https://weibo.com/p/1001603702080723373561?mod=zwenzhang'
    article = get_article(test_url_old)
    pprint(article)
    article = get_article(test_url_new)
    pprint(article)
