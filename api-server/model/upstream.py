#coding=utf-8

from common import *

class UpstreamModel(CommonModel):

    def add(self, env_id, host, port):
        sql = "insert into upstream(env_id, host, port) values(%s, '%s', %s)" % (
            env_id, host, port)
        return self.update(sql)

    def delete(self, env_id, host, port):
        sql = "delete from upstream where env_id=%s and host='%s' and port=%s" % (
            env_id, host, port)
        return self.update(sql)

    def rows(self, env_id):
        sql  = "select * from upstream where env_id=%s" % env_id
        rows = self.query(sql)
        if rows == None or len(rows) == 0: rows = []
        return rows