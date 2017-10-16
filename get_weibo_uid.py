# coding:utf-8

from mysql_helper import MysqlHelper
import json


def get_uid():
    db = MysqlHelper()
    users = db.get_wb_user("*", ["uid is null"])
    print len(users)
    for user in users:
        if not user.search_data:
            continue
        name = user.name
        data = json.loads(user.search_data)
        try:
            group = data["cards"][1]['card_group']
            if len(group) > 0:
                for u in group:
                    print u['user']['screen_name']
                    if u['user']['screen_name'].encode("utf-8") == name.encode("utf-8"):
                        uid = u['user']['id']
                        print uid
                        db.upsert_wb_user_by_name({"name": name, "uid": uid})
                        print("success update uid for name %s" % name)
                        break
        except Exception:
            pass

if __name__ == '__main__':
    get_uid()
