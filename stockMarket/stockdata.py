#!/usr/bin/env python

import os
import pandas as pd
from bs4 import BeautifulSoup
import subprocess as sp
import tushare as ts

class CollectData(object) :

    def __init__(self, location='sha'):

        # parameters
        # location of the stock market, shanghai (sh) or shenzhen (sz)
        self.stock_loc = location

        # attributes
        # a dataframe containing all stock codes from a market
        self.code_list = None
        self.hist_data = None

    def stock_list(self):
        """
        get a list of stock code given the market
        :return: pd.DataFrame, information of all stock codes, as well as their names
        """
        #TODO: process sha stock ids and information with bs4

        PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        DEFINITIONS_ROOT = os.path.join(PROJECT_ROOT, '../data/')

        html = DEFINITIONS_ROOT + self.stock_loc + "_stock_list_all.html"

        text = sp.check_output("cat %s "%html, shell=True)
        soup = BeautifulSoup(text, "html.parser")
        all_codes = [ x for x in list(soup.find_all('a'))
                      if "banban.cn/gupiao/6" in x.encode("utf-8") ]

        stock_list = pd.DataFrame()
        stock_list['code'] = [x.encode("utf-8").split("/")[4] for x in all_codes]
        stock_list['cn_name'] = [x.encode("utf-8").split("/")[5] for x in all_codes]
        stock_list['link'] = [x.encode("utf-8").split("/")[2] for x in all_codes]

        self.code_list = stock_list['code']
        return stock_list

    def getHistoryKData(self, code, ktype="D", savefile=""):
        """
        obtain history K-line data
        :param code: str, the stock code, such sha, 600003
        :param ktype: str, k-line data frequency, W for week, D for data, 30 for 30 mins
                           details could be found here http://tushare.org/trading.html#id2
        :param savefile: str, save the data to a file
        :return: pd.DataFrame, the stock history K-line data
        """

        if len(savefile) == 0 :
            savefile = code + "_hist_data.csv"

        hist = None

        try :
            # download data using tushare
            hist = ts.get_hist_data(code, pause=3.1415, retry_count=5, ktype=ktype)
            hist.to_csv(savefile, sep=",", header=True, index=True)
            self.hist_data = hist
        except :
            print('Download data %s failed, please try again later.'%code)

        return hist

    def getTodayTicksData(self, code):
        #TODO: reuse the tushare get_today_ticks
        print("http://tushare.org/trading.html#id4")
        print("Usage: tushare.get_today_ticks(code, date)")
        return NotImplementedError


class ProcessDataSet(object):

    def __init__(self):
        pass

    def mergedDataSet(self, df1, df2):
        merged = pd.concat((df1, df2), axis=1, sort=False, copy=True)

        merged = merged.dropna(axis='index')

        return merged
