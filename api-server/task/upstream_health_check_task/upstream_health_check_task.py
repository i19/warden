#coding=utf-8

import requests
import cache as cache
import sys
sys.path.append('../')
sys.path.append('../../')
from multiprocessing import Process
from decouple import config
from agileutil.log import Log
import time
from model.group import GroupModel
from model.project import ProjectModel
from model.environment import EnvironmentModel
from model.upstream import UpstreamModel

log = Log(config('UPSTREAM_CHECK_LOG_FILE'))

def set_resty_upstream(openresty, upstream, oper):
    if openresty == None or upstream == None or oper == None: return
    log.info('ready to call openresty api set upstream %s:%s to %s' % (
        upstream['host'], upstream['port'], upstream['status']
    ))
    host = openresty['host']
    port = openresty['port']
    uri = config('UPSTREAT_RESTY_UP_DOWN_URI')
    url = 'http://%s:%s/%s' % (host, port, uri)
    upstream_host = upstream['host']
    upstream_port = upstream['port']
    params = {
        'host' : upstream_host,
        'port' : upstream_port,
        'oper' : oper
    }
    if oper == 'down':
        params['ttl'] = config('UPSTREAM_DISABLE_TTL', cast=int)
    code = 0
    resp = ''
    try:
        r = requests.get(url, data=params, timeout=config('UPSTREAM_CHECK_TIMEOUT', cast=int))
        code = r.status_code
        resp = r.text
    except Exception, ex:
        log.error('http request to set openresty upstream exception, ex:' + str(ex))
        return
    log.info('after send http request to set upstream, url:%s, code:%s, resp:%s' % (
        url, code, resp
    ))
    if code != 200 or resp != 'ok':
        log.error('code != 200, request to set upstream failed')
        return
    else:
        log.info('http request to set openresty upstream succed')

def batch_set_resty_upstream(group, upstream, oper):
    if group == None or upstream == None : return
    if oper not in ['up', 'down']: return
    all_openresty = GroupModel().allOpenrestys(group['id'])
    if len(all_openresty) == 0:
        log.error('group:%s has no openresty', group['name'])
        return
    from gevent import monkey; monkey.patch_socket();import gevent
    greenlets = [gevent.spawn(set_resty_upstream, openresty, upstream, oper) for openresty in all_openresty]
    gevent.joinall(greenlets)
    key = cache.gen_upstream_key(upstream['host'], upstream['port'])
    cache.set(key, upstream['status'])
    log.info('set cache finish')

def do_offline(group, upstream):
    if group == None or upstream == None : return
    batch_set_resty_upstream(group, upstream, 'down')

def do_online(group, upstream):
    if group == None or upstream == None : return
    batch_set_resty_upstream(group, upstream, 'up')

def check_one(upstream):
    host = upstream['host']
    port = upstream['port']
    url = 'http://%s:%s/%s' % (host, port, config('UPSTREAM_CHECK_URI'))
    code = 0
    resp = ''
    try:
        r = requests.get(url, timeout=config('UPSTREAM_CHECK_TIMEOUT', cast=int))
        code = r.status_code
        resp = r.text
    except Exception, ex:
        log.error('http request exception,url:%s ex:%s' % (url, str(ex)))
        upstream['status'] = 'failed'
        return upstream
    log.info('after http request, url:%s, code:%s, resp:%s' % (url, code, resp))
    if str(code)[0:1] not in ['2', '3', '4']:
        log.error('http request failed, url:%s,code:%s, resp:%s' % (url, code, resp))
        upstream['status'] = 'failed'
    else:
        upstream['status'] = 'ok'
    return upstream

def batch_check(upstreams):
    if upstreams == None: return []
    if len(upstreams) == 0: return []
    from gevent import monkey; monkey.patch_socket();import gevent
    greenlets = [gevent.spawn(check_one, upstream) for upstream in upstreams]
    gevent.joinall(greenlets)
    upstreams = [greenlet.value for greenlet in greenlets]
    return upstreams

def upstream_check():
    groupModel = GroupModel()
    groups = groupModel.rows()
    for group in groups:
        #这里返回ip,port去重后的结果
        all_upstreams = groupModel.allUpstreams(group['id'])
        #协程批量curl,填充请求结果
        all_upstreams = batch_check(all_upstreams)
        for upstream in all_upstreams:
            key = cache.gen_upstream_key(upstream['host'], upstream['port'])
            status = cache.get(key)
            if status == '':
                if upstream['status'] == 'failed':
                    do_offline(group, upstream)
                    log.info('set upstream %s:%s status to %s' % (
                        upstream['host'], upstream['port'], upstream['status']
                    ))
            else:
                if status == upstream['status']:
                    continue
                if upstream['status'] == 'failed':
                    do_offline(group, upstream)
                else:
                    do_online(group, upstream)
                log.info('set upstream %s:%s status from %s to %s' % (
                    upstream['host'], upstream['port'], status, upstream['status']
                ))

def run():
    while True:
        log.info('sleep')
        time.sleep(config('UPSTREAM_CHECK_INTVAL', cast=int))
        try:
            log.info('upstream health check begin===')
            upstream_check()
            log.info('upstream health check end===')
        except Exception, ex:
            log.error('global exception:' + str(ex))

def start():
    p = Process(target=run)
    p.start()
    return