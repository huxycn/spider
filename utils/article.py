import time
import json
import uuid
from pymongo import MongoClient


def gen_id():
    return uuid.uuid4().int & (1 << 64) - 1


def current_time():
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))


def connect_db(db_name='table', coll_name='spider_article'):
    client = MongoClient(host='10.10.9.97', port=27017)
    db = client[db_name]
    db.authenticate('table', 'table')
    coll = db[coll_name]
    return coll


class Article(object):
    def __init__(self, title, content, source, publish_organization, publish_date, capture_link, area_name, area_code,
                 comment_count=0, favour_count=0, favorite_count=0, share_count=0, read_count=0, **kwargs):
        self.entity = {
            'title': title,
            'content': content,
            'source': source,
            'publishOrganization': publish_organization,
            'publishDate': publish_date,
            'captureLink': capture_link,
            'captureDate': current_time(),
            'areaName': area_name,
            'areaCode': area_code,
            'commentCount': comment_count,
            'favourCount': favour_count,
            'favoriteCount': favorite_count,
            'shareCount': share_count,
            'readCount': read_count
        }
        for k, v in kwargs.items():
            self.entity[k] = v

    def __str__(self):
        return json.dumps(self.entity)

    def push_to_db(self, db_name='table', coll_name='spider_article'):
        from pprint import pprint
        pprint(self.entity)
        coll = connect_db(db_name, coll_name)
        coll.insert_one(self.entity)


if __name__ == '__main__':
    article = Article(title='title',
                      content='content',
                      source='source',
                      publish_organization='publish_organization',
                      publish_date='publish_date',
                      capture_link='capture_link',
                      area_name='遵义市')
    print(article)


