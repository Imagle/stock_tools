# -*- coding: UTF-8 -*-
import time
import sys
import json
import urllib2
reload(sys)
sys.setdefaultencoding('utf8')

xueqiuHeader = {"Accept": 'application/json, text/javascript, */*; q=0.01',
                 "Referer": 'https: // xueqiu.com / hq',
                 "User-Agent": 'Mozilla / 5.0(Macintosh;Intel Mac OS X 10_14_1) AppleWebKit / 537.36(KHTML, like Gecko) \
                 Chrome / 71.0.3578.98 Safari/537.36',
                 "X-Requested-With": 'XMLHttpRequest',
                 "Cookie": '__utmz=1.1521689062.37.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _ga=GA1.2.2022971702.1507098243; device_id=7912987cc1acb87793b6a39ac3f56509; s=ep120643by; bid=9f1e4b7c1bf25a9ee495aee5366eb4dd_jo1cumta; aliyungf_tc=AQAAAGyK+jSkmQ4A0+YCaibkXpaa9LOQ; Hm_lvt_1db88642e346389874251b5a1eded6e3=1544851645,1545271068,1546251974,1547359277; _gid=GA1.2.145758004.1547359277; __utma=1.2022971702.1507098243.1546531445.1547359282.62; __utmc=1; __utmt=1; snbim_minify=true; _gat_gtag_UA_16079156_4=1; xq_a_token=243bb1cce89c8d4d365a26452e50d6e62b83db37; xq_a_token.sig=f-qBQHaLY5XWBkok8dfHMwfvPh8; xq_r_token=ad975892bb77cd4b31f5b18209607d808244bdc6; xq_r_token.sig=pvTbFtrQT8yyrLiTwRhbZ1iQYxg; u=461547359804327; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1547359808; __utmb=1.3.10.1547359282'
                }

def getNetValueFactor(net_value, net_value_5d):
    print "Begin to 计算净值因子..."
    net_value_factor = 0
    J = net_value - net_value_5d
    if J > 0.01:
        net_value_factor = 4
    elif  J < 0.01 and J > -0.01:
        net_value_factor = 3
    elif J < -0.01:
        net_value_factor = 2
    print "    Success 计算净值因子，FACTOR[%s]" % net_value_factor
    return net_value_factor

def getIndexFactor():
    print "Begin to get 指数 Data..."
    print "    Begin to get 上证50 Data..."
    #上证50(SH:000016)
    stock = 'SH000016'
    index_A50 = getIndexData(stock)
    print "    Begin to get 沪深300 Data..."
    #沪深300, SH000300
    stock = 'SH000300'
    index_300 = getIndexData(stock)
    print "    Begin to get 中证500 Data..."
    #中证500(SH:000905)
    stock = 'SH000905'
    index_500 = getIndexData(stock)
    print "    Begin to get 创业板 Data..."
    #创业板(SZ:159915)
    stock = 'SZ159915'
    index_cyb = getIndexData(stock)
    print "    Begin to get 上证指数 Data..."
    #上证指数(SH:000001)
    stock = 'SH000001'
    index_001 = getIndexData(stock)

    index_factor = calMa(index_A50, index_300, index_500, index_cyb, index_001)
    print "    Success 计算指数因子，FACTOR[%s]" % index_factor
    return index_factor

def calMa(index_50, index_300, index_500, index_cyb, index_001):
    index_factor = 0
    diff_5d_50 = index_50[1][1] - index_50[0][1]
    diff_20d_50 = index_50[1][3] - index_50[0][3]

    diff_5d_300 = index_300[1][1] - index_300[0][1]
    diff_20d_300 = index_300[1][3] - index_300[0][3]

    diff_5d_500 = index_500[1][1] - index_500[0][1]
    diff_20d_500 = index_500[1][3] - index_500[0][3]

    diff_5d_cyb = index_cyb[1][1] - index_cyb[0][1]
    diff_20d_cyb = index_cyb[1][3] - index_cyb[0][3]

    diff_5d_001 = index_001[1][1] - index_001[0][1]
    diff_20d_001 = index_001[1][3] - index_001[0][3]

    if diff_5d_50 > 0 and diff_5d_300 > 0 and diff_5d_500 > 0 and diff_5d_cyb > 0 and diff_5d_001 > 0:
        index_factor += 1
    if diff_20d_50 > 0 and diff_20d_300 > 0 and diff_20d_500 > 0 and diff_20d_cyb > 0 and diff_20d_001 > 0:
        index_factor += 2
    print "    5日线 : 50[%s], 300[%s], 500[%s], cyb[%s], 001[%s]" % (diff_5d_50, diff_5d_300, diff_5d_500, diff_5d_cyb, diff_5d_001)
    print "    20日线: 50[%s], 300[%s], 500[%s], cyb[%s], 001[%s]" % (diff_20d_50, diff_20d_300, diff_20d_500, diff_20d_cyb, diff_20d_001)

    return index_factor

def getIndexData(stock):
    now = int(time.time()) * 1000
    url = '''https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=%s&begin=%s&period=day&type=before&count=-2&indicator=ma''' % (stock, now)
    contents = urllib2.urlopen(urllib2.Request(
        url,
        headers = xueqiuHeader
    )).read()
    contents = json.loads(contents)
    return contents['data']['item']

def getPercentFactor():
    print "Begin to get 涨跌幅 Data..."
    print "    Begin to get ZhangTing Data..."
    now = int(time.time())
    url = "https://xueqiu.com/stock/cata/stocklist.json?page=1&size=100&order=desc&orderby=percent&type=11%2C12&_=" + str(now)
    contents = urllib2.urlopen(urllib2.Request(
        url,
        headers = xueqiuHeader
    )).read()
    contents = json.loads(contents)
    #print "    Success for getting ZhangTing Data..."
    #print "    Begin to analyse ZhangTing Data..."
    zhangting_num = 0
    zhangting_factor = 0
    for stock in contents['stocks']:
        percent = float(stock['percent'])
        if percent > 9.9:
            zhangting_num += 1
    if zhangting_num > 30:
        zhangting_factor = 0.5
    if zhangting_num > 50:
        zhangting_factor += 0.5
    if zhangting_num >= 100:
        zhangting_factor += 0.5
    if zhangting_num > 200:
        zhangting_factor += 0.5
    #print "    Success for analysing ZhangTing Data, NUM[%s], Factor[%s]..." % (zhangting_num, zhangting_factor)
    print "    Begin to get DieTing Data..."
    now = int(time.time())
    url = "https://xueqiu.com/stock/cata/stocklist.json?page=1&size=101&order=asc&orderby=percent&type=11%2C12&_=" + str(now)
    contents = urllib2.urlopen(urllib2.Request(
        url,
        headers = xueqiuHeader
    )).read()
    contents = json.loads(contents)
    #print "    Success for getting DieTing Data..."
    #print "    Begin to analyse Dieting Data..."
    dieting_num = 0
    for stock in contents['stocks']:
        percent = float(stock['percent'])
        if percent < -9.9:
            dieting_num += 1
    #print "    Success for analysing DieTing Data, Z_NUM[%s], D_NUM[%s]..." % (zhangting_num, dieting_num)
    if dieting_num > zhangting_num:
        zhangting_factor += -1
    print "    Success 计算涨跌幅: 涨停[%s], 跌停[%s], FACTOR[%s]..." % (zhangting_num, dieting_num, zhangting_factor)
    return zhangting_factor

def getVolumeFactor():
    print "Begin to get 交易量 Data..."
    now = int(time.time())
    url = "https://xueqiu.com/stock/quote_order.json?page=1&size=100&order=desc&exchange=CN&stockType=sha&column=symbol%2Cname%2Ccurrent%2Cchg%2Cpercent%2Clast_close%2Copen%2Chigh%2Clow%2Cvolume%2Camount%2Cmarket_capital%2Cpe_ttm%2Chigh52w%2Clow52w%2Chasexist&orderBy=volume&_=" + str(now)
    contents = urllib2.urlopen(urllib2.Request(
        url,
        headers = xueqiuHeader
    )).read()
    contents = json.loads(contents)
    sha_stocks = contents['data']
    print "    Success for getting 沪市交易量..."

    url = "https://xueqiu.com/stock/quote_order.json?page=1&size=100&order=desc&exchange=CN&stockType=sza&column=symbol%2Cname%2Ccurrent%2Cchg%2Cpercent%2Clast_close%2Copen%2Chigh%2Clow%2Cvolume%2Camount%2Cmarket_capital%2Cpe_ttm%2Chigh52w%2Clow52w%2Chasexist&orderBy=volume&_=" + str(now)
    contents = urllib2.urlopen(urllib2.Request(
        url,
        headers = xueqiuHeader
    )).read()
    contents = json.loads(contents)
    sza_stocks = contents['data']
    print "    Success for getting 深市交易量..."

    url = "https://xueqiu.com/stock/quote_order.json?page=1&size=100&order=desc&exchange=CN&stockType=cyb&column=symbol%2Cname%2Ccurrent%2Cchg%2Cpercent%2Clast_close%2Copen%2Chigh%2Clow%2Cvolume%2Camount%2Cmarket_capital%2Cpe_ttm%2Chigh52w%2Clow52w%2Chasexist&orderBy=volume&_=" + str(
        now)
    contents = urllib2.urlopen(urllib2.Request(
        url,
        headers=xueqiuHeader
    )).read()
    contents = json.loads(contents)
    cyb_stocks = contents['data']
    print "    Success for getting 创业板交易量..."
    #print "    Begin to analyse Volume Data..."
    tmp_list = merge_data(sha_stocks, sza_stocks)
    final_list = merge_data(tmp_list, cyb_stocks)
    volume_factor = 0
    red_num = 0
    green_num = 0
    for i, stock in enumerate(final_list):
        p = float(stock[4])
        if p > 0:
            red_num += 1
        if p < 0:
            green_num += 1
        if i is 9 or i is 49 or i is 99 or i is 199:
            if red_num > green_num:
                volume_factor += 0.25
    print "    Success 计算交易量因子, FACTOR[%s]..." % volume_factor
    return volume_factor

def merge_data(a_list, b_list):
    tmp_list = []
    i = 0
    j = 0
    len_a = len(a_list)
    len_b = len(b_list)
    a_v = a_list[i]
    b_v = b_list[j]
    while i < len_a and j < len_b:
        while( i < len_a and j < len_b and a_v[9] >= b_v[9]) :
            tmp_list.append(a_v)
            i += 1
            if i < len_a:
                a_v = a_list[i]
        while (i < len_a and j < len_b and a_v[9] < b_v[9]):
            tmp_list.append(b_v)
            j += 1
            if j < len_b:
                b_v = b_list[j]
    while i < len_a:
        tmp_list.append(a_list[i])
        i += 1
    while j < len_b:
        tmp_list.append(b_list[j])
        j += 1
    return tmp_list

def main(net_value_cur, net_value_5d):
    net_value_factor = getNetValueFactor(net_value_cur, net_value_5d)
    index_factor = getIndexFactor()
    zhangting_factor = getPercentFactor()
    volume_factor = getVolumeFactor()
    chicang = net_value_factor + index_factor + zhangting_factor + volume_factor
    print ""
    print "======前方高能，请注意======\n"
    print "    目前应该保持的仓位是 [%s]\n" % chicang
    print "==========祝君好运==========\n"

def userage():
    print "使用说明："
    print "    python assets_controller.py 当日净值 5日平均净值"

if __name__ == "__main__":
    if len(sys.argv) != 3 :
        userage()
        sys.exit(0)
    net_value_cur = float(sys.argv[1])
    net_value_5d = float(sys.argv[2])
    main(net_value_cur, net_value_5d)


