from datetime import datetime, timedelta
import sets

import daily_currency_rates4
from graphs import load_graphs
import helpers.constants as constants
from utils import visualize
from wisdom import daily_currency_rates3


start = datetime.strptime('20120101000000', constants.GENERAL_DATE_FORMAT)
end = datetime.strptime('20120701000000', constants.GENERAL_DATE_FORMAT)


def execute():
    daily_currency_rates4.load()
    
    #calc_pop_and_per(500)
    predict_daily_currency_pair(500)



def calc_pop_and_per(num_nodes):
    #top = [1, 2, 5, 10, 20, 50, 100, 200]
    top = [1, 2, 5]
    
    performance = []
    for t in range(len(top)):
        performance.append([])

    ind_performance = []
    for t in range(len(top)):
        ind_performance.append([])

    time = start
    while time<end:
        time_str = datetime.strftime(time, constants.GENERAL_DATE_FORMAT)
        
        g_edges = load_graphs.load_time_network(time_str, data=False)


        top_nodes = rank_network_nodes(g_edges)
        top_nodes = top_nodes[-num_nodes:]
        
        
        g_trades = load_graphs.load_time_network(time_str, data=True, nodes=top_nodes)

        
        for t in range(len(top)):
            p = invest_like_group(g_trades, top_nodes[-top[t]:], time)
            print 'per', time, top[t], p
            performance[t].append(p)


        for t in range(len(top)):
            ind_top_nodes = calc_independent_nodes(g_edges, top_nodes[-top[t]:])

            p = invest_like_group(g_trades, ind_top_nodes, time)
            print 'ind', time, top[t], p
            ind_performance[t].append(p)
             
        time = time + timedelta(days=1)



    overall = calc_overall_performance(top, performance)

    for t in range(len(top)):
        visualize.write_results(performance[t], 'top_performance_' + str(top[t]))

    visualize.write_results_using_str(overall, 'top_performance_overall')


    ind_overall = calc_overall_performance(top, ind_performance)

    for t in range(len(top)):
        visualize.write_results(ind_performance[t], 'ind_top_performance_' + str(top[t]))

    visualize.write_results_using_str(ind_overall, 'ind_top_performance_overall')


def invest_like_group(g, top_nodes, time):
    p = 0
    for i in range(len(top_nodes)):
        v = top_nodes[i]

        temp = invest_like_individual(g, v, time)
        
        p = p + (temp if temp!=None else 0)
        
    p = p/len(top_nodes)
    
    return p;


def invest_like_individual(g, v, time):
        
    totalAmount = 0
    totalProfit = 0
    
    if g.has_node(v):
        for e in g.out_edges(v, data=True):
            for t in e[2]['data']:
                #profit, amount = daily_profit_for_trade_proportional(t, time)
                #profit, amount = daily_profit_for_trade_proportional_by_rates(t, time)
                #profit, amount = daily_profit_for_trade_by_rates(t, time)
                profit, amount = daily_profit_for_trade_by_rates_starting_from_tomorrow_proportional(t, time)
                
                
                if profit==None:
                    continue
                                
                totalProfit = totalProfit + profit         
                totalAmount = totalAmount + amount
    
    if totalAmount>0:    
        p = totalProfit/totalAmount
    else:
        p = None
    
    return p


def predict_daily_currency_pair(num_nodes):
    top = [1, 2, 5, 10, 20, 50, 100]
    #top = [1, 2, 5, 10]
    
    profit = []
    invested = []
    performance = []
    for t in range(len(top)):
        profit.append(0)
        invested.append(0)
        performance.append(0)

    ind_profit = []
    ind_invested = []
    ind_performance = []
    for t in range(len(top)):
        ind_profit.append(0)
        ind_invested.append(0)
        ind_performance.append(0)


    time = start
    while time<end:
        time_str = datetime.strftime(time, constants.GENERAL_DATE_FORMAT)
        
        g_edges = load_graphs.load_time_network(time_str, data=False)


        top_nodes = rank_network_nodes(g_edges)
        top_nodes = top_nodes[-num_nodes:]
        
        
        g_trades = load_graphs.load_time_network(time_str, data=True, nodes=top_nodes)

        
        for t in range(len(top)):
            p, i = predict_daily_currency_pair_like_group(g_trades, top_nodes[-top[t]:], time)

            profit[t] = profit[t] + p
            invested[t] = invested[t] + i
            
            print top[t], p, i


        for t in range(len(top)):
            ind_top_nodes = calc_independent_nodes(g_edges, top_nodes[-top[t]:])

            p, i = predict_daily_currency_pair_like_group(g_trades, ind_top_nodes, time)

            ind_profit[t] = ind_profit[t] + p
            ind_invested[t] = ind_invested[t] + i

            print top[t], p, i
             
        time = time + timedelta(days=1)


    
    period = period_length(start, end)

    for t in range(len(top)):    
        performance[t] = profit[t] / (invested[t]/period)
        print 'per', top[t], performance[t], profit[t], invested[t], period


    for t in range(len(top)):    
        ind_performance[t] = ind_profit[t] / (ind_invested[t]/period)
        print 'ind', top[t], ind_performance[t], ind_profit[t], ind_invested[t], period


    visualize.write_results_using_str(performance, 'top_performance_overall')

    visualize.write_results_using_str(ind_performance, 'ind_top_performance_overall')


def predict_daily_currency_pair_like_group(g, top_nodes, time):
    profit = 0
    invested = 0
    for i in range(len(top_nodes)):
        v = top_nodes[i]

        p, i = predict_daily_currency_pair_like_individual(g, v, time)
        
        profit = profit + (p if p!=None else 0)
        invested = invested + (i if i!=None else 0)
            
    return profit, invested;


#calculate profit and invested (sum, not avg) for one USD invested on an individual
def predict_daily_currency_pair_like_individual(g, v, time):
    
    total_invested = 0
    total_profit = 0

    open_time = tomorrow(time)
    max_close_time = None
    
    if g.has_node(v):
        for e in g.out_edges(v, data=True):
            for t in e[2]['data']:
                close_time = t['CloseOccured'] if t['CloseOccured']<=end else end
                
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
    open_time = t['OpenOccured']
    close_time = t['CloseOccured']

    open_date = datetime(open_time.year, open_time.month, open_time.day)
    close_date = datetime(close_time.year, close_time.month, close_time.day)
    period = (close_date - open_date).days + 1

    if period<=0:
        #shouldn't happen...
        #print '###############', period, time, open_date, close_date, t
        return None, None

    profit = float(t['NetProfit'])
    profit = profit / period

    amount = t['DollarsAmount']
    
    return profit, amount


def daily_profit_for_trade_proportional_by_rates(t, time):
    open_time = t['OpenOccured']
    close_time = t['CloseOccured']

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

    profit, amount = daily_profit_for_trade_by_rates_by_dates(t, open_time, close_time, accuracy=timedelta(hours=1))

    if profit==None or amount==None:
        return None, None

    return profit, amount


def daily_profit_for_trade_by_rates_starting_from_tomorrow_proportional(t, time):
    open_time = datetime(time.year, time.month, time.day) + timedelta(days=1)
    close_time = t['CloseOccured']
    
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

    amount = t['DollarsAmount']

    open_rate = daily_currency_rates4.get_rate(t['Instrument'], open_time, accuracy)
    close_rate = daily_currency_rates4.get_rate(t['Instrument'], close_time, accuracy)

    if open_rate==None or close_rate==None:
        #we didn't find accurate enough rates (i.e. rates around the required time)
        #print '###', open_time, close_time, t['Instrument'], t['PositionID']
        return None, None
    
    
    
    profitPercentage = (close_rate-open_rate) * (1.0 if t['DealSide']=='Long=Buy' else - 1.0)    
    profit = float(t['AmountInUnitsDecimal']) * profitPercentage


    usd_rate = get_usd_rate(t, close_rate)
    profit = profit * usd_rate

    
    #if ( (t['NetProfit']>0 and profit/t['NetProfit']>2) or (profit>0 and t['NetProfit']/profit>2) ):
    #    the calculated profit is significantly different than the NetProfit
    #    print profit, t['NetProfit'], open_rate, close_rate, t

    if profit<0 and (-profit)>amount:
        #the loss cannot be higher than the amount invested
        #print profit, amount
        profit = -amount
    
    return profit, amount


def get_usd_rate(t, close_rate):
    instrument = t['Instrument']
    
    curr = instrument.split('/')
    
    if curr[1]=='USD':
        return 1.0
    
    if curr[0]=='USD':
        return 1.0/close_rate
    
    instrument = 'USD/' + curr[1]
    if instrument not in daily_currency_rates3.get_instruments():
        instrument = curr[1] + '/USD'
    

    
    close_rate = daily_currency_rates4.get_rate(instrument, t['CloseOccured'], accuracy=timedelta(days=1))
        
    curr = instrument.split('/')
    
    if curr[1]=='USD':
        return close_rate
    
    if curr[0]=='USD':
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


def calc_independent_nodes(g, top_nodes):
    independent_nodes = [top_nodes[-1]]
    
    for i in range(2, len(top_nodes)+1):
        v = top_nodes[-i]
        if independent(g, independent_nodes, v):
            independent_nodes.insert(0, v)
    
    return independent_nodes


def independent(g, nodes, v):

    r = reachable(g, v, 'out')
    r.union_update( reachable(g, v, 'in') )
    
    r.intersection_update(nodes)
    
    return len(r)==0


def reachable(g, v, direction):
    visited = sets.Set()
    visited.add(v)
    
    visiting = [v]
    while len(visiting)>0:
        v1 = visiting[0]
        visiting.remove(v1)

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
                visiting.append(v2)
                visited.add(v2)

    return visited



#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
