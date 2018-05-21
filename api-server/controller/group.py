#coding=utf-8

from common import *
import sys
sys.path.append('../')
from model.group import GroupModel

class Group(CommonController):

    def GET(self):
        return self.resp(data=GroupModel().rows())

    def PUT(self, group_name):
        try:
            GroupModel().add(group_name)
        except Exception, ex:
            return self.resp(errno=1, errmsg=str(ex))
        return self.resp()

    def DELETE(self, group_name):
        try:
            GroupModel().delete(group_name)
        except Exception, ex:
            return self.resp(errno=1, errmsg=str(ex))
        return self.resp()