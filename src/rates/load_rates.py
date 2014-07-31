import sys
sys.path.insert(0, '../')

import json
import bisect
from datetime import datetime, timedelta

from helpers import constants

shift = timedelta(seconds=int(150*60))

_rates = {}


def load(period):
    global _rates

    if period in _rates:
        return _rates[period]

    input_filename = constants.RATES_FOLDER_NAME + 'rates_' + str(period)
    
    _rates[period] = json.load(open(input_filename, 'r'))
    
    return _rates[period]


def get_rate(buyCurAbbreviation, sellCurAbbreviation, time, accuracy):
    period = constants.get_period(constants.PERIODS_MONTHLY, time)

    load(period)
        
    currency = buyCurAbbreviation + '/' + sellCurAbbreviation

    time = time - shift
    time_str = datetime.strftime(time, '%Y%m%d%H%M%S') 
    
    times = _rates[period][currency]
    
    index = bisect.bisect_left(times, [time_str, 0])
    
    if index<0:
        return None
    
    if index>=len(times):
        return None
    
    closest_time_str = times[index][0]
    closest_time = datetime.strptime(closest_time_str, '%Y%m%d%H%M%S')
    rate = float(times[index][1])
    
    if closest_time-time > accuracy:
        #print instrument, t['OpenOccured']+shift-time, t
        return None
    
    return rate
