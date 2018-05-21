#coding=utf-8

import web
from agileutil.webpy_base import WebPyBase
import agileutil.ip as ip_util

class CommonController(WebPyBase):
    
    def isValidPort(self, port):
        try:
            port = int(port)
        except:
            return False
        if port >= 0 and port <= 65535:
            return True
        else:
            return False

    def isValidIp(self, ip):
        return ip_util.is_invalid_ip(ip)