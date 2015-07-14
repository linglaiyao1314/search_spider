# -*- coding:utf-8 -*-
__author__ = 'user'

from gevent.wsgi import WSGIServer
from baidurun import app

http_server = WSGIServer(('0.0.0.0', 8888), app)
# http_server = WSGIServer(('127.0.0.1', 5000), app)
http_server.serve_forever()
