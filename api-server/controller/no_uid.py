#coding=utf-8

from common import *
import sys
sys.path.append('../')
from model.group import GroupModel
from model.project import ProjectModel
from model.environment import EnvironmentModel

class NoUidEnv(CommonController):

    def PUT(self, group_name, proj_name, no_uid_env_name):
        group = GroupModel().load(group_name)
        if group == None:
            return self.resp(errno=1, errmsg='no this group')
        group_id = group['id']
        projModel = ProjectModel()
        project = projModel.load(group_id, proj_name)
        if project == None:
            return self.resp(errno=2, errmsg='no this project')
        project_id = project['id']
        all_envs = EnvironmentModel().rows(project_id)
        all_env_names = [env['name'] for env in all_envs]
        if no_uid_env_name not in all_env_names:
            if no_uid_env_name != '':
                return self.resp(errno=3, errmsg='no this env, please call api set')
        projModel.setNoUidEnv(project_id, no_uid_env_name)
        return self.resp()