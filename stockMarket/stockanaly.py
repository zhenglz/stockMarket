#!/usr/bin/env python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr


class BasicAnalysis(object):

    def __init__(self):

        pass

    def correlation(self, x, y):
        pcc, p_value = pearsonr(x, y)

        return pcc, p_value

    def timeLagCorrelation(self, dat1, dat2, start, period=30, dt=0):
        # TODO: calculate the correlation considering
        # time lagged information
        x = dat1[start:period+start]
        y = dat2[start+dt:period+start+dt]

        pcc, p_value = self.correlation(x, y)

        return pcc, p_value

    def timeSeriesPattern(self):
        # TODO: calculate the time series pattern from data
        return NotImplementedError

    def compare2PastMean(self, x, hist_x, lastDays=150):
        # TODO: evaluate whether current price higher than
        # history price

        return 150*(x - sum(hist_x)/150.0)/(sum(hist_x))


class PairCorrelation(object):

    def __init__(self, stock1, stock2):
        # time information should be included in dataframe
        self.df1 = stock1
        self.df2 = stock2

    def maxPearsonCorr(self, f='close', pcc_cutoff=0.5, pv_cutoff=0.5):
        import math
        max_dt = min(math.floor(self.df1.shape[0]/2),
                     math.floor(self.df2.shape[0]/2))

        if max_dt >= 30:
            pccs_pvalues = []
            for start in range(int(max_dt)):
                pcc, pv = BasicAnalysis().timeLagCorrelation(self.df1[f], self.df2[f],
                                                             period=30, start=0, dt=max_dt)
                pccs_pvalues.append((pcc, pv))

            # sort the pccs
            pccs_pvalues.sort(key=lambda tup: tup[0], reverse=True)  # sorts in place

            if pccs_pvalues[0][0] > pcc_cutoff and pccs_pvalues[0][1] < pv_cutoff:
                return True, pccs_pvalues[0][1], pccs_pvalues[0][0]
            else:
                return False, pccs_pvalues[0][1], pccs_pvalues[0][0]

        else:
            return False

    def lastPeriodCorrelation(self, last_day_num=150, f='close'):

        pcc, pv = BasicAnalysis().timeLagCorrelation(self.df1[f][-last_day_num:],
                                                     self.df2[f][-last_day_num:], dt=0)

        return pcc, pv

    def matrixPeriodCorrelation(self, datset, period=30, cc_method="pearson"):

        df = datset.iloc[:period, :]

        corr = df.corr(method=cc_method)

        return corr

class StockDisplay(object):

    def __init__(self, dat):
        self.dat = dat

    def kLinePlot(self):
        # TODO k-line plot of a stock

        return NotImplementedError

    def timeSeriesPlot(self):
        # TODO time series plot of a stock

        return NotImplementedError
