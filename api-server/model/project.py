#coding=utf-8

from common import *

class ProjectModel(CommonModel):

    def add(self, group_id, project_name):
        sql = "insert into project(group_id, name) values(%s, '%s')" % (
            group_id, project_name)
        return self.update(sql)

    def delete(self, group_id, project_name):
        sql = "delete from project where group_id=%s and name='%s'" % (
            group_id, project_name)
        return self.update(sql)

    def rows(self, group_id):
        sql = "select * from project where group_id=%s" % group_id
        rows = self.query(sql)
        if rows == None or len(rows) == 0: rows = []
        return rows

    def load(self, group_id, project_name):
        sql = "select * from project where group_id=%s and name='%s'" % (group_id, project_name)
        rows = self.query(sql)
        if rows == None or len(rows) == 0: return None
        return rows[0]

    def setSpecialEnv(self, project_id, spec_env_name):
        sql = "update project set spec_env='%s' where id=%s" % (
            spec_env_name, project_id)
        return self.update(sql)

    def setSpecUid(self, project_id, spec_uid_str):
        sql = "update project set spec_uids='%s' where id=%s" % (
            spec_uid_str, project_id)
        return self.update(sql)

    def setNoUidEnv(self, project_id, no_uid_env_name):
        sql = "update project set no_uid_env='%s' where id=%s" % (
            no_uid_env_name, project_id)
        return self.update(sql)
        