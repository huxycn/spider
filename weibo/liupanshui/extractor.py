import re
from datetime import datetime
from bs4 import element


reading_extractor_reg = re.compile(r'\d+')


def extract_title(soup, tag, class_):
    return soup.find(tag, class_=class_).text.strip()


def extract_time(soup, tag, class_, in_format):
    datetime_string = soup.find(tag, class_=class_).text.strip()
    datetime_obj = datetime.strptime(datetime_string, in_format)
    return datetime_obj.strftime('%Y-%m-%d %H:%M')


def extract_reading(soup, tag, class_):
    return int(reading_extractor_reg.findall(soup.find(tag, class_=class_).text)[0])


def extract_content(soup, tag, class_):
    # return '$$'.join(list(soup.find(tag, class_=class_).stripped_strings))

    return '$$'.join(list(soup.find(tag, class_=class_).stripped_strings)).\
        replace('\u200b', '').replace('\xa0', '').strip()


def remove_empty_characters(s):
    return s.replace('\u200b', '').replace('\xa0', '').replace('\u3000', '').replace('\n', '').strip()


def extract_content_with_img(soup, tag, class_):
    param_list = []
    soup = soup.find(tag, class_=class_)
    for t in soup.contents:
        if type(t) == element.NavigableString:
            param_list.append(remove_empty_characters(t))
        else:
            if 'img-box' in t.attrs:
                param_list.append(t.find('img').attrs['src'])
            else:
                param_list.append(remove_empty_characters(t.text))
    param_list = list(filter(lambda x: x, param_list))
    return '$$'.join(param_list)
