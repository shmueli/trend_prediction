import sys
sys.path.insert(0, '../')

from datetime import datetime
import json

import calc_returns
from helpers import constants


periods = constants.PERIODS_MONTHLY
days = 1
old = False


_returns = None
_period = None


def load(period):
    global _period, _returns

    if _period==period:
        return _returns

    input_filename = constants.RETURNS_FOLDER_NAME + calc_returns.get_suffix(days, old, period)
    
    _period = period
    _returns = json.load(open(input_filename, 'r'))
    
    return _returns


def get_return(v, date):
    period = constants.get_period(periods, date)

    load(period)

    date_str = datetime.strftime(date, '%Y%m%d%H%M%S') 
    v_str = str(v)

    if v_str not in _returns:
        return None
    
    if date_str not in _returns[v_str]:
        return None
            
    return _returns[v_str][date_str]
