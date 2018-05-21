#coding=utf-8

from common import *
from project import ProjectModel
from environment import EnvironmentModel
from upstream import UpstreamModel
from openresty import OpenrestyModel

class GroupModel(CommonModel):

    def add(self, group_name):
        sql = "insert into `group`(`name`) values('%s')" % group_name
        return self.update(sql)

    def delete(self, group_name):
        sql = "delete from `group` where `name`='%s'" % group_name
        return self.update(sql)

    def rows(self):
        sql = "select * from `group`"
        rows = self.query(sql)
        if rows == None or len(rows) == 0: rows = []
        return rows

    def load(self, group_name):
        sql = "select * from `group` where `name`='%s'" % group_name
        rows = self.query(sql)
        if rows == None or len(rows) == 0: return None
        return rows[0]

    def allUpstreams(self, group_id):
        all_upstreams = []
        projectModel = ProjectModel()
        envModel = EnvironmentModel()
        upstreamModel = UpstreamModel()
        projects = projectModel.rows(group_id)
        host_port_upstream_hash = {}
        for project in projects:
            project_id = project['id']
            envs = envModel.rows(project_id)
            for env in envs:
                env_id = env['id']
                upstreams = upstreamModel.rows(env_id)
                for upstream in upstreams:
                    host = upstream['host']
                    port = upstream['port']
                    keystr = '%s_%s' % (host, port)
                    if host_port_upstream_hash.has_key(keystr):
                        continue
                    host_port_upstream_hash[keystr] = upstream
        if len(host_port_upstream_hash) == 0: return []
        return host_port_upstream_hash.values()

    def allOpenrestys(self, group_id):
        return OpenrestyModel().rows(group_id)