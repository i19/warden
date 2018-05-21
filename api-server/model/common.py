#coding=utf-8

import sys
sys.path.append('../')
import db.mysql as mysql

class CommonModel:

    def query(self, sql):
        return mysql.query(sql)

    def update(self, sql):
        return mysql.update(sql)

    def lastrowid(self):
        return mysql.lastrowid()