# -- coding: utf-8 --
import os
import json
import requests
from requests.exceptions import ProxyError
import time
from random import randint
from headers import headers
from mysql_helper import MysqlHelper
import settings
from proxies import Proxy
import logging
from my_logger import MyLog

logger = MyLog('crawler', logFileBasePath=settings.LOGS_DIR, outputFileLevel=logging.DEBUG).getLogger()

proxies = Proxy()
proxies.gen_proxies_enable("http://m.weibo.cn", 5)


class EmptyContent(Exception):
    def __init__(self):
        self.message = "content is empty"


def get_user_task():
    db = MysqlHelper()
    res = db.get_wb_user("*", [])
    t = []
    for i in res:
        t.append({"uid": i.uid, "status": i.status})
    return t


def craw_user_info(uid, status):
    url = get_wb_user_url(uid)
    print url


def craw_user_post_update(uid):

    db = MysqlHelper()
    last_id = db.get_last_wb_post_id(uid)
    # print last_id
    page = 1
    url = get_wb_post_list_url(uid, page)
    while(True):
        logger.info("crawler %s" % url)
        rsp = send_request(url)
        items = parse_post(rsp)
        max_id = items[2]['weibo_id']
        if len(items) == 0:
            break
        else:
            save_post(items)
            # save_post_file(rsp, uid, page)
            page += 1
            url = get_wb_post_list_url(uid, page)
            if int(max_id) < last_id:
                break
        time.sleep(get_sleep_time())


def craw_user_post_all(uid):

    # to continue set
    if uid == "6065555143":
        page = 241
    else:
        page = 1

    url = get_wb_post_list_url(uid, page)

    while(True):
        logger.info("crawler %s" % url)
        rsp = send_request(url)
        items = parse_post(rsp)
        if len(items) == 0:
            break
        else:
            save_post(items)
            # save_post_file(rsp, uid, page)
            page += 1
            url = get_wb_post_list_url(uid, page)
        time.sleep(get_sleep_time())
    db = MysqlHelper()
    db.upsert_wb_user({"uid": uid, "status": 1})


def get_sleep_time():
    return 1
    # return randint(1, 3)


def get_wb_user_url(uid):
    return "https://weibo.cn/u/" + uid


def get_wb_post_list_url(uid, i):
    return "https://m.weibo.cn/api/container/getIndex?type=uid&value=" + \
           str(uid) + "&containerid=107603" + str(uid) + "&page=" + str(i)


def send_request(url, retry=0):
    retry += 1
    if retry > 3:
        raise
    try:
        proxy = proxies.get_proxy()
        print proxy
        rsp = requests.get(url, headers=headers, proxies=proxy, timeout=5)
    except ProxyError:
        send_request(url, retry)
    else:
        if rsp.status_code == 200:
            try:
                c = json.loads(rsp.text.decode("utf-8"))
                if len(c) == 0:
                    send_request(url, retry)
                return c
            except TypeError:
                send_request(url, retry)
        else:
            raise EmptyContent


def parse_post(content):
    items = []
    for card in content['cards']:
        item = {}
        if card['card_type'] == 9:
            wb_url = card['scheme']
            blog = card['mblog']
            is_origin = 0 if 'retweeted_status' in blog.keys() else 1
            item["weibo_id"] = blog['id']
            item['weibo_uid'] = blog['user']['id']
            item['weibo_cont'] = blog['text']
            item['weibo_img'] = blog.get('thumbnail_pic', "")
            item['weibo_video'] = ''
            item['weibo_url'] = wb_url
            item['weibo_source'] = blog['source']
            item['is_origin'] = is_origin
            item['is_longtext'] = blog['isLongText']
            item['created_at'] = format_time(blog['created_at'])
            item['device'] = ''
            item['repost_num'] = blog['reposts_count']
            item['comment_num'] = blog['comments_count']
            item['praise_num'] = blog['attitudes_count']
            item['comment_crawled'] = 0
            item['repost_crawled'] = 0
            item['repost'] = ''
            if is_origin == 0:
                try:
                    repost = {}
                    repost['created_at'] = format_time(blog['retweeted_status']['created_at'])
                    repost['weibo_id'] = blog['retweeted_status']['id']
                    repost['weibo_cont'] = blog['retweeted_status']['text']
                    repost['thumbnail_pic'] = blog['retweeted_status'].get('thumbnail_pic', "")
                    if blog['retweeted_status'].get('user', None):
                        repost['uid'] = blog['retweeted_status']['user']['id']
                    item['repost'] = json.dumps(repost)
                except Exception, e:
                    logger.error(e)
            if len(blog.get('pics', '')) > 0:
                temp = []
                for pic in blog['pics']:
                    temp.append(pic['pid'])
                item['weibo_pics'] = json.dumps(temp)
            items.append(item)
    return items


def save_post_file(rsp, uid, page):
    file_name = 'u_' + str(uid) + '_p' + str(page) + ".json"
    with open(os.path.join(settings.DATA_DIR, file_name), "w") as f:
        f.write(rsp)


def save_post(items):
    db = MysqlHelper()
    for item in items:
        res = db.upsert_wb_post(item)
        if res:
            logger.debug("weibo post %s be upsert" % item['weibo_id'])
    return


def format_time(post_time):

    # old days
    if "-" in post_time:
        _arr = post_time.split("-")
        if len(_arr) == 2:
            return time.strftime("%Y", time.localtime()) + "-" + post_time
        else:
            return post_time
    # yesterday
    if "昨天".decode('utf-8') in post_time:
        return time.strftime("%Y-%m-%d", time.localtime(time.time() - 86400))

    # today
    return time.strftime("%Y-%m-%d", time.localtime())


def test_file_save_mysql():
    uid = '5667151225'
    for i in range(1, 261):
        path = os.path.join(settings.DATA_DIR, 'u_' + uid + '_p' + str(i) + '.json')
        with open(path, "r") as f:
            c = f.read()
            items = parse_post(c)
            save_post(items)


if __name__ == '__main__':
    tasks = get_user_task()
    for user in tasks:
        uid = user['uid']
        status = user['status']
        craw_user_info(uid, status)
        if status == 1:
            craw_user_post_update(uid)
        elif status == 0:
            craw_user_post_all(uid)



