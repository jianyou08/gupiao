# -*- coding:utf-8 -*-
import os
import datetime
import sys
import time
import getopt
import xml.etree.ElementTree as ET
import hashlib
import web
import json

sys.path.append("../good_price")
from good_price_cn import GoodPriceCalc
import alog

class ApiHandle:
    def GET(self):
        try:
            data = web.input()
            codes = data.code
            calc = GoodPriceCalc()
            price_data = calc.calc(codes)
            res = calc.to_json(price_data, 4)
            return res
            return json.dumps(res)
        except Exception as Argument:
            return Argument