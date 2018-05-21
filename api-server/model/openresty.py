#coding=utf-8

from common import *

class OpenrestyModel(CommonModel):

    def add(self, group_id, host, port):
        sql = "insert into openresty(group_id, host, port) values(%s, '%s', %s)" % (
            group_id, host, port)
        return self.update(sql)

    def delete(self, group_id, host, port):
        sql = "delete from openresty where group_id=%s and host='%s' and port=%s" % (
            group_id, host, port)
        return self.update(sql)

    def rows(self, group_id):
        sql = "select * from openresty where group_id=%s" % group_id
        rows = self.query(sql)
        if rows == None or len(rows) == 0: rows = []
        return rows