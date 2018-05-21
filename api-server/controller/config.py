#coding=utf-8

from common import *
import sys
sys.path.append('../')
import time
import demjson
from model.group import GroupModel
from model.project import ProjectModel
from model.environment import EnvironmentModel
from model.upstream import UpstreamModel
from model.config import generate_config
from model.config import publish_config

class Config(CommonController):

    def POST(self, group_name, proj_name):
        begin = time.time()
        config_str, err = generate_config(group_name, proj_name)
        if err != None:
            return self.resp(errno=1, errmsg=err)
        #print "config_str", config_str
        err = publish_config(group_name, config_str)
        if err != None:
            return self.resp(errno=2, errmsg=err)
        end = time.time()
        usage = end - begin
        return self.resp(errmsg="sync config succed, cost: %s seconds" % int(usage),data=demjson.decode(config_str))        