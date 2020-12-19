# -*- coding:utf-8 -*-
import os
import datetime
import sys
import time
import xml.etree.ElementTree as ET


def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    xmlData = ET.fromstring(web_data)
    #print(xmlData.find('MsgType'))
    msg_type = xmlData.find('MsgType').text
    if msg_type == 'text':
        return TextMsg(xmlData)
    elif msg_type == 'image':
        return ImageMsg(xmlData)


class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text


class TextMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.ContentRaw = xmlData.find('Content').text.encode("utf-8")
        self.Content = bytes.decode(self.ContentRaw)
        self.handle_type = 'goodprice'
        if self.Content.startswith('xueqiu:') :
            self.handle_type = 'xueqiu_token'
            self.Content = self.Content[7:]
        if self.Content.startswith('note:'): 
            self.handle_type = 'note'
            self.Content = self.Content[5:]


class ImageMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.PicUrl = xmlData.find('PicUrl').text
        self.MediaId = xmlData.find('MediaId').text

