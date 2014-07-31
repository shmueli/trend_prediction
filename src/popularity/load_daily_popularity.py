import sys
sys.path.insert(0, '../')

import json
from datetime import datetime

from helpers import constants

_popularity = {}


def load(period):
    global _popularity

    if period in _popularity:
        return _popularity[period]

    input_filename = constants.POPULARITY_FOLDER_NAME + 'daily_popularity' + '_' + str(period)
    
    _popularity[period] = json.load(open(input_filename, 'r'))
    
    return _popularity[period]


def get_popularity(v, date):
    period = constants.get_period(date)
    
    load(period)

    date_str = datetime.strftime(date, '%Y%m%d%H%M%S') 
    v_str = str(v)

    if v_str not in _popularity[period] or date_str not in _popularity[period][v_str]:
        return None
    
    return _popularity[period][v_str][date_str]
