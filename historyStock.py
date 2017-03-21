#!/usr/bin/env python

import numpy as np
from email.mime.text import MIMEText
from datetime import date
import smtplib
import os
import scipy.stats
import tushare as ts
from time import sleep
from datetime import datetime


class EmailSender :

    def __init__(self,passwd, receivers) :

        self.SMTP_SERVER = "smtp.gmail.com"
        self.SMTP_PORT = 587
        self.SMTP_USERNAME = "astrozheng@gmail.com"
        self.SMTP_PASSWORD = passwd

        self.EMAIL_TO = receivers
        self.EMAIL_FROM = "astrozheng@gmail.com"

        self.DATE_FORMAT = "%d/%m/%Y"
        self.EMAIL_SPACE = ", "


    def send_email(self, DATA, EMAIL_SUBJECT):
        msg = MIMEText(DATA)
        msg['Subject'] = EMAIL_SUBJECT + " %s" % (date.today().strftime(self.DATE_FORMAT))
        msg['To'] = self.EMAIL_SPACE.join(self.EMAIL_TO)
        msg['From'] = self.EMAIL_FROM
        mail = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
        mail.starttls()
        mail.login(self.SMTP_USERNAME, self.SMTP_PASSWORD)
        mail.sendmail(self.EMAIL_FROM, self.EMAIL_TO, msg.as_string())
        mail.quit()

class GetHistoryData :
    # SHA 000001
    def __init__(self):
        pass
        #self.id = stockId

    def stockHistStatistics(self, id,maxDayRange=250):
        stock = ts.get_h_data(id, index=True)

        close_hist = stock['close'][:maxDayRange]
        close_hist_mean = np.mean(stock['close'][:maxDayRange])
        close_hist_std  = np.std(stock['close'][:maxDayRange])

        day_delta = np.mean(stock['open'][:maxDayRange]
                            - stock['close'][:maxDayRange])
        day_delta_mean = np.mean(stock['open'][:maxDayRange]
                                 - stock['close'][:maxDayRange])
        day_delta_std = np.std(stock['open'][:maxDayRange]
                                - stock['close'][:maxDayRange])

        twodayDiff = []
        close = list(stock['close'])
        print(len(close))
        for i in range(maxDayRange) :
            #print "DAA"
            delta = close[i] - close[i+1]
            twodayDiff.append(delta)

        twodayDiff_mean = np.mean(np.asarray(twodayDiff))
        twodayDiff_std  = np.std(np.asarray(twodayDiff))

        return [close_hist, close_hist_mean, close_hist_std], [day_delta, day_delta_mean,day_delta_std], [twodayDiff, twodayDiff_mean, twodayDiff_std]

    def stockTodayValues(self, stockId='sh'):
        if not stockId :
            # real time stock values
            df = ts.get_realtime_quotes(self.id)
        else:
            df = ts.get_realtime_quotes(stockId)

        return(df)

    def compareMeans(self, hist_mean, current):
        # perform a one sample t-tes to compare the current value with history mean
        # return a list of two elements: t-statistics and the two tailed p value
        return(scipy.stats.ttest_1samp(hist_mean, current))

    def normalProb(self, mean, std, x):
        # assume a gaussian distribution of the data
        z_score = (x - mean) / std
        # one tailed accumulated probability
        prob = scipy.stats.norm.cdf(z_score)
        return(prob)

if __name__ == "__main__" :
    # find current time
    tminfor = datetime.now()
    weekday = tminfor.timetuple()[6]
    hour    = tminfor.timetuple()[3]
    minute  = tminfor.timetuple()[4]
    time = str(datetime.now())

    BLOCK = 50.0

    while weekday in range(5) and str(hour) in ['14','13'] and int(float(minute)) in range(10, 40) :
    #if 1 :
        print weekday, hour, minute
        ## in the right time zone, do the job
        stockhist = GetHistoryData()
        EmailData = 'To Mr. MT: \n\n Current Time '+time+'   \n'
        try:
            today = stockhist.stockTodayValues('sh')
        except:
            today = None
            EmailData += 'Today\'s stock information is not available. \n\nMessage From Machine Hbutterfly.\n'

        if not today.empty :
            current = today['price']

            EmailData += 'Today: \n    Open       Now     Delta   \n    %8.2f  %8.2f  %8.2f \n\n' \
                         % ( float(today['open']), float(today['price']),
                             float(today['price'])-float(today['open']) )

            stats = stockhist.stockHistStatistics('000001', 200)
            # compare today's price to historical data
            histmean = stats[0][1]
            histstd = stats[0][2]
            EmailData += '\nLast 200 days: \n   Mean     Std     Max     Min \n %8.2f %8.2f %8.2f %8.2f \n\n' \
                         % (histmean, histstd,
                            np.max(stats[0][0]),
                            np.min(stats[0][0])
                            )

            # delta change
            EmailData += 'Change of Previous Day: \n    Mean     Std     Max     Min \n %8.2f %8.2f %8.2f %8.2f\n' \
                         % (
                            stats[1][1], stats[1][2],
                            np.max(stats[1][0]),
                            np.min(stats[1][0]),
                            )

            # compare mean
            EmailData += '\nCompare Mean of now price to history mean \n   ' \
                         'Now    History    Higher     Probability (more larger, more close to hist mean) \n'
            EmailData += '    %8.2f  %8.2f  ' % (today['price'], histmean)
            if float(today['price']) > float(histmean) :
                prob = (1.0 - (stockhist.normalProb(histmean, histstd, float(today['price']))))/0.5
                EmailData += ' True '
                EmailData += ' %4.3f \n\n' % prob

                EmailData += '\nToday you should buy very small or sell some \n'
                if prob < 0.5 :
                    EmailData += 'Sell this amount: %8.2f  RMB\n' % ((1 - prob/0.5 ) * BLOCK )
                else :
                    EmailData += 'Buy this amount: %8.2f  RMB\n' % ((prob - 0.5) * BLOCK * 2.0)
            else :
                prob = (stockhist.normalProb(histmean, histstd, float(today['price'])))/0.5
                EmailData += ' False '
                EmailData += ' %4.3f \n' % prob

                EmailData += '\n A Must Buy Day. \nBuy this amount %8.2f RMB' % ((1.0 - prob) * 1.0 + 1.0 ) * BLOCK

            ## concultion from the data

            EmailData += '\n\nMessage From Machine Hbutterfly.\n'
            # send a email
            email = EmailSender(YOURPSWD, ['lzheng002@e.ntu.edu.sg', 'lzzheng002@gmail.com'])
            email.send_email(EmailData, EMAIL_SUBJECT="STOCK DATA OF SHA "+time)

        sleep(1200)

    sleep(1200)
