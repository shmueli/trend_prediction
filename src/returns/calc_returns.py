import sys
sys.path.insert(0, '../')

from datetime import datetime, timedelta
import json

from graphs import load_graphs, load_graphs_old
from rates import load_rates, load_instruments

from helpers import constants


def execute(periods, days, old):
    for p in periods:
        store_daily_returns_for_all_individuals(periods[p]['start'], periods[p]['end'], p, days, old)


def store_daily_returns_for_all_individuals(start, end, p, days, old):
    output_filename = constants.RETURNS_FOLDER_NAME + get_suffix(days, old, p)
    
    returns = {}
    
    time = start
    while time<end:
        time_str = datetime.strftime(time, constants.GENERAL_DATE_FORMAT) 

        if old:
            g_trades = load_graphs_old.load_time_network(time, data=True)
        else:
            g_trades = load_graphs.load_time_network(time, data=True)

        for v in g_trades.node:
            if days=='end':
                r = calc_returns_for_individual(g_trades, v, time, end)
            else:
                r = calc_returns_for_individual(g_trades, v, time, time + timedelta(days=days))
            
            if v not in returns:
                returns[v] = {}                    
            returns[v][time_str] = r
                
        time = time + timedelta(days=1)
        
    json.dump(returns, open(output_filename, 'w'))
    

'''
def calc_returns_for_group(g, group, start, end):
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

        [ind_profit, ind_units, ind_amount, ind_leverage, ind_period] = calc_returns_for_individual(g, v, start, end)
        
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


def calc_returns_for_group_given_individuals(individuals, group):
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

        [ind_profit, ind_invested, ind_pos_trades, ind_neg_trades, ind_bal_trades, ind_ignored_trades, ind_period, ind_ROI] = individuals[v]
        
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
'''


def calc_returns_for_individual(g, v, open_time, close_time):

    ind_profit = []
    ind_units = []
    ind_amount = []
    ind_leverage = []
    ind_period = []

    if g.has_node(v):
        for e in g.out_edges(v, data=True):
            for t in e[2]['data']:
                
                adj_open_time = open_time
                if (t['openDate']+constants.SHIFT)>=open_time:
                    adj_open_time = (t['openDate']+constants.SHIFT)

                adj_close_time = close_time
                if (t['closeDate']+constants.SHIFT)<=close_time:
                    adj_close_time = (t['closeDate']+constants.SHIFT)

                #In some cases adj_close_time<=adj_open_time - that's a bug of eToro and in such cases the rates will be taken from the trade itself...
                                    
                profit, units, amount, leverage, period = calc_return_for_trade(t, adj_open_time, adj_close_time, timedelta(hours=1))
                
                ind_profit.append(profit)         
                ind_units.append(units)         
                ind_amount.append(amount)         
                ind_leverage.append(leverage)
                ind_period.append(period)         


    return [
        ind_profit,
        ind_units,
        ind_amount,
        ind_leverage,
        ind_period,
    ] 


def calc_return_for_trade(t, open_time, close_time, accuracy):    
    #Important insights:
    #1. I assume that the DollarAmount and AmountInUnitsDecimal fields are correct and that the Leverage field might be wrong...
    #2. NetProfit contains also the spread which may be a bit high for small profits
    #3. Guy database is not accurate enough - instead I use eToro's rate for other trades which occurred around the required time


    if open_time == t['openDate'] + constants.SHIFT:
        open_rate = t['openRate']
    else:
        open_rate = load_rates.get_rate(t['buyCurAbbreviation'], t['sellCurAbbreviation'], open_time, accuracy)


    if close_time == t['closeDate'] + constants.SHIFT:
        close_rate = t['closeRate']
    else:
        close_rate = load_rates.get_rate(t['buyCurAbbreviation'], t['sellCurAbbreviation'], close_time, accuracy)
    
    
    if open_rate==None or close_rate==None:
        #we didn't find accurate enough rates (i.e. rates around the required time)
        return None, None, None, None, None

    
    profit_delta = (close_rate-open_rate) * (1.0 if t['buyOrSell']=='Buy' else - 1.0)
    profit = t['unitsDecimal'] * profit_delta
    temp_rate = get_usd_rate(close_time, 'USD', t['sellCurAbbreviation'], t['buyCurAbbreviation'])
    if temp_rate==None:
        return None, None, None, None, None
    profit_in_usd = profit * temp_rate

    '''
    t_profit = t['nProfit'] - t['spread']
    if open_time == t_open_time and close_time == t_close_time:
        if sig_diff(profit_in_usd, t_profit, 2.0):
            print '$$$', 'profit', profit_in_usd, t_profit, str(t)
        profit_in_usd = t_profit
    '''

    #'''
    temp_rate = get_usd_rate(open_time, 'USD', t['buyCurAbbreviation'], t['sellCurAbbreviation'])
    if temp_rate==None:
        #we didn't find accurate enough rates (i.e. rates around the required time)
        #if open_time.weekday()!=5 and open_time.weekday()!=6:
        #    print '###########################################################', open_time, 'USD', t['buyCurAbbreviation'], t['sellCurAbbreviation']
        return None, None, None, None, None
    units_in_usd = t['unitsDecimal']*temp_rate
    
    t_amount_in_usd = t['amount']
    t_leverage = t['leverage']

    period = period_length(open_time, close_time)

    return profit_in_usd, units_in_usd, t_amount_in_usd, t_leverage, period


def get_usd_rate(close_time, target, source, mediator):
    if source==target:
        return 1.0
    
    buy = target
    sell = source
    instrument = buy + '/' + sell
    
    if instrument not in load_instruments.load():
        buy = source
        sell = target
        instrument = buy + '/' + sell

    if instrument not in load_instruments.load():
        temp_rate1 = get_usd_rate(close_time, target, mediator, None)
        temp_rate2 = get_usd_rate(close_time, mediator, source, None)
        return temp_rate1*temp_rate2

    close_rate = load_rates.get_rate(buy, sell, close_time, timedelta(days=1))
    
    if close_rate==None:
        return None
    
        
    if sell==target:
        return close_rate
    
    if buy==target:
        return 1.0/close_rate


def tomorrow(time):
    tomorrow = datetime(time.year, time.month, time.day) + timedelta(days=1)
    return tomorrow


def period_length(start, end):
    diff = (end - start)
    period = diff.days + (1 if diff>timedelta(days=diff.days) else 0)

    return period


def get_suffix(days, old, p):
    suffix = 'returns_'

    suffix = suffix + str(days) + '_'

    if old:
        suffix = suffix + 'old_'
    else:
        suffix = suffix + 'new_'
    
    suffix = suffix + str(p)

    return suffix
