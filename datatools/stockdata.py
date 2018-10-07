#!/usr/bin/env python

import os
import pandas as pd

class CollectData(object) :

    def __init__(self, location='sh'):

        # location of the stock market, shanghai (sh) or shenzhen (sz)
        self.stock_loc = location

    def stock_list(self):
        #TODO: process sha stock ids and information
        pass