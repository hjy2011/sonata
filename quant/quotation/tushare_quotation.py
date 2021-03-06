#!/usr/bin/python
#-*- coding: utf-8 -*- 
#****************************************************************#
# @Brief: tusharequotation.py 获取天级历史数据
# @@Author: www.zhangyunsheng.com@gmail.com
# @CreateDate: 2016-04-18 00:11
# @ModifyDate: 2016-04-18 00:13
# Copyright ? 2016 Baidu Incorporated. All rights reserved.
#***************************************************************#

import tushare as ts
import pandas as pd
import time
import os
import sys
import logging
import getopt
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.const as CT
import utils.date_time as date_time

class TushareQuotation:
    """历史数据"""

    def __init__(self):
        return

    def get_stock_basics(self, expire=60*24):
        """
        获取沪深上市公司基本情况
        :param expire: 本地数据失效时间(分)，超过时间更新本地数据,强制更新传0

        @result:
        code,代码
        name,名称
        industry,所属行业
        area,地区
        pe,市盈率
        outstanding,流通股本
        totals,总股本(万)
        totalAssets,总资产(万)
        liquidAssets,流动资产
        fixedAssets,固定资产
        reserved,公积金
        reservedPerShare,每股公积金
        eps,每股收益
        bvps,每股净资
        pb,市净率
        timeToMarket,上市日期
        """
        if not os.path.exists(CT.BASICS_DIR):
            os.makedirs(CT.BASICS_DIR)

        basics_file_path = CT.BASICS_DIR + './basics.csv'

        expired = date_time.check_file_expired(basics_file_path, expire)
        if expired:
            d = ts.get_stock_basics()
            d = d.sort_index()
            d.to_csv(CT.BASICS_DIR + './basics.csv')

            all_stock_symbol = open(CT.BASICS_DIR + './symbols.csv', 'w')
            stock_symbol = []
            for symbol in d['name'].index:
                stock_symbol.append(symbol + '\n')
            all_stock_symbol.writelines(stock_symbol)
            all_stock_symbol.close()
            return d
        else:
            d = pd.read_csv(basics_file_path)
            return d

    def get_h_data(self, symbol, expire=60):
        """
        获取一支股票所有历史数据保存到本地
        """
        if not os.path.exists(CT.HIS_DIR):
            os.makedirs(CT.HIS_DIR)
        file_path = CT.HIS_DIR + symbol
        expired = date_time.check_file_expired(file_path, expire)
        if expired:
            today = date_time.get_today_str()
            d = ts.get_h_data(symbol, autype=None, start=CT.START, end=today, drop_factor=False)
            d.to_csv(CT.HIS_DIR + symbol)
            return d
        else:
            d = pd.read_csv(file_path)
            return d

    def get_tick_data(self, symbol, date, expire=60*24*365*10):
        """
        获取一支股票一天的tick数据保存到本地
        --------
        symbol: string,股票代码
        date: string,1900-01-01
        """
        if not os.path.exists(CT.TICK_DIR):
            os.makedirs(CT.TICK_DIR)
        if not os.path.exists(CT.TICK_DIR +  symbol):
            os.makedirs(CT.TICK_DIR + symbol)

        file_path = CT.TICK_DIR + symbol + '/' + date
        expired = date_time.check_file_expired(file_path, expire)
        if expired:
            d = ts.get_tick_data(symbol, date)
            #过掉当天没数据的
            if len(d) > 10:
                d.to_csv(file_path)
        else:
            d = pd.read_csv(file_path)

        #过掉当天没数据的
        if len(d) > 10:
            return d
        else:
            return ''

    def get_today_shibor_ON(self):
        """
        获取今天的银行间拆借利率 隔夜(O/N)
        """
        d = ts.shibor_data() #取当前年份的数据
        #print d.sort('date', ascending=False).head(10)
        return d['ON'][len(d['ON']) - 1]

def main(argv):
    t = TushareQuotation()
    #d = t.get_stock_basics(0)
    #print d
    #d = t.get_h_data('002337')
    #print d
    d = t.get_tick_data('000001', '2016-05-20')
    print d
    d = t.get_today_shibor_ON()
    print d
    return

if __name__ == "__main__":
    main(sys.argv)
