from pprint import pprint
from urllib.parse import urljoin
from weibo.liupanshui.crawler import get_article_url_list, get_article


def full_crawl():
    test_start_article_list_page_url = urljoin('https://weibo.com', '/p/1001065114158006/wenzhang')
    article_url_list = get_article_url_list(test_start_article_list_page_url)
    for i, url in enumerate(article_url_list):
        print('{} <{}> {}'.format(i, url, '=' * 30))
        try:
            article = get_article(url)
            pprint(article)
        except Exception as e:
            print(e)
        print()


def increment_crawl():
    pass
