#coding=utf-8

import time
import demjson
import agileutil.util as util
from decouple import config
from group import GroupModel
from project import ProjectModel
from environment import EnvironmentModel
from upstream import UpstreamModel
from openresty import OpenrestyModel
import sys
sys.path.append('../')
import logger.logger as logger

def generate_config(group_name, proj_name):
    '''
    生成发布到nginx的配置文件
    成功返回 配置, None
    失败返回 '', 错误信息
    '''
    groupModel = GroupModel()
    projModel = ProjectModel()
    envModel = EnvironmentModel()
    upstreamModel = UpstreamModel()
    group = groupModel.load(group_name)
    if group == None:
        return '', 'no this group'
    group_id = group['id']
    proj = projModel.load(group_id, proj_name)
    if proj == None:
        return '', 'no this project'
    no_uid_env = proj['no_uid_env']
    if no_uid_env == None or no_uid_env == '':
        return '', "project's no_uid_env must be set"
    proj_id = proj['id']
    env_name_node_hash = {}
    all_envs = envModel.rows(proj_id)
    if len(all_envs) == 0:
        return '', 'this project has no environment, please call api set'
    upstream_node_sum = 0 #检查必须有upstream节点
    uid_rate_sum = 0 #检查所有环境的uid_rate之和必须为100
    for env in all_envs:
        env_name = env['name']
        uid_rate = env['uid_rate']
        upstreams = upstreamModel.rows(env['id'])
        if uid_rate > 0:
            if len(upstreams) <= 0:
                return '', 'env %s uid_rate is:%s, but no upstream' % (env_name, uid_rate)
        upstream_node_sum = upstream_node_sum + len(upstreams)
        node = {}
        node['uid_rate'] = uid_rate
        node['upstreams'] = upstreams
        env_name_node_hash[env_name] = node
        uid_rate_sum = uid_rate_sum + uid_rate
    if uid_rate_sum != 100:
        return '', 'all environment uid_rate sum is not equal to 100, please call api set uid_rate'
    if upstream_node_sum <= 0:
        return '', 'no upstream node for every environment, please call api set' 
    spec_env = proj['spec_env']
    spec_uids = proj['spec_uids']
    no_uid_env = proj['no_uid_env']
    if spec_uids == None: spec_uids = ''
    configMap = {
        proj_name: {
            'spec_env': spec_env,
            'spec_uids': spec_uids,
            'envs': env_name_node_hash,
            'no_uid_env' : no_uid_env
        }
    }
    configStr = ''
    try:
        configStr = demjson.encode(configMap)
    except Exception, ex:
        return '', str(ex)
    return configStr, None

def publish_config(group_name, config_str):
    '''
    发布配置到nginx
    成功返回 None
    失败返回 错误信息
    '''
    groupModel = GroupModel()
    openrestyModel = OpenrestyModel()
    group = groupModel.load(group_name)
    if group == None: return 'no this group'
    group_id = group['id']
    openresty_list = openrestyModel.rows(group_id)
    if len(openresty_list) == 0:
        return 'this group has no openresty node, please call api set'
    uri = config('SYNC_CONFIG_URI')
    for resty in openresty_list:
        host = resty['host']
        port = resty['port']
        url = 'http://%s:%s/%s' % (host, port, uri)
        param = {'config' : config_str}
        code, resp = util.http(url, param)
        if code != 200 or resp != 'ok':
            logger.error('publish config failed on openresty %s:%s, http response code:%s, resp:%s' % (host, port, code, resp))
            return 'publish config failed on openresty %s:%s, http response code:%s, resp:%s' % (host, port, code, resp)
        logger.info('publish config succed on openresty %s:%s' % (host, port))
    return None