import json
import requests
from bs4 import BeautifulSoup


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Cookie': 'SINAGLOBAL=4714091703372.676.1564453952687; SUB=_2AkMqF2lwf8NxqwJRmP4UxG7hbo51ww7EieKcS5irJRMxHRl-yT83qlw_tRB6AZdHnspkQC0FdKN0NqFKi2ycqB0w8hM-; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5RiSxfBmF7FXsBgA9ZV_iT; YF-V5-G0=b588ba2d01e18f0a91ee89335e0afaeb; _s_tentry=-; Apache=5247468294333.337.1577066716671; ULV=1577066716675:4:1:1:5247468294333.337.1577066716671:1573702433344; UOR=,,www.google.com; login_sid_t=f4751fc096eaca74a5ddb63d456f31a6; cross_origin_proto=SSL; Ugrow-G0=7e0e6b57abe2c2f76f677abd9a9ed65d; wb_view_log=1920*12001; YF-Page-G0=bd9e74eeae022c6566619f45b931d426|1578399165|1578399165'
}


def get_html(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        return ''


def get_fm_view_dict(html):
    fm_view_dict = {}
    soup = BeautifulSoup(html, 'lxml')
    script_tags = soup.find_all('script')
    for script_tag in script_tags:
        try:
            json_str = script_tag.text.replace('FM.view(', '').replace(')', '')
            json_obj = json.loads(json_str)
            fm_view_dict[json_obj['domid']] = json_obj['html']
        except Exception as e:
            pass
    return fm_view_dict
