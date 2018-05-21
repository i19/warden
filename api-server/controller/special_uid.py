#coding=utf-8

from common import *
import sys
sys.path.append('../')
from model.group import GroupModel
from model.project import ProjectModel

class SpecialUid(CommonController):

    def PUT(self, group_name, proj_name, spec_uid_str):
        group = GroupModel().load(group_name)
        if group == None:
            return self.resp(errno=1, errmsg='no this group')
        group_id = group['id']
        projModel = ProjectModel()
        project = projModel.load(group_id, proj_name)
        if project == None:
            return self.resp(errno=2, errmsg='no this priject')
        project_id = project['id']
        spec_uid_list = list( set( [ spec_uid.strip() for spec_uid in spec_uid_str.split(',')] ) )
        try: 
            spec_uid_list.remove('') 
        except: 
            pass
        spec_uid_str = ','.join(spec_uid_list)
        ProjectModel().setSpecUid(project_id, spec_uid_str)
        return self.resp()