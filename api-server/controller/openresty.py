#coding=utf-8

from common import *
import sys
sys.path.append('../')
from model.group import GroupModel
from model.openresty import OpenrestyModel

class Openresty(CommonController):

    def GET(self, group_name):
        group = GroupModel().load(group_name)
        if group == None:
            return self.resp(errno=1, errmsg='no this group')
        group_id = group['id']
        rows = OpenrestyModel().rows(group_id)
        return self.resp(data=rows)

    def PUT(self, group_name, host, port):
        group = GroupModel().load(group_name)
        if group == None:
            return self.resp(errno=1, errmsg='no this group')
        group_id = group['id']
        if self.isValidIp(host) == False:
            return self.resp(errno=2, errmsg='%s is invalid ip' % host)
        if self.isValidPort(port) == False:
            return self.resp(errno=3, errmsg='%s is invalid port' % port)
        try:
            OpenrestyModel().add(group_id, host, port)
        except Exception, ex:
            return self.resp(errno=4, errmsg=str(ex))
        return self.resp()

    def DELETE(self, group_name, host, port):
        group = GroupModel().load(group_name)
        if group == None:
            return self.resp(errno=1, errmsg='no this group')
        group_id = group['id']
        OpenrestyModel().delete(group_id, host, port)
        return self.resp()