#coding=utf-8

from agileutil.cache import Cache
from decouple import config

cache_ins = Cache(config('UPSTREAM_CACHE_FILE'))

def gen_upstream_key(host, port):
    keystr = 'upstream_node_%s_%s' % (host, port)
    return keystr

def get(k):
    v = cache_ins.get(k)
    if v == None: v = ''
    return v

def set(k, v):
    return cache_ins.set(k, v)