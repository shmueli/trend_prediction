import sys
sys.path.insert(0, '../')

from datetime import datetime, timedelta
import json

from graphs import load_graphs
from rates import load_rates, load_instruments

from helpers import constants

def execute():
    for p in constants.PERIODS_MONTHLY:
        store_daily_returns_for_all_individuals(constants.PERIODS_MONTHLY[p]['start'], constants.PERIODS_MONTHLY[p]['end'], p)


def store_daily_returns_for_all_individuals(start, end, period):
    output_filename = constants.RETURNS_FOLDER_NAME + 'daily_limited_returns' + '_' + str(period)
    
    returns = {}
    
    time = start
    while time<end:
        time_str = datetime.strftime(time, constants.GENERAL_DATE_FORMAT) 

        g_trades = load_graphs.load_time_network(time, data=True)

        for v in g_trades.node:
            r = calc_returns_for_individual(g_trades, v, time, tomorrow(time))
            
            if v not in returns:
                returns[v] = {}                    
            returns[v][time_str] = r
                
        time = time + timedelta(days=1)
        
    json.dump(returns, open(output_filename, 'w'))
    

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

        [ind_profit, ind_invested, ind_pos_trades, ind_neg_trades, ind_bal_trades, ind_ignored_trades, ind_period, ind_ROI] = calc_returns_for_individual(g, v, start, end)
        
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



def calc_returns_for_individual(g, v, open_time, close_time):

    ind_profit = 0
    ind_invested = 0
    ind_pos_trades = 0
    ind_neg_trades = 0
    ind_bal_trades = 0
    ind_ignored_trades = 0
    ind_period = 0
    ind_ROI = None

    min_adj_open_time = None
    max_adj_close_time = None
    
    if g.has_node(v):
        for e in g.out_edges(v, data=True):
            for t in e[2]['data']:
                
                adj_open_time = open_time
                if (t['openDate']+constants.SHIFT)>=open_time:
                    adj_open_time = (t['openDate']+constants.SHIFT)

                adj_close_time = close_time
                if (t['closeDate']+constants.SHIFT)<=close_time:
                    adj_close_time = (t['closeDate']+constants.SHIFT)
                
                if adj_close_time<=adj_open_time:
                    continue
                
                if min_adj_open_time==None or adj_open_time<min_adj_open_time:
                    min_adj_open_time = adj_open_time

                if max_adj_close_time==None or adj_close_time<max_adj_close_time:
                    max_adj_close_time = adj_close_time
                    
                profit, invested = calc_return_for_trade(t, adj_open_time, adj_close_time, timedelta(hours=1))

                if profit==None or invested==None:
                    ind_ignored_trades = ind_ignored_trades + 1
                    continue

                ind_profit = ind_profit + profit         
                ind_invested = ind_invested + invested
                if profit>0:
                    ind_pos_trades = ind_pos_trades + 1
                elif profit<0:
                    ind_neg_trades = ind_neg_trades + 1
                elif profit==0:
                    ind_bal_trades = ind_bal_trades + 1
                
    if ind_invested>0:
        ind_period = period_length(min_adj_open_time, max_adj_close_time)

        #The reason that the calculation of ROI here is right:
        #We take the trades that were open on that day only, so new trades
        #cannot be added and that's why the budget remains fixed
        ind_ROI = float(ind_profit)/float(ind_invested)                

    return [
        ind_profit,
        ind_invested,
        ind_pos_trades,
        ind_neg_trades,
        ind_bal_trades,
        ind_ignored_trades,
        ind_period,
        ind_ROI,            
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
        return None, None

    
    profit_delta = (close_rate-open_rate) * (1.0 if t['buyOrSell']=='Buy' else - 1.0)
    profit = t['unitsDecimal'] * profit_delta
    temp_rate = get_usd_rate(close_time, 'USD', t['sellCurAbbreviation'], t['buyCurAbbreviation'])
    if temp_rate==None:
        return None, None        
    profit_in_usd = profit * temp_rate

    '''
    t_profit = t['nProfit'] - t['spread']
    if open_time == t_open_time and close_time == t_close_time:
        if sig_diff(profit_in_usd, t_profit, 2.0):
            print '$$$', 'profit', profit_in_usd, t_profit, str(t)
        profit_in_usd = t_profit
    '''

    '''  
    temp_rate = get_usd_rate(open_time, 'USD', t['buyCurAbbreviation'], t['sellCurAbbreviation'])
    if temp_rate==None:
        #we didn't find accurate enough rates (i.e. rates around the required time)
        if open_time.weekday()!=5 and open_time.weekday()!=6:
            print '###########################################################', open_time, 'USD', t['buyCurAbbreviation'], t['sellCurAbbreviation']
        return None, None        
    units_in_usd = t['unitsDecimal']*temp_rate
    
    t_units = t['amount']*t['leverage']
    '''

    t_amount_in_usd = t['amount']

    #limit the loss to 100%
    if profit_in_usd<float(-t_amount_in_usd):
        profit_in_usd = -t_amount_in_usd

    return profit_in_usd, t_amount_in_usd


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


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
