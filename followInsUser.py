#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from InstagramAPI import InstagramAPI
from mysql_helper import MysqlHelper
from random import randint
from settings import INS_ACCOUNT
import time


def follow_by_username(api, userName):
    """
    search username and get user pk, then follow
    """
    try:
        api.searchUsername(userName)
        if api.LastJson:
            uid = api.LastJson['user']['pk']
            res = api.follow(uid)
            return res
    except Exception, e:
        print userName, e


def main():
    db = MysqlHelper()
    items = db.get_ins_user(["status=0"])

    api = InstagramAPI(INS_ACCOUNT['username'], INS_ACCOUNT['password'])
    api.login()  # login

    for item in items:
        if follow_by_username(api, item.user_name):
            print("follow %s success" % item.user_name)
            db.upsert_ins_user({"status": 1, "user_name": item.user_name})
        else:
            print("can not get the user %s" % item.user_name)
            db.upsert_ins_user({"status": -1, "user_name": item.user_name})
        time.sleep(randint(2, 5))


if __name__ == "__main__":
    main()
    # db = MysqlHelper()
    # db.upsert_ins_user({"status": 1, "user_name": "madebytanja"})


