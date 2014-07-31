#this module compares the ROI for NETWORK and CROWD

from datetime import datetime, timedelta
import sets

import daily_currency_rates4
from graphs import load_graphs
import helpers.constants as constants
from utils import visualize
from wisdom import daily_currency_rates3


def execute():
    daily_currency_rates4.load()
    
    #'''
    start = datetime.strptime('20110701000000', constants.GENERAL_DATE_FORMAT)
    end = datetime.strptime('20120101000000', constants.GENERAL_DATE_FORMAT)
    predict_daily_currency_pair(start, end, '1')
    #'''

    #'''
    start = datetime.strptime('20120101000000', constants.GENERAL_DATE_FORMAT)
    end = datetime.strptime('20120701000000', constants.GENERAL_DATE_FORMAT)
    predict_daily_currency_pair(start, end, '2')
    #'''

    '''
    start = datetime.strptime('20120701000000', constants.GENERAL_DATE_FORMAT)
    end = datetime.strptime('20130101000000', constants.GENERAL_DATE_FORMAT)
    predict_daily_currency_pair(start, end, '3')
    '''

    #'''
    start = datetime.strptime('20130101000000', constants.GENERAL_DATE_FORMAT)
    end = datetime.strptime('20130701000000', constants.GENERAL_DATE_FORMAT)
    predict_daily_currency_pair(start, end, '4')
    #'''

def predict_daily_currency_pair(start, end, suffix):
    top = [1, 2, 5, 10, 20, 50, 100, 200, 500]
    #top = [1, 2, 5, 10]
    num_nodes = max(top)
    
    profit = []
    invested = []
    performance = []
    for t in range(len(top)):
        profit.append(0)
        invested.append(0)
        performance.append(0)

    ind1_profit = []
    ind1_invested = []
    ind1_performance = []
    for t in range(len(top)):
        ind1_profit.append(0)
        ind1_invested.append(0)
        ind1_performance.append(0)

    ind2_profit = []
    ind2_invested = []
    ind2_performance = []
    for t in range(len(top)):
        ind2_profit.append(0)
        ind2_invested.append(0)
        ind2_performance.append(0)

    ind8_profit = []
    ind8_invested = []
    ind8_performance = []
    for t in range(len(top)):
        ind8_profit.append(0)
        ind8_invested.append(0)
        ind8_performance.append(0)

    time = start
    while time<end:
        #we look at the network today but start investing tomorrow - that's why 4 and 5 means Saturday and Sunday (instead of Friday and Saturday)
        if time.weekday()!=4 and time.weekday()!=5:
            #time_str = datetime.strftime(time, constants.GENERAL_DATE_FORMAT)
            
            g_edges = load_graphs.load_time_network(time, data=False)
    
    
            top_nodes = rank_network_nodes(g_edges)
            top_nodes = top_nodes[-num_nodes:]
            
            
            g_trades = load_graphs.load_time_network(time, data=True, nodes=top_nodes)
    
            
            for t in range(len(top)):
                p, i = predict_daily_currency_pair_like_group(g_trades, top_nodes[-top[t]:], time, start, end)
    
                profit[t] = profit[t] + p
                invested[t] = invested[t] + i
                
                print top[t], p, i
    
    
            for t in range(len(top)):
                ind1_top_nodes = calc_independent_nodes(g_edges, top_nodes[-top[t]:], 1)
    
                p, i = predict_daily_currency_pair_like_group(g_trades, ind1_top_nodes, time, start, end)
    
                ind1_profit[t] = ind1_profit[t] + p
                ind1_invested[t] = ind1_invested[t] + i
    
                print top[t], p, i
                 
    
            for t in range(len(top)):
                ind2_top_nodes = calc_independent_nodes(g_edges, top_nodes[-top[t]:], 2)
    
                p, i = predict_daily_currency_pair_like_group(g_trades, ind2_top_nodes, time, start, end)
    
                ind2_profit[t] = ind2_profit[t] + p
                ind2_invested[t] = ind2_invested[t] + i
    
                print top[t], p, i
    
    
            for t in range(len(top)):
                ind8_top_nodes = calc_independent_nodes(g_edges, top_nodes[-top[t]:], None)
    
                p, i = predict_daily_currency_pair_like_group(g_trades, ind8_top_nodes, time, start, end)
    
                ind8_profit[t] = ind8_profit[t] + p
                ind8_invested[t] = ind8_invested[t] + i
    
                print top[t], p, i
             
        time = time + timedelta(days=1)


    
    period = period_length(start, end)

    for t in range(len(top)):    
        performance[t] = 0.0 if invested[t]==0 else profit[t] / (float(invested[t])/period)
        print 'per', top[t], performance[t], profit[t], invested[t], period


    for t in range(len(top)):    
        ind1_performance[t] = 0.0 if ind1_profit[t]==0 else ind1_profit[t] / (float(ind1_invested[t])/period)
        print 'ind1', top[t], ind1_performance[t], ind1_profit[t], ind1_invested[t], period


    for t in range(len(top)):    
        ind2_performance[t] = 0.0 if ind2_profit[t]==0 else ind2_profit[t] / (float(ind2_invested[t])/period)
        print 'ind2', top[t], ind2_performance[t], ind2_profit[t], ind2_invested[t], period

    
    for t in range(len(top)):    
        ind8_performance[t] = 0.0 if ind8_profit[t]==0 else ind8_profit[t] / (float(ind8_invested[t])/period)
        print 'ind8', top[t], ind8_performance[t], ind8_profit[t], ind8_invested[t], period


    visualize.write_results_using_str(performance, 'top_performance_overall_' + suffix)

    visualize.write_results_using_str(ind1_performance, 'ind1_top_performance_overall_' + suffix)

    visualize.write_results_using_str(ind2_performance, 'ind2_top_performance_overall_' + suffix)

    visualize.write_results_using_str(ind8_performance, 'ind8_top_performance_overall_' + suffix)


def predict_daily_currency_pair_like_group(g, top_nodes, time, start, end):
    profit = 0
    invested = 0
    for i in range(len(top_nodes)):
        v = top_nodes[i]

        p, i = predict_daily_currency_pair_like_individual(g, v, time, start, end)
        
        profit = profit + (p if p!=None else 0)
        invested = invested + (i if i!=None else 0)
            
    return profit, invested;


#calculate profit and invested (sum, not avg) for one USD invested on an individual
def predict_daily_currency_pair_like_individual(g, v, time, start, end):
    
    total_invested = 0
    total_profit = 0

    open_time = tomorrow(time)
    max_close_time = None
    
    if g.has_node(v):
        for e in g.out_edges(v, data=True):
            for t in e[2]['data']:
                close_time = t['closeDate'] if t['closeDate']<=end else end
                
                if close_time<open_time:
                    continue
                
                p, i = daily_profit_for_trade_by_rates_by_dates(t, open_time, close_time, accuracy=timedelta(minutes=1))

                if p==None or i==None:
                    continue

                max_close_time = close_time if (max_close_time==None or max_close_time<close_time) else max_close_time
                
                total_profit = total_profit + p         
                total_invested = total_invested + i
                
    if total_invested>0:    
        profit = total_profit/total_invested
        invested = period_length(open_time, max_close_time)
    else:
        profit = None
        invested = None
    
    return profit, invested


def tomorrow(time):
    tomorrow = datetime(time.year, time.month, time.day) + timedelta(days=1)
    return tomorrow


def period_length(start, end):
    period = (end - start).days + 1

    return period

    
def daily_profit_for_trade_proportional(t, time):
    open_time = t['openDate']
    close_time = t['closeDate']

    open_date = datetime(open_time.year, open_time.month, open_time.day)
    close_date = datetime(close_time.year, close_time.month, close_time.day)
    period = (close_date - open_date).days + 1

    if period<=0:
        #shouldn't happen...
        #print '###############', period, time, open_date, close_date, t
        return None, None

    profit = float(t['nProfit'])
    profit = profit / period

    amount = t['amount']
    
    return profit, amount


def daily_profit_for_trade_proportional_by_rates(t, time):
    open_time = t['openDate']
    close_time = t['closeDate']

    open_date = datetime(open_time.year, open_time.month, open_time.day)
    close_date = datetime(close_time.year, close_time.month, close_time.day)
    period = (close_date - open_date).days + 1

    if period<=0:
        #shouldn't happen...
        #print '###############', period, time, open_date, close_date, t
        return None, None

    profit, amount = daily_profit_for_trade_by_rates_by_dates(t, open_time, close_time, accuracy=timedelta(minutes=1))

    if profit==None or amount==None:
        return None, None
    
    profit = profit / period

    return profit, amount


def daily_profit_for_trade_by_rates(t, time):
    open_time = datetime(time.year, time.month, time.day)
    close_time = open_time + timedelta(days=1)

    profit, amount = daily_profit_for_trade_by_rates_by_dates(t, open_time, close_time, accuracy=timedelta(minutes=1))

    if profit==None or amount==None:
        return None, None

    return profit, amount


def daily_profit_for_trade_by_rates_starting_from_tomorrow_proportional(t, time):
    open_time = datetime(time.year, time.month, time.day) + timedelta(days=1)
    close_time = t['closeDate']
    
    if open_time>=close_time:
        return None, None

    open_date = datetime(open_time.year, open_time.month, open_time.day)
    close_date = datetime(close_time.year, close_time.month, close_time.day)
    period = (close_date - open_date).days + 1

    if period<=0:
        #shouldn't happen...
        #print '###############', period, time, open_date, close_date, t
        return None, None

    profit, amount = daily_profit_for_trade_by_rates_by_dates(t, open_time, close_time, accuracy=timedelta(minutes=1))

    if profit==None or amount==None:
        return None, None
    
    profit = profit / period

    return profit, amount


def daily_profit_for_trade_by_rates_by_dates(t, open_time, close_time, accuracy=timedelta(minutes=1)):    
    #Important insights:
    #1. I assume that the DollarAmount and AmountInUnitsDecimal fields are correct and that the Leverage field might be wrong...
    #2. NetProfit contains also the spread which may be a bit high for small profits
    #3. Guy database is not accurate enough - instead I use eToro's rate for other trades which occurred around the required time

    amount = float(t['amount'].replace(',', ''))
    
    open_rate = daily_currency_rates4.get_rate(t['buyCurAbbreviation'], t['sellCurAbbreviation'], open_time, accuracy)
    close_rate = daily_currency_rates4.get_rate(t['buyCurAbbreviation'], t['sellCurAbbreviation'], close_time, accuracy)

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
    if instrument not in daily_currency_rates3.get_instruments():
        buy = curr2
        sell = 'USD'    
    
    close_rate = daily_currency_rates4.get_rate(buy, sell, close_time, accuracy=timedelta(days=1))
    
    if close_rate==None:
        return None
    
        
    if sell=='USD':
        return close_rate
    
    if buy=='USD':
        return 1.0/close_rate



def rank_network_nodes(g):
    ranked_nodes = [(real_in_degree(g, v), v) for v in g.nodes()]
    ranked_nodes.sort()
    ranked_nodes = [e[1] for e in ranked_nodes]
     
    return ranked_nodes


def real_out_degree(g, v):
    d = g.out_degree(v) if g.has_node(v) else 0;
         
    return d


def real_in_degree(g, v):
    d = g.in_degree(v) if g.has_node(v) else 0;
     
    return d


def calc_overall_performance(top, performance):
    overall = {}
    for i in range(len(top)):
        o = 1.0
        for p in performance[i]:
            o = o * (1.0 + p)
        overall[top[i]] = o
    return overall


def calc_independent_nodes(g, top_nodes, hops):
    independent_nodes = [top_nodes[-1]]
    
    for i in range(2, len(top_nodes)+1):
        v = top_nodes[-i]
        if independent(g, independent_nodes, v, hops):
            independent_nodes.insert(0, v)
    
    return independent_nodes


def independent(g, nodes, v, hops):

    r = reachable(g, v, 'out', hops)
    r.union_update( reachable(g, v, 'in', hops) )
    
    r.intersection_update(nodes)
    
    return len(r)==0


def reachable(g, v, direction, hops):
    
    visited = sets.Set()
    visited.add(v)   
    visiting = [(v, 0)]
    while len(visiting)>0:
        first = visiting[0]
        visiting.remove(first)
        v1 = first[0]
        cur_hops = first[1]

        if cur_hops==hops:
            break

        if direction=='out':
            edges = g.out_edges(v1)
        else:
            edges = g.in_edges(v1)
           
        for e in edges:
            if direction=='out':
                v2 = e[1]
            else:
                v2 = e[0]
            
            if v2 not in visited:
                visited.add(v2)
                visiting.append((v2, cur_hops+1))

    return visited



#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
