import sys
sys.path.insert(0, '../')

import json
from datetime import datetime

from helpers import constants


_returns = None
_period = None


def load(period):
    global _period, _returns

    if _period==period:
        return _returns

    input_filename = constants.RETURNS_FOLDER_NAME + 'period_returns' + '_' + str(period)
    
    _period = period
    _returns = json.load(open(input_filename, 'r'))
    
    return _returns


def get_return(v, date):
    period = constants.get_period_tri_monthly(date)

    load(period)

    date_str = datetime.strftime(date, '%Y%m%d%H%M%S') 
    v_str = str(v)

    if v_str not in _returns:
        return [0, 0, 0, 0, 0, 0, 0, None]
    
    if date_str not in _returns[v_str]:
        return [0, 0, 0, 0, 0, 0, 0, None]
            
    return _returns[v_str][date_str]


def calc_returns_for_group(group, date):
    grp_profit = 0
    grp_invested = 0
    grp_pos_trades = 0
    grp_neg_trades = 0
    grp_bal_trades = 0
    grp_ignored_trades = 0
    grp_period = 0
    grp_ROI = None

    for t in range(len(group)):
        v = group[t]

        [ind_profit, ind_invested, ind_pos_trades, ind_neg_trades, ind_bal_trades, ind_ignored_trades, ind_period, ind_ROI] = get_return(v, date)
        
        if ind_ROI==None:
            grp_ignored_trades = grp_ignored_trades + ind_ignored_trades
            continue

        grp_profit = grp_profit + ind_profit
        grp_invested = grp_invested + ind_invested
        grp_pos_trades = grp_pos_trades + ind_pos_trades
        grp_neg_trades = grp_neg_trades + ind_neg_trades
        grp_bal_trades = grp_bal_trades + ind_bal_trades
        grp_period = ind_period if ind_period>grp_period else grp_period
        grp_ROI = ind_ROI if grp_ROI==None else grp_ROI + ind_ROI

    if grp_ROI!=None:
        grp_ROI = grp_ROI/float(len(group))
                    
    return [
        grp_profit,
        grp_invested,
        grp_pos_trades,
        grp_neg_trades,
        grp_bal_trades,
        grp_ignored_trades,
        grp_period,
        grp_ROI,            
    ]
