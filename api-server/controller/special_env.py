#coding=utf-8

from common import *
import sys
sys.path.append('../')
from model.group import GroupModel
from model.project import ProjectModel
from model.environment import EnvironmentModel

class SpecialEnv(CommonController):

    def PUT(self, group_name, proj_name, spec_env_name):
        group = GroupModel().load(group_name)
        if group == None:
            return self.resp(errno=1, errmsg='no this group')
        group_id = group['id']
        projModel = ProjectModel()
        project = projModel.load(group_id, proj_name)
        if project == None:
            return self.resp(errno=2, errmsg='no this priject')
        project_id = project['id']
        all_envs = EnvironmentModel().rows(project_id)
        if len(all_envs) == 0:
            return self.resp(errno=3, errmsg='now this project has no environment, please add')
        all_env_names = [ env['name'] for env in all_envs ]
        if spec_env_name not in all_env_names and spec_env_name != '':
            return self.resp(errno=4, errmsg="special env name is not in this project's environment")
        projModel.setSpecialEnv(project_id, spec_env_name)
        return self.resp()