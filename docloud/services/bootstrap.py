# coding=utf8

from docloud.core.service import Service

class Bootstrap(Service):
    def ping(self):
        return {'status': True}