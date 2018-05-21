#coding=utf-8

from common import *
import sys
sys.path.append('../')
from model.group import GroupModel
from model.project import ProjectModel

class Project(CommonController):

    def GET(self, group_name):
        group = GroupModel().load(group_name)
        if group == None:
            return self.resp(errno=1, errmsg='no this group')
        group_id = group['id']
        rows = ProjectModel().rows(group_id)
        return self.resp(data=rows)

    def PUT(self, group_name, project_name):
        group = GroupModel().load(group_name)
        if group == None:
            return self.resp(errno=1, errmsg='no this group')
        group_id = group['id']
        try:
            ProjectModel().add(group_id, project_name)
        except Exception, ex:
            return self.resp(errno=2, errmsg=str(ex))
        return self.resp()
    
    def DELETE(self, group_name, project_name):
        group = GroupModel().load(group_name)
        if group == None:
            return self.resp(errno=1, errmsg='no this group')
        group_id = group['id']
        ProjectModel().delete(group_id, project_name)
        return self.resp()