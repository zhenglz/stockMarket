#!/usr/bin/env python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class BasicAnalysis(object) :

    def __init__(self, dat):

        self.dat = dat

    def timeLagCorrelation(self, dat1, dat2,
                           dt=0, method='pearson'):
        #TODO: calculate the correlation considering
        # time lagged information
        return NotImplementedError

    def timeSeriesPattern(self):
        #TODO: calculate the time series pattern from data
        return NotImplementedError

    def compare2PastMean(self, lastDays=150):
        #TODO: evaluate whether current price higher than
        # history price
        return NotImplementedError

class StockDisplay(object) :

    def __init__(self, dat):
        self.dat = dat

    def kLinePlot(self):
        #TODO k-line plot of a stock

        return NotImplementedError

    def timeSeriesPlot(self):
        #TODO time series plot of a stock

        return NotImplementedError
