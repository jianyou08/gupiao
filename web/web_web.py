# -*- coding:utf-8 -*-
import os
import datetime
import sys
import time
import getopt
import xml.etree.ElementTree as ET
import hashlib
import web

import wx_receive
import wx_reply
from wx_handle import *
from api_handle import *


sys.path.append("../good_price")
from good_price_cn import GoodPriceCalc
import alog

debug_mode = False

urls = (
    '/wx', 'WXHandle',
    '/goodprice', 'H5Handle',
    '/api', 'ApiHandle',
)

class H5Handle:
    def GET(self):
        try:
            data = web.input()
            codes = data.code
            calc = GoodPriceCalc()
            price_data = calc.calc(codes)
            b = calc.to_text(price_data, '<br>')
            html = '<html><head><meta charSet="utf-8"/></head><body>' + b + '</body></html>'
            return html
        except Exception as Argument:
            return Argument

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], 'dp:', ['debug', 'port='])
    port = 80
    opts = []
    for opt, arg in opts:
        if opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-d", "--debug"):
            debug(True)
            debug_mode = True
        else:
            print("web.py -p[--port] <port>  -d[--debug]")
            exit(2)
    alog.info(port, '__main__', 'port')
    alog.info(debug_mode, '__main__', 'debug')
    app = web.application(urls, globals())
    app.run()

