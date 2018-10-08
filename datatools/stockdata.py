#!/usr/bin/env python

import os
import pandas as pd
from bs4 import BeautifulSoup
import subprocess as sp

class CollectData(object) :

    def __init__(self, location='sh'):

        # location of the stock market, shanghai (sh) or shenzhen (sz)
        self.stock_loc = location

    def stock_list(self, html):
        #TODO: process sha stock ids and information with bs4

        text = sp.check_output("cat %s "%html, shell=True)
        soup = BeautifulSoup(text, "html.parser")
        all_codes = [ x for x in soup.find_all('a') if "banban.cn/gupiao/6" in x ]

        stock_list = pd.DataFrame()
        stock_list['code'] = [x.split("\"")[1].split("/")[-1] for x in all_codes]
        stock_list['cn_name'] = [x.split(">")[1].split("<")[0] for x in all_codes]
        stock_list['link'] = [x.split("\"")[1] for x in all_codes]

        return stock_list

