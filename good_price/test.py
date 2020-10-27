#-*-coding:utf-8-*

import codecs
import urllib2
import json
import bs4
import time
import requests
from bs4 import BeautifulSoup

html=u'<table class="quote-info"><tbody><tr><td>最高：<span class="stock-rise">48.69</span></td><td>今开：<span class="stock-fall">48.60</span></td><td>涨停：<span class="stock-rise">58.40</span></td><td>成交量：<span>17.63万手</span></td></tr><tr class="separateTop"><td>最低：<span class="stock-fall">47.20</span></td><td>昨收：<span>48.67</span></td><td>跌停：<span class="stock-fall">38.94</span></td><td>成交额：<span>8.41亿</span></td></tr><tr class="separateBottom"><td>换手：<span>0.52%</span></td><td>盘后量：<span>7手</span></td><td>量比：<span class="stock-fall">0.97</span></td><td>总市值：<span>1961.84亿</span></td></tr><tr><td>振幅：<span>3.06%</span></td><td>盘后额：<span>3.33万</span></td><td>委比：<span class="stock-rise">82.20%</span></td><td>流通值：<span>1626.27亿</span></td></tr><tr><td>市盈率(动)：<span>145.08</span></td><td>市盈率(TTM)：<span>144.25</span></td><td>每股收益：<span>0.33</span></td><td>股息(TTM)：<span>0.11</span></td></tr><tr><td>市盈率(静)：<span>142.27</span></td><td>市净率：<span>20.43</span></td><td>每股净资产：<span>2.33</span></td><td>股息率(TTM)：<span>0.24%</span></td></tr><tr><td>总股本：<span>41.22亿</span></td><td>52周最高：<span>56.09</span></td><td>质押率：<span>56.09</span></td><td>盈利情况：<span>已盈利</span></td></tr><tr><td>流通股：<span>34.17亿</span></td><td>52周最低：<span>25.69</span></td><td>商誉/净资产：<span>37.09%</span></td><td>注册制：<span>否</span></td></tr><tr><td>投票权：<span>无差异</span></td><td>VIE结构：<span>否</span></td><td>货币单位：<span>CNY</span></td></tr></tbody></table>'


soup = BeautifulSoup(html, 'html.parser')

import re
reg = re.compile(u'市盈率.TTM.：')
s1=soup.find(text=u'市盈率(TTM)：')
print s1
print s1.parent()[0].get_text()

reg = re.compile(u'股息.TTM.：')
s1=soup.find(text=u'股息(TTM)：')
print s1
print s1.parent()[0].get_text()

