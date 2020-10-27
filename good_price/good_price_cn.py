#-*-coding:utf-8-*

import codecs
import urllib2
import json
import bs4
import time
import requests
from interval import Interval
import sys
sys.path.append("../fox_data")
import szse
import chinabond
import xueqiu

CN_symbol = u'代码'
CN_name = u'名称'
CN_pe_ttm = u'ttm市盈率'
CN_dividend = u'ttm股息'
CN_dividend_yield = u'ttm股息率'
CN_current = u'最新价格'
CN_high52w = u'52周最高价'
CN_low52w = u'52周最低价'

def print_json(js, info ='', support_cn = True):
    if len(info) > 0:
        info += ': '
    if js is None:
        print info,"is None"
    else:
        if support_cn:
            print info + json.dumps(js, encoding='UTF-8', ensure_ascii=False, sort_keys=True)
        else:
            print info,js

def req_quote_ttm(symbol):
    xueqiu.set_token('xq_a_token=3242a6863ac15761c18a8469b89065b03bd5e164')
    resp = xueqiu.fetch(symbol, 'quote_detail', params={})
    #jsresp = json.loads(resp, encoding='utf-8')
    print_json(resp, 'xueqiu.fetch quote_detail:'+symbol)
    quote=resp['data']['quote']
    data = {CN_symbol:symbol}
    data[CN_name] = quote['name']
    data[CN_current] = str(quote['current'])
    data[CN_pe_ttm] = str(quote['pe_ttm'])
    data[CN_dividend] = str(quote['dividend'])
    data[CN_dividend_yield] = str(quote['dividend_yield'])
    data[CN_high52w] = str(quote['high52w'])
    data[CN_low52w] = str(quote['low52w'])
    return data

CN_chinabond10 = u'10年期国债收益率'
CN_szpe = u'深证A股平均市盈率'
#CN_symbol = u'代码'
#CN_name = u'名称'
#CN_pe_ttm = u'ttm市盈率'
#CN_dividend = u'ttm股息'
#CN_dividend_yield = u'ttm股息率'
#CN_current = u'最新价格'
#CN_high52w = u'52周最高价'
#CN_low52w = u'52周最低价'
CN_goodbuy_pe15 = u'买入好价-15倍市盈率'
CN_goodbuy_cb10 = u'买入好价-10年期国债收益'
CN_normalbuy_pe25 = u'买入合理价格-25倍市盈率'
CN_sell_pe = u'卖出好价-50倍市盈率'
CN_sell_dividend = u'卖出好价-股息率计算'
CN_ratio_buy_current = u'收益率-当前价买入'
CN_buy_info = u'是否可买入'
CN_sell_info = u'是否可卖'

def calc_good_price(chinabond10, szpe, symbol, ttm_data):
    data = ttm_data
    data[CN_chinabond10] = "%.3f%%" % (chinabond10*100)
    data[CN_szpe] = str(szpe)
    current = float(ttm_data[CN_current])
    pe_ttm  = float(ttm_data[CN_pe_ttm])
    dividend  = float(ttm_data[CN_dividend])
    dividend_yield = float(ttm_data[CN_dividend_yield][:-1]) / 100
    #print pe_ttm,ttm_data[CN_pe_ttm]
    if (pe_ttm <= 0.001) or (dividend <= 0.001) :
        return data
    buy_good_price = 0.0
    buy_good_price_h = 0.0
    #buy-好价:通过市盈率计算好价格，X=15 *（当前股价 / 个股TTM市盈率）
    buy_good_price = 15 * current / pe_ttm
    data[CN_goodbuy_pe15] = "%.2f" % (buy_good_price)
    #buy-好价:通过股息率计算好价格，X=每股股息 /十年期国债收益率 
    goodbuy_cb10 = dividend / chinabond10
    data[CN_goodbuy_cb10] = "%.2f" % (goodbuy_cb10)
    if buy_good_price > goodbuy_cb10:
        buy_good_price_h = buy_good_price
        buy_good_price = goodbuy_cb10
    else:
        buy_good_price_h = goodbuy_cb10
    #buy-正常价:通过市盈率计算好价格，X=25 *（当前股价 / 个股TTM市盈率）
    buy_normal = 25 * current / pe_ttm
    data[CN_normalbuy_pe25] = "%.2f" % (buy_normal)
    #sell:通过市盈率计算好价格，X=50 *（当前股价 / 个股TTM市盈率）
    sell_price = 50 * current / pe_ttm
    data[CN_sell_pe] = "%.2f" % (sell_price)
    #sell:通过股息率计算好价格，X=每股股息 / (十年期国债收益率÷3)
    sell_price1 = goodbuy_cb10 * 3
    data[CN_sell_dividend] = "%.2f" % (sell_price1)
    if sell_price < sell_price1:
        sell_price = sell_price1

    #收益率:按照当前价购买
    ratio = (sell_price - current) / current
    data[CN_ratio_buy_current] = "%.2f%%" % (ratio * 100)
    print_json(data)

    '''购买条件判断:两个条件同时满足时即可买入
    1、 深证 A 股的市盈率小于 20 且目标公司股票的 TTM 市盈率小于 15；
    2、 动态股息率大于 10 年期国债收益率。
    '''
    info = u''
    def level(levels, v):
        lv = 0
        for (a,b) in levels:
            lv += 1
            if v in Interval(a,b):return lv
    level_list = []
    #市场风险
    market_intervals = [(1,20), (20,30), (30, 40), (40,60), (60,1000), (-100, 0)]
    level_szpe = level(market_intervals, szpe)
    level_list.append((level_szpe, u'市场风险'))

    #该股市盈率风险
    pettm_intervals = [(1,20), (20,30), (30, 40), (40,60), (60,1000), (-100, 0)]
    level_ttmpe = level(pettm_intervals, pe_ttm)
    level_list.append((level_ttmpe, u'市盈率风险'))

    #价格风险
    price_intervals = [(0,buy_good_price), (buy_good_price,buy_good_price_h), (buy_good_price_h, buy_normal), (buy_normal, sell_price), (sell_price, sell_price*10)]
    level_price = level(price_intervals, current)
    level_list.append((level_price, u'价格风险'))

    #动态股息风险(公司盈利情况)
    if dividend_yield > chinabond10:
        level_dividend = 1
        level_list.append((level_dividend, u'公司盈利风险(动态股息率)'))
    elif dividend_yield < chinabond10/3:
        level_dividend = 5
        level_list.append((level_dividend, u'公司盈利风险(动态股息率)'))

    #print_json(dividend_intervals)
    #print_json(level_list)
    lv_avg = sum([l for (l,t) in level_list if l is not None]) / len(level_list)
    lv_max = max([l for (l,t) in level_list if l is not None])
    if (lv_avg <= 2 and lv_max <=2) or (dividend_yield > chinabond10 and szpe < 20 and pe_ttm < 16):
        info = u'%d:买，低风险，可以考虑购买 ' % (lv_avg)
    elif (lv_avg < 4):
        info = u'%d:观望，中风险，可以继续观望 ' % (lv_avg)
    else:
        info = u'%d:观望，高风险,等待好价格 ' % (lv_avg)
    for (l,t) in level_list:
        info += t + "(%d);"  % l
    #info += '-'.join([[t for (l,t) in level_list]])

    data[CN_buy_info] = info

    '''卖出条件判断:当【深证A股的市盈率】>60 或  该股【ttm市盈率】>50  或 【ttm股息】< 【10年期国债收益率】的1/3    都是卖出的好时机
    1.目标公司市盈率50倍以上，深证A股市盈率60倍左右
    2.动态股息率小于10年期国债收益率三分之一
    3.目标公司有变坏的迹象
    '''
    info = u''
    if szpe >= 60 or pe_ttm > 50 or dividend < chinabond10/3:
        info = u'卖:赶紧卖，达到最佳卖点'
    else:
        if szpe >= 50 or pe_ttm > 40:
            info = u'减仓：高风险'
        elif szpe >= 40 or pe_ttm > 35:
            info = u'适当建仓:中等风险'
        else:
            info = u'继续持有'
    data[CN_sell_info] = info
    print_json(data)
    return data

CVS_TITLES = [CN_chinabond10, CN_szpe, CN_symbol, CN_name, CN_pe_ttm, CN_dividend, CN_dividend_yield, CN_current, CN_high52w, CN_low52w,
            CN_goodbuy_pe15, CN_goodbuy_cb10, CN_normalbuy_pe25, 
            CN_sell_pe, CN_sell_dividend, 
            CN_ratio_buy_current,
            CN_buy_info, CN_sell_info]
def save_to_cvs(fo, symbol, itemdata = {}):
    #print_json(itemdata, symbol, support_cn=False)
    if len(itemdata) == 0:
        fo.write(symbol + u'\n')
    for key in CVS_TITLES:
        if (itemdata is not None) and (key in itemdata.keys()):
            fo.write(itemdata[key])
        fo.write(',')
    fo.write('\n')
    fo.flush()

def req_quote(quote_list):
    chinabond10 = chinabond.chinabond()
    chinabond10 = chinabond10 / 100
    print 'chinabond10:',chinabond10
    szpe = szse.szse_value()
    print 'szpe:',szpe
    fo = codecs.open('good_price.csv', 'w+', encoding='gbk')
    #fo.write(CN_chinabond10 + ',' + "%.3f%%\n" % (chinabond10*100))
    #fo.write(CN_szpe + ',' + str(szpe) + '\n')
    fo.write(','.join(CVS_TITLES) + '\n')
    for (code, mk, symbol) in quote_list:
        print symbol,'...'
        if True:
            try:
            #if True:
                ttm_data = req_quote_ttm(symbol)
                print_json(ttm_data)
                itemdata = calc_good_price(chinabond10, szpe, symbol, ttm_data)
                save_to_cvs(fo, symbol, itemdata)
            #else:
            except Exception,e1:
                print "[req_quote] error:",e1
                data = {CN_symbol:symbol, CN_szpe:str(szpe), CN_chinabond10:"%.3f%%" % (chinabond10*100)}
                save_to_cvs(fo, symbol, data)
                continue
        else:
            ttm_data = req_quote_ttm(symbol)
            print_json(ttm_data)
            itemdata = calc_good_price(chinabond10, szpe, symbol, ttm_data)
            save_to_cvs(fo, symbol, itemdata)
        time.sleep(2)
    fo.close()
    
def load_quotes(filename='list.txt'):
    quote_list = []
    with open(filename, 'r') as fi:
        for line in fi:
            arr = line.strip('\r').strip('\n').split('.')
            if len(arr) >= 2:
                quote_list.append((arr[0], arr[1], arr[1] + arr[0]))
        fi.close()
    return quote_list

#req_quote([('600519', 'SH', 'SH600030')])
#req_quote([('600519', 'SH', 'SZ000100'), ('600885', 'SH', 'SZ000568'), ('002833', 'SZ', 'SZ002081'), ('002833', 'SZ', 'SZ002613'), ('002833', 'SZ', 'SH600331'), ('002833', 'SZ', 'SH600396'), ('002833', 'SZ', 'SH601318')])
#req_quote([('600519', 'SH', 'SH600519'), ('600885', 'SH', 'SH600885'), ('002833', 'SZ', 'SZ002833')])
req_quote(load_quotes())

print 'finish...'