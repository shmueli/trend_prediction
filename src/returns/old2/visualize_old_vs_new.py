import sys
sys.path.insert(0, '../')
import pylab

import json
from datetime import datetime, timedelta

from helpers import constants

from popularity import load_daily_popularity

import numpy as np

def load_old_returns(period):
    input_filename = constants.RETURNS_FOLDER_NAME + 'daily_old_returns' + '_' + str(period)
    
    returns = json.load(open(input_filename, 'r'))
    
    return returns

def load_new_returns(period):
    input_filename = constants.RETURNS_FOLDER_NAME + 'daily_returns' + '_' + str(period)
    
    returns = json.load(open(input_filename, 'r'))
    
    return returns


def visualize_old_vs_new(period):
    old_returns = load_old_returns(period)
    new_returns = load_new_returns(period)

    X = []
    Y = []
    cnt = 0
    for v in old_returns:
        cnt = cnt+1
        if cnt%1000==0:
            print cnt

        if v not in new_returns:
            continue
        
        for date_str in old_returns[v]:
            if date_str not in new_returns[v]:
                continue
            
            date = datetime.strptime(date_str, '%Y%m%d%H%M%S')
            if date.weekday()==5 or date.weekday()==6:
                continue
            
            old_roi = old_returns[v][date_str][-1]
            if old_roi==None:
                continue

            new_roi = new_returns[v][date_str][-1]
            if new_roi==None:
                continue
            
            if old_roi<-10 or old_roi>10:
                continue
            
            X.append(old_roi)
            Y.append(new_roi)
            

    print len(X), len(Y)
                 
    pylab.scatter(X, Y)

    pylab.show()


visualize_old_vs_new(1)