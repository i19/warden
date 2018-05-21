#coding=utf-8

from common import *
import sys
sys.path.append('../')
from model.group import GroupModel
from model.project import ProjectModel
from model.environment import EnvironmentModel

class Environment(CommonController):

    def GET(self, group_name, proj_name):
        group = GroupModel().load(group_name)
        if group == None:
            return self.resp(errno=1, errmsg='no this group')
        group_id = group['id']
        project = ProjectModel().load(group_id, proj_name)
        if project == None:
            return self.resp(errno=2, errmsg='no this project')
        project_id =project['id']
        rows = EnvironmentModel().rows(project_id)
        return self.resp(data=rows)

    def PUT(self, group_name, proj_name, env_name):
        group = GroupModel().load(group_name)
        if group == None:
            return self.resp(errno=1, errmsg='no this group')
        group_id = group['id']
        project = ProjectModel().load(group_id, proj_name)
        if project == None:
            return self.resp(errno=2, errmsg='no this project')
        project_id =project['id']
        try:
            EnvironmentModel().add(project_id, env_name)
        except Exception, ex:
            return self.resp(errno=3, errmsg=str(ex))
        return self.resp()
    
    def DELETE(self, group_name, proj_name, env_name):
        group = GroupModel().load(group_name)
        if group == None:
            return self.resp(errno=1, errmsg='no this group')
        group_id = group['id']
        project = ProjectModel().load(group_id, proj_name)
        if project == None:
            return self.resp(errno=2, errmsg='no this project')
        project_id =project['id']
        EnvironmentModel().delete(project_id, env_name)
        return self.resp()

    def POST(self, group_name, proj_name):
        group = GroupModel().load(group_name)
        if group == None:
            return self.resp(errno=1, errmsg='no this group')
        group_id = group['id']
        project = ProjectModel().load(group_id, proj_name)
        if project == None:
            return self.resp(errno=2, errmsg='no this project')
        project_id = project['id']
        all_envs = EnvironmentModel().rows(project_id)
        all_env_names = [ env['name'] for env in all_envs ]
        if len(all_envs) == 0:
            return self.resp(errno=3, errmsg='no environment in this project')
        param_keys = web.input().keys()
        if param_keys == None or len(param_keys) == 0:
            return self.resp(errno=4, errmsg='no envoronment and uid_rate param in request body')
        for param_key in param_keys:
            if param_key not in all_env_names:
                return self.resp(errno=5, errmsg='%s is not in project environment, please check, all env names is:%s' % (
                    param_key, str(all_env_names) ))
        if len(param_keys) != len(all_envs):
            return self.resp(errno=6, errmsg="param count is not equal to this project's environment name count, all env names is:%s" % (
                str(all_env_names) ))
        param_val_sum = 0
        param_vals = web.input().values()
        for param_val in param_vals:
            if '.' in param_val:
                return self.resp(errno=7, errmsg='uid_rate should be interger not float')
            try:
                param_val = int(param_val)
            except Exception, ex:
                return self.resp(errno=8, errmsg='uid_rate should be interger not float')
            if param_val < 0:
                return self.resp(errno=9, errmsg='uid_rate should be more than or equal 0')
            param_val_sum = param_val_sum + param_val
        if param_val_sum != 100:
            return self.resp(errno=10, errmsg='uid_rate sum shoud be 100')
        env_name_id_hash = {}
        for env in all_envs:
            env_id = env['id']
            name = env['name']
            env_name_id_hash[name] = env_id
        envModel = EnvironmentModel()
        for env_name, uid_rate in web.input().items():
            uid_rate = int(uid_rate)
            env_id = env_name_id_hash[env_name]
            envModel.setUidRate(project_id, env_id, uid_rate)
        return self.resp()