import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_html(url):
    res = requests.get(url)
    html = res.content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    return soup



def crawl_article_rule_1(url):
    soup = get_html(url)
    article_container = soup.find('div', id='c')
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
    print(title, content)


def crawl_article_rule_2(url):



if __name__ == "__main__":
    guizhou_url_example = 'http://rst.guizhou.gov.cn/gzdt/xwdt/202001/t20200116_43328705.html'
    guiyang_url_example = 'http://rsj.guiyang.gov.cn/zxzx/zxzxgzdt/zxzxgzdtyw/202001/t20200117_43529798.html'
    crawl_article_rule_1(guiyang_url_example)
