# -- encoding:utf-8 --

import base64
import json
import logging
import pickle
import requests
from headers import headers

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.abspath(__file__)))

from my_logger import MyLog
import settings

logger = MyLog('Login', logFileBasePath=settings.LOGS_DIR, outputFileLevel=logging.WARN).getLogger()


def get_cookie_from_login_sina_com_cn(account, password):
    """
    获取一个账号的Cookie
    """
    loginURL = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)"
    username = base64.b64encode(account.encode("utf-8")).decode("utf-8")
    postData = {
        "entry": "sso",
        "gateway": "1",
        "from": "null",
        "savestate": "30",
        "useticket": "0",
        "pagerefer": "",
        "vsnf": "1",
        "su": username,
        "service": "sso",
        "sp": password,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "cdult": "3",
        "domain": "sina.com.cn",
        "prelt": "0",
        "returntype": "TEXT",
    }
    session = requests.Session()
    r = session.post(loginURL, data=postData)
    jsonStr = r.content.decode("gbk")
    info = json.loads(jsonStr)
    if info["retcode"] == "0":
        logger.warning("Get Cookie Success!( Account:%s )" % account)
        cookie = session.cookies.get_dict()
        return json.dumps(cookie)
    else:
        logger.warning("Failed!( Reason:%s )" % info["reason"])
        return ""


def login():
    account = settings.WEIBO_ACCOUNT[0]
    password = settings.WEIBO_ACCOUNT[1]
    cookie = get_cookie_from_login_sina_com_cn(account, password)
    if cookie:
        pickle.dump(cookie, open(path.join(settings.DATA_DIR, 'weibo.pkl'), "w"))


def get_cookie():
    try:
        with open(path.join(settings.DATA_DIR, 'weibo.pkl'), 'r') as f:
            cookie = json.loads(pickle.load(f))
    except IOError, e:
        return ''
    else:
        return cookie


def send_request(url):
    cookie = get_cookie()
    if not cookie:
        return

    rsp = requests.get(url, cookies=cookie, headers=headers, allow_redirects=False)
    print rsp.status_code
    print rsp.history
    print rsp.content.decode("utf-8")
    #return rsp.content.decode("utf-8")


def save_data(content):
    with open(path.join(settings.DATA_DIR, 'res.txt'), "w") as f:
        f.write(content)


if __name__ == "__main__":
    #for i in range(1, 20):
    url = "https://m.weibo.cn/api/container/getIndex?type=uid&value=1753078432&containerid=1076031753078432"
    url = "https://m.weibo.cn/status/4153345382467230"
    send_request(url)

    #content = send_request(url)
    # with open(path.join(settings.DATA_DIR, 'res.txt'), "r") as f:
    #     d = json.loads(f.read())
    #     print len(d)
    #     print d()

