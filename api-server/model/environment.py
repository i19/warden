#coding=utf-8

from common import *

class EnvironmentModel(CommonModel):

    def add(self, project_id, env_name):
        sql = "insert into environment(project_id, name) values(%s, '%s')" % (
            project_id, env_name)
        return self.update(sql)

    def rows(self, project_id):
        sql  = "select * from environment where project_id=%s" % project_id
        rows = self.query(sql)
        if rows == None or len(rows) == 0: rows = []
        return rows

    def delete(self, project_id, env_name):
        sql = "delete from environment where project_id=%s and name='%s'" % (
            project_id, env_name)
        return self.update(sql)

    def setUidRate(self, project_id, env_id, uid_rate):
        sql = "update environment set uid_rate=%s where project_id=%s and id=%s" % (
            uid_rate, project_id, env_id)
        return self.update(sql)

    def load(self, project_id, env_name):
        sql = "select * from environment where project_id=%s and name='%s'" % (
            project_id, env_name)
        rows =  self.query(sql)
        if rows == None or len(rows) == 0: return None
        return rows[0]