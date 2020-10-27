#-*-coding:utf-8-*

import codecs
import json
import time
import requests
import datetime

def http_get(url, headers={}, json_rs = True):
    print 'url:',url
    resp=requests.get(url, headers=headers)
    if resp.status_code != 200:
        print url,resp.status_code
        raise Exception(resp.content)
    if json_rs is True:
        return json.loads(resp.content)
    return resp.content

def http_post(url, headers={}, params={}, json_rs = True):
    resp = requests.post(url, headers=headers, params=params)
    #print r.status_code
    #print r.content
    if resp.status_code != 200:
        print url,resp.status_code
        raise Exception(resp.content)
    if json_rs is True:
        return json.loads(resp.content)
    return resp.content


def dump_str(filename, s):
    with codecs.open(filename, 'w', encoding='utf-8') as f:
        f.write(s)
        f.close()

def dump_json(filename, js):
    with codecs.open(filename, 'w', encoding='utf-8') as f:
        json.dump(js, f, encoding='utf-8', indent=4, ensure_ascii=False)
        f.close()

def load_json(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        js = json.load(f)
        f.close()
        return js
    raise Exception('[load_json] open failed:' + filename)
