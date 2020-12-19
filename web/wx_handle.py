# -*- coding: utf-8 -*-

import web
import os
import datetime
import sys
import time
import xml.etree.ElementTree as ET
import hashlib

import wx_receive
import wx_reply

sys.path.append("../good_price")
from good_price_cn import GoodPriceCalc
import alog
import xueqiu

class WXHandle(object):
    def GET(self):
        try:
            data = web.input()
            alog.debug(data, 'wx_handle::GET', 'input')
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "haojiage" #请按照公众平台官网\基本配置中信息填写

            list = [token.encode('utf-8'), timestamp.encode('utf-8'), nonce.encode('utf-8')]
            list.sort()
            alog.info(list, 'wx_handle::GET', 'list')
            sha1 = hashlib.sha1()
            #map(sha1.update, list)
            for i in list:
                sha1.update(i)
            hashcode = sha1.hexdigest()
            alog.info("handle/GET func: hashcode:"+hashcode+' signature:'+signature, 'wx_handle::GET', 'check')
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception as Argument:
            return Argument

    def POST(self):
        try:
            alog.debug('hello', 'wx_handle', 'WXHandle::POST')
            webData = web.data()
            alog.info("Handle Post webdata is " + str(webData), 'wx_handle', 'WXHandle::POST')
            recMsg = wx_receive.parse_xml(webData)
            if isinstance(recMsg, wx_receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                alog.debug('handle_type:'+recMsg.handle_type, 'WXHandle::POST')
                if recMsg.handle_type == 'goodprice':
                    calc = GoodPriceCalc()
                    price_data = calc.calc(recMsg.Content)
                    content = calc.to_text(price_data, '\n')
                elif 'xueqiu_token' == recMsg.handle_type:
                    xueqiu.set_token('xq_a_token='+recMsg.Content)
                    content = u'设置雪球token成功:' + xueqiu.get_token()
                else:
                    content = u'不支持命令:' + recMsg.Content
                replyMsg = wx_reply.TextMsg(toUser, fromUser, content)
                s = replyMsg.send()
                alog.debug(s, 'wx_handle', 'POST reply')
                return s
            else:
                alog.info('not support', 'WXHandle::POST', u'recMsg.MsgType')
                return "success"
        except Exception as Argment:
            alog.info(Argment, 'WXHandle::POST', u'error')
            return Argment

