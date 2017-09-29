# -- coding:utf-8 --

import mysql_helper
import time
import re

if __name__ == '__main__':
    db = mysql_helper.MysqlHelper()
    res = db.get_wb_post(["weibo_cont like '%%ins%%'"])
    ins_users = []
    if len(res):
        # print len(res)
        # time.sleep(3)
        pattern = "(.*?)(ins)(\s+|)([\w\.]+)(.*)"
        for p in res:
            words = p.weibo_cont.lower()
            words = re.sub(r'</?\w+[^>]*>', '', words)
            words = words.encode("utf-8").replace(":", "").replace("：", " ") \
                .replace("#", "").replace("主", "").replace("是", "").replace("博", "") \
                .replace("达人", "").replace("@", "").replace("_", "")

            m = re.match(pattern, words)

            if m is not None:
                ins_user = m.group(4)
                if len(ins_user) > 5:
                    ins_users.append({'user_name': ins_user})
                else:
                    pass
                    # print p.id
                    # print words
            else:
                pass
                # print p.id
                # print words

        db = mysql_helper.MysqlHelper()
        for user in ins_users:
            res = db.upsert_ins_user(user)
            print res
