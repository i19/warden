#coding=utf-8

from common import *
import sys
sys.path.append('../')
from model.group import GroupModel
from model.project import ProjectModel
from model.environment import EnvironmentModel
from model.upstream import UpstreamModel

class Upstream(CommonController):

    def GET(self, group_name, proj_name, env_name):
        group = GroupModel().load(group_name)
        if group == None:
            return self.resp(errno=1, errmsg='no this group')
        group_id = group['id']
        project = ProjectModel().load(group_id, proj_name)
        if project == None:
            return self.resp(errno=2, errmsg='no this project')
        project_id =project['id']
        environment = EnvironmentModel().load(project_id, env_name)
        if environment == None:
            return self.resp(errno=3, errmsg='no this environment')
        env_id = environment['id']
        rows = UpstreamModel().rows(env_id)
        return self.resp(data=rows)

    def PUT(self, group_name, proj_name, env_name, host, port):
        group = GroupModel().load(group_name)
        if group == None:
            return self.resp(errno=1, errmsg='no this group')
        group_id = group['id']
        project = ProjectModel().load(group_id, proj_name)
        if project == None:
            return self.resp(errno=2, errmsg='no this project')
        project_id =project['id']
        environment = EnvironmentModel().load(project_id, env_name)
        if environment == None:
            return self.resp(errno=3, errmsg='no this environment')
        env_id = environment['id']
        if self.isValidIp(host) == False:
            return self.resp(errno=4, errmsg = '%s is invalid ip' % host)
        if self.isValidPort(port) == False:
            return self.resp(errno=5, errmsg='%s is invalid port' % port)
        try:
            UpstreamModel().add(env_id, host, port)
        except Exception, ex:
            return self.resp(errno=6, errmsg=str(ex))
        return self.resp()
    
    def DELETE(self, group_name, proj_name, env_name, host, port):
        group = GroupModel().load(group_name)
        if group == None:
            return self.resp(errno=1, errmsg='no this group')
        group_id = group['id']
        project = ProjectModel().load(group_id, proj_name)
        if project == None:
            return self.resp(errno=2, errmsg='no this project')
        project_id =project['id']
        environment = EnvironmentModel().load(project_id, env_name)
        if environment == None:
            return self.resp(errno=3, errmsg='no this environment')
        env_id = environment['id']
        UpstreamModel().delete(env_id, host, port)
        return self.resp()