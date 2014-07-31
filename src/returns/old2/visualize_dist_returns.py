import sys
sys.path.insert(0, '../')
import pylab

import json
from datetime import datetime

import numpy as np

from helpers import constants


_returns = None
_period = None


def load(period):
    global _period, _returns

    if _period==period:
        return
    
    #input_filename = constants.RETURNS_FOLDER_NAME + 'daily_returns' + '_' + str(period)
    #input_filename = constants.RETURNS_FOLDER_NAME + 'daily_limited_returns' + '_' + str(period)
    #input_filename = constants.RETURNS_FOLDER_NAME + 'daily_old_returns' + '_' + str(period)
    #input_filename = constants.RETURNS_FOLDER_NAME + 'daily_old_limited_returns' + '_' + str(period)
    input_filename = constants.RETURNS_FOLDER_NAME + 'period_returns' + '_' + str(period)
    #input_filename = constants.RETURNS_FOLDER_NAME + 'period_limited_returns' + '_' + str(period)
    
    _period = period
    _returns = json.load(open(input_filename, 'r'))


def visualize(period):
    returns = []
    
    load(period)

    #'''
    cnt = 0
    for v in _returns:
        cnt = cnt+1
        if cnt%1000==0:
            print cnt

        for date_str in _returns[v]:
            date = datetime.strptime(date_str, '%Y%m%d%H%M%S')
            if date.weekday()==5 or date.weekday()==6:
                continue
            
            r = _returns[v][date_str]
            roi = r[-1]
            if roi==None:
                continue
            
            #if (roi<-1 or roi>1):
            #    print v, date_str, r
            #    continue
                
            returns.append(roi)
    #'''
    
    #returns = [1,1,5,5,5,5,9,9]
    
    print len(returns)
    print np.mean(returns)
    print np.median(returns)
    
    pylab.hist(returns, bins = 100)
    #pylab.yscale('log')

    pylab.show()


visualize(7)