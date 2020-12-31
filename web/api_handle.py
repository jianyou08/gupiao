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
from good_price_cn import *
import alog

class ApiHandleGoodPrice:
    def GET(self):
        try:
            data = web.input()
            codes = data.code
            user = data.user
            calc = GoodPriceCalc()
            price_data = calc.calc(codes, user=user)
            res = {
                "basic": [
                    [CN_symbol],
                    [CN_name],
                    [CN_pe_ttm],
                    [CN_dividend],
                    [CN_dividend_yield],
                    [CN_low52w],
                    [CN_high52w],
                    [CN_current],
                ],
                "market":[
                    [CN_chinabond10],
                    [CN_szpe],
                ],
                "goodprice": [
                    [CN_normalbuy_pe25],
                    [CN_goodbuy_cb10],
                    [CN_goodbuy_pe15],
                    [CN_sell_pe],
                    [CN_sell_dividend],
                    [CN_buy_info],
                    [CN_sell_info]
                ]
            }
            def add(res, idx, itemdata, group):
                resitem = res[group][idx]
                key = res[group][idx][0]
                #print(group,key,resitem)
                if group not in itemdata:
                    resitem.append('')
                    return
                if key in itemdata[group]:
                    resitem.append(itemdata[group][key])
                else:
                    resitem.append('')
            for (symbol,itemdata) in price_data.items():
                for idx in range(len(res['basic'])):
                    add(res, idx, itemdata, 'basic')
                for idx in range(len(res['market'])):
                    add(res, idx, itemdata, 'market')
                for idx in range(len(res['goodprice'])):
                    add(res, idx, itemdata, 'goodprice')
            #return res
            return json.dumps(res)
        except Exception as Argument:
            return Argument

class ApiHandleHistory:
    def GET(self):
        try:
            data = web.input()
            user = data.user
            if len(user) <= 0:
                return '{"code":1, "info":"需要输出参数user参数"}'
            with codecs.open("data/user/goodprice_history_%s.txt" % (user), 'r', encoding='utf-8') as f:
                hisdata = []
                for line in f:
                    arr = line.strip().strip('\n').split('\t')
                    if len(arr) < 6: continue
                    user        = arr[0]
                    dts         = arr[1]
                    code        = arr[2]
                    gp_name     = arr[3]
                    gp_price    = arr[4]
                    gp_pe_ttm   = arr[5]
                    #user, dts, code, ttm_data[CN_name], ttm_data[CN_current], ttm_data[CN_pe_ttm]
                    hisdata.append([dts,code,gp_name,gp_price,gp_pe_ttm])
                f.close()
                codes = set()
                data = []
                for item in reversed(hisdata):
                    if item[1] in codes: continue
                    if len(data) > 20 : continue
                    codes.add(item[1])
                    data.append(item)
                res = {"code":0, "info":"ok", "data":data}
                return json.dumps(res)
            return '{"code":0, "info":"没有查询到数据", "data":{}}'
            
        except Exception as Argument:
            return Argument