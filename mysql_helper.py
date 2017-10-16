# -- coding : utf-8 -- *
import simplemysql

from settings import MYSQL_CONFIG


class MysqlHelper(object):

    tb_user = "user"
    tb_wb_user = "wb_user"
    tb_wb_post = "wb_post"
    tb_ins_user = "ins_user"

    def __init__(self):
        self.db = simplemysql.SimpleMysql(**MYSQL_CONFIG)

    # get valid user
    def get_valid_users(self):
        return self.db.getAll(self.tb_user, "*", ["enable = 1"])

    # set user invalid
    def disable_user(self, name):
        self.db.update(self.tb_user, {"enbale": 0}, ["name ='" + name + "'"])
        return

    # user is a map type {"name": name , "password": password, "enable": 1}
    def upsert_user(self, user):
        self.db.insertOrUpdate(self.tb_user, user, "name")
        return self.db.lastId()

    def get_wb_user(self, select, condition):
        return self.db.getAll(self.tb_wb_user, select, condition)

    def upsert_wb_user(self, user):
        self.db.insertOrUpdate(self.tb_wb_user, user, "uid")
        self.db.commit()
        return self.db.lastId()

    def upsert_wb_user_by_name(self, user):
        self.db.insertOrUpdate(self.tb_wb_user, user, "name")
        self.db.commit()
        return self.db.lastId()

    def get_last_wb_post_id(self, uid):
        res = self.db.getOne(self.tb_wb_post, ["weibo_id"], ["weibo_uid='" + uid + "'"], ["weibo_id", "desc"])
        # print self.db.lastQuery()
        if res:
            return res.weibo_id
        else:
            return False

    def upsert_wb_post(self, post):
        self.db.insertOrUpdate(self.tb_wb_post, post, "weibo_id")
        self.db.commit()
        return self.db.lastId()

    def get_wb_post(self, condition):
        return self.db.getAll(self.tb_wb_post, "*", condition)

    def get_wb_post_by_keyword(self, keyword):
        sql = "select * from %s where weibo_cont like %s" % (self.tb_wb_post, keyword)
        cur = self.db.query(sql)
        return cur.fentchall()

    def upsert_ins_user(self, user):
        self.db.insertOrUpdate(self.tb_ins_user, user, "id")
        self.db.commit()
        return self.db.lastId()

    def get_ins_user(self, condition):
        return self.db.getAll(self.tb_ins_user, "*", condition)

if __name__ == "__main__":
    db = MysqlHelper()
    # db.get_valid_users()
    # res = db.get_wb_user(condition=["status = 0"])
    # for i in res:
    #     print i

    weibo_id = db.get_last_wb_post_id("5667151225")
    print(weibo_id)
