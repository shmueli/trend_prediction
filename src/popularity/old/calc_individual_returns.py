from datetime import datetime, timedelta

from rates import currency_rates
from graphs import load_graphs
import helpers.constants as constants


shift = timedelta(seconds=int(150*60))


def execute():
    currency_rates.load()
    
    start = datetime.strptime('20110701000000', constants.GENERAL_DATE_FORMAT)
    end = datetime.strptime('20130701000000', constants.GENERAL_DATE_FORMAT)
    store_daily_popularity_for_all_individuals(start, end)


def store_daily_popularity_for_all_individuals(start, end):
    output_folder = 'X:/workspace/trend_prediction_out/etoro/daily_period/daily_returns/'
    
    time = start
    while time<end:
        if time.weekday()!=5 and time.weekday()!=6:
            g_trades = load_graphs.load_time_network(time, data=True)

            vs = {}
            
            for v in g_trades.node:
                r = calc_popularity_for_individual(g_trades, v, time, tomorrow(time))
                
                if v not in vs:
                    vs[v] = []
                    
                vs[v].append(r)
            
            for v in vs:
                writer = open(output_folder + str(v), 'a')

                for r in vs[v]:
                    line = str(r)
                    line = line[1:-1].replace(', ', ',')
                    line = time.strftime(constants.GENERAL_DATE_FORMAT) + ',' + line
    
                    writer.write(line + '\n')
                
                writer.close()
             
        time = time + timedelta(days=1)


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

        [ind_profit, ind_invested, ind_pos_trades, ind_neg_trades, ind_bal_trades, ind_ignored_trades, ind_period, ind_ROI] = calc_popularity_for_individual(g, v, start, end)
        
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



def calc_popularity_for_individual(g, v, open_time, close_time):

    ind_profit = 0
    ind_invested = 0
    ind_pos_trades = 0
    ind_neg_trades = 0
    ind_bal_trades = 0
    ind_ignored_trades = 0
    ind_period = 0
    ind_ROI = None

    if g.has_node(v):
        for e in g.out_edges(v, data=True):
            for t in e[2]['data']:
                 
                
                adj_open_time = open_time
                open_rate = None
                if (t['openDate']+shift)>=open_time:
                    adj_open_time = (t['openDate']+shift)
                    open_rate = t['openRate']

                adj_close_time = close_time
                close_rate = None
                if (t['closeDate']+shift)<=close_time:
                    adj_close_time = (t['closeDate']+shift)
                    close_rate = t['closeRate']   
                
                if close_time<=open_time:
                    continue
                
                profit, invested = calc_return_for_trade(t, adj_open_time, adj_close_time, timedelta(hours=1), open_rate, close_rate)

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
        ind_period = period_length(open_time, close_time)

        #The reason that the calculation of ROI here is right:
        #We take the trades that were open on that day only, so new trades
        #cannot be added and that's why the budget remains fixed
        ind_ROI = float(ind_profit)/float(ind_invested)

    a = 1
    
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


def calc_return_for_trade(t, open_time, close_time, accuracy, open_rate, close_rate):    
    #Important insights:
    #1. I assume that the DollarAmount and AmountInUnitsDecimal fields are correct and that the Leverage field might be wrong...
    #2. NetProfit contains also the spread which may be a bit high for small profits
    #3. Guy database is not accurate enough - instead I use eToro's rate for other trades which occurred around the required time

    amount = t['amount']
    
    if open_rate==None:
        open_rate = currency_rates.get_rate(t['buyCurAbbreviation'], t['sellCurAbbreviation'], open_time, accuracy)
        
    if close_rate==None:
        close_rate = currency_rates.get_rate(t['buyCurAbbreviation'], t['sellCurAbbreviation'], close_time, accuracy)

    if open_rate==None or close_rate==None:
        #we didn't find accurate enough rates (i.e. rates around the required time)
        #print '###', open_time, close_time, t['Instrument'], t['PositionID']
        return None, None
    
    

    if close_rate/open_rate>2 or open_rate/close_rate>2:
        open_rate = currency_rates.get_rate(t['buyCurAbbreviation'], t['sellCurAbbreviation'], open_time, accuracy)
        close_rate = currency_rates.get_rate(t['buyCurAbbreviation'], t['sellCurAbbreviation'], close_time, accuracy)

        if open_rate==None or close_rate==None:
            #we didn't find accurate enough rates (i.e. rates around the required time)
            #print '###', open_time, close_time, t['Instrument'], t['PositionID']
            return None, None

    
    profitPercentage = (close_rate-open_rate) * (1.0 if t['buyOrSell']=='Buy' else - 1.0) #check

          
    profit = float(t['unitsDecimal']) * profitPercentage


    usd_rate = get_usd_rate(t, close_time, close_rate)
    if usd_rate==None:
        #we didn't find accurate enough rates (i.e. rates around the required time)
        return None, None


    profit = profit * usd_rate

    
    #if ( (t['NetProfit']>0 and profit/t['NetProfit']>2) or (profit>0 and t['NetProfit']/profit>2) ):
    #    the calculated profit is significantly different than the NetProfit
    #    print profit, t['NetProfit'], open_rate, close_rate, t

    if profit<0 and (-profit)>amount:
        #the loss cannot be higher than the amount invested
        #print profit, amount
        profit = -amount
    
    return profit, amount


def get_usd_rate(t, close_time, close_rate):
    curr1 = t['buyCurAbbreviation'] #check
    curr2 = t['sellCurAbbreviation']
    
    if curr2=='USD':
        return 1.0
    
    if curr1=='USD':
        return 1.0/close_rate
    
    buy = 'USD'
    sell = curr2
    instrument = buy + '/' + sell
    if instrument not in currency_rates.get_instruments():
        buy = curr2
        sell = 'USD'    
    
    close_rate = currency_rates.get_rate(buy, sell, close_time, accuracy=timedelta(days=1))
    
    if close_rate==None:
        return None
    
        
    if sell=='USD':
        return close_rate
    
    if buy=='USD':
        return 1.0/close_rate


def tomorrow(time):
    tomorrow = datetime(time.year, time.month, time.day) + timedelta(days=1)
    return tomorrow


def period_length(start, end):
    period = (end - start).days + 1

    return period


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
