import sys
sys.path.insert(0, '../')
import pylab

import json
from datetime import datetime, timedelta

from helpers import constants

from popularity import load_daily_popularity

import numpy as np

def load_returns(period):
    #input_filename = constants.RETURNS_FOLDER_NAME + 'period_returns' + '_' + str(period)
    input_filename = constants.RETURNS_FOLDER_NAME + 'daily_returns' + '_' + str(period)
    #input_filename = constants.RETURNS_FOLDER_NAME + 'daily_limited_returns' + '_' + str(period)
    #input_filename = constants.RETURNS_FOLDER_NAME + 'daily_old_returns' + '_' + str(period)
    
    returns = json.load(open(input_filename, 'r'))
    
    return returns


def visualize_popularity_vs_return(period):
    _returns = load_returns(period)
    _popularity = load_daily_popularity.load(period)

    X = []
    Y = []
    cnt = 0
    for v in _returns:
        cnt = cnt+1
        if cnt%1000==0:
            print cnt

        if v not in _popularity:
            continue
        
        for date_str in _returns[v]:
            if date_str not in _popularity[v]:
                continue
            
            date = datetime.strptime(date_str, '%Y%m%d%H%M%S')
            if date.weekday()==5 or date.weekday()==6:
                continue
            
            r = _returns[v][date_str]
            roi = r[-1]
            if roi==None:
                continue
            
            X.append(roi)
            Y.append(_popularity[v][date_str][0])
            

    print len(X), len(Y)
                 
    pylab.scatter(X, Y)

    pylab.show()


def visualize_popularity_vs_period_return(period, length):
    _returns = load_returns(period)
    _popularity = load_daily_popularity.load(period)

    X = []
    Y = []
    cnt = 0
    for v in _returns:
        cnt = cnt+1
        if cnt%1000==0:
            print cnt

        if v not in _popularity:
            continue
        
        for date_str in _returns[v]:
            if date_str not in _popularity[v]:
                continue
            
            profit = []
            invested = []
            date = datetime.strptime(date_str, '%Y%m%d%H%M%S')
            for i in range(length):
                currdate = date - timedelta(days=i)
                
                if currdate.weekday()==5 or currdate.weekday()==6:
                    continue
            
                currdate_str = currdate.strftime('%Y%m%d%H%M%S')
                
                if currdate_str not in _returns[v]:
                    continue

                r = _returns[v][currdate_str]
                
                profit.append(r[0])
                invested.append(r[1])

            if len(invested)==0:
                continue
            
            roi = np.sum(profit)/np.average(invested)
            
            X.append(roi)
            Y.append(_popularity[v][date_str][0])
            

    print len(X), len(Y)
                 
    pylab.scatter(X, Y)

    pylab.show()


visualize_popularity_vs_period_return(1, 90)