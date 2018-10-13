#!/usr/bin/env python

import os
import urllib2
import pandas as pd
from bs4 import BeautifulSoup
import subprocess as sp
import tushare as ts


class CollectData(object):
    """
    Collect stock data from internet

    Parameters
    ----------
    stock_loc: str,
        the location of the stock market

    Attributes
    ----------
    code_list: list,
        a list of all codes for a given stock market
    hist_data: pd.DataFrame,
        the history data for a stock
    PROJECT_ROOT: str,
        the path of the project
    DATA_ROOT: str,
        the path holding the data files, such as the downloaded
        stock history csv files

    """

    def __init__(self, location='sha'):

        # parameters
        # location of the stock market, shanghai (sh) or shenzhen (sz)
        self.stock_loc = location

        # attributes
        # a dataframe containing all stock codes from a market
        self.code_list = None
        self.hist_data = None

        self.PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        self.DATA_ROOT = os.path.join(self.PROJECT_ROOT, '../data/')

    def stock_list(self):
        """
        get a list of stock code given the market

        Returns
        stock_list: pd.DataFrame,
            information of all stock codes, as well as their names
        -------

        """
        #TODO: process sha stock ids and information with bs4

        html = self.DATA_ROOT + self.stock_loc + "_stock_list_all.html"

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

    def getHistoryKData(self, code, ktype="D", savefile=False):
        """
        get history K-line data for a stock

        Parameters
        ----------
        code: str,
            the stock code, such sha, 600003
        ktype: str, default is D, by day
            k-line data frequency, W for week, D for data, 30 for 30 mins
            details could be found here http://tushare.org/trading.html#id2
        savefile: bool, default is False
            whether save the data to a file

        Returns
        -------
        hist: pd.DataFrame,
            the history data of a stock

        """

        savefile_name = ""
        if savefile:
            savefile_name = self.DATA_ROOT + code + "_hist_data.csv"

        hist = None

        try:
            # download data using tushare
            hist = ts.get_hist_data(code, pause=3.1415, retry_count=5, ktype=ktype)
            if savefile_name :
                hist.to_csv(savefile_name, sep=",", header=True, index=True)

            self.hist_data = hist
        except urllib2.HTTPError:
            print('Download data %s failed, please try again later.' % code)

        return hist

    def loadHistFromCsv(self, csvfile):
        """
        load dataset from a csv file

        Parameters
        ----------
        csvfile: str,
            the file name of a csv file

        Returns
        -------
        df: pd.DataFrame
            history data of a stock
        """

        df = pd.read_csv(csvfile, sep=",", header=0)

        return df

    def getTodayTicksData(self, code):
        """
        get today's data given a stock code

        Parameters
        ----------
        code: str,
            the code of a stock

        Returns
        -------
        df: pd.DataFrame,
            the dat of today for stock code
        """
        #TODO: reuse the tushare get_today_ticks
        #print("http://tushare.org/trading.html#id4")
        #print("Usage: tushare.get_today_ticks(code)")
        df = ts.get_today_ticks(code, pause=1.414)

        return df


class ProcessDataSet(object):

    def __init__(self):
        pass

    def mergedDataSet(self, df1, df2):
        """
        merge two history dataset by their index (dat)

        Parameters
        ----------
        df1: pd.DataFrame
        df2: pd.DataFrame

        Returns
        -------
        merged: pd.DataFrame
        """
        merged = pd.concat((df1, df2), axis=1, sort=False, copy=True)

        merged = merged.dropna(axis='index')

        return merged
