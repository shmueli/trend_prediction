from datetime import datetime, timedelta
import sets

import daily_currency_rates2
from graphs import load_graphs
import helpers.constants as constants
from utils import visualize


rates = None
instruments = None

start = datetime.strptime('20120101000000', constants.GENERAL_DATE_FORMAT)
end = datetime.strptime('20120701000000', constants.GENERAL_DATE_FORMAT)
#end = datetime.strptime('20121231000000', constants.GENERAL_DATE_FORMAT)


def execute():
    #load_graphs.init_connection()
    
    global rates
    global instruments
    rates, instruments = daily_currency_rates2.load()
    
    calc_pop_and_per(2000)


def calc_pop_and_per(num_nodes):
    top = [1, 2, 5, 10, 20, 50, 100, 200, 500]
    
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

        ind_top_nodes = calc_independent_nodes(g_edges, top_nodes)
        
        
        g_trades = load_graphs.load_time_network(time_str, data=True, nodes=top_nodes)

        
        for t in range(len(top)):
            p = invest_like_group(g_trades, top_nodes[-top[t]:], time)
            print 'per', time, top[t], p
            performance[t].append(p)

        for t in range(len(top)):
            p = invest_like_group(g_trades, ind_top_nodes[-top[t]:], time)
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
                profit = daily_profit_for_trade_proportional(t, time)
                #profit = daily_profit_for_trade_rates(t, time)
                
                if profit==None:
                    continue
                                
                amount = float(t['DollarsAmount'])

                totalProfit = totalProfit + profit         
                totalAmount = totalAmount + amount
    
    if totalAmount>0:    
        p = totalProfit/totalAmount
    else:
        p = None
    
    return p


def daily_profit_for_trade_proportional(t, time):
    openDT = t['OpenOccured']
    openDT = datetime(openDT.year, openDT.month, openDT.day)
    closeDT = t['CloseOccured']
    closeDT = datetime(closeDT.year, closeDT.month, closeDT.day)

    profit = float(t['NetProfit'])
    period = (closeDT - openDT).days + 1

    if period<=0:
        print '###############', period, time, openDT, closeDT, t
        return None

    profit = profit / period
    
    return profit


def daily_profit_for_trade_rates(t, time):
    open_date = time
    close_date = open_date + timedelta(days=1)
    
    if open_date not in rates:
        print '###', 'open_date'
        return None
    
    if t['Instrument'] not in rates[open_date]:
        #print t['Instrument'], open_date
        return None
    
    open_rate = rates[open_date][t['Instrument']]
    close_rate = rates[close_date][t['Instrument']]
    
    profitPercentage = (close_rate-open_rate) / open_rate * (1.0 if t['DealSide']=='Long=Buy' else - 1.0)
    
    profit = float(t['DollarsAmount']) * float(t['Leverage']) * profitPercentage
    
    return profit


def rank_network_nodes(g):
    ranked_nodes = [(real_in_degree(g, v), v) for v in g.nodes()]
    ranked_nodes.sort()
    ranked_nodes = [e[1] for e in ranked_nodes]
     
    return ranked_nodes


def real_out_degree(g, v):
    '''
    d = 0
    for e in g.out_edges(v, data=True):
        if valid_edge(g, e, False):
            d = d+1
    '''
    
    d = g.out_degree(v) if g.has_node(v) else 0;
         
    return d


def real_in_degree(g, v):
    '''
    d = 0
    for e in g.in_edges(v, data=True):
        if valid_edge(g, e, False):
            d = d+1
    '''

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


'''
def clean_graph(g):
    g_clean = nx.DiGraph()
    
    for e in g.edges(data=True):
        if valid_edge(g, e, True):
            g_clean.add_edge(e[0], e[1])
            g_clean.edge[e[0]][e[1]]['data']=[]
            
            #maybe need to check recursively???
            for t in e[2]['data']:
                t2 = valid_trade(g, t)
                if t2!=None:
                    t['OpenOccured']=t2['OpenOccured']
                    t['CloseOccured']=t2['CloseOccured']
                    g_clean.edge[e[0]][e[1]]['data'].append(t)
    
    return g_clean


def valid_edge(g, e, self_edges):
    if not self_edges and e[0]==e[1]:
        return False
    
    for t in e[2]['data']:
        if valid_trade(g, t):
            return True

    return False


def valid_trade(g, t):
    if t['Instrument'] not in instruments:
        return None
    
    if t['SocialType']=='Non-social':
        return t
    
    if t['ParentPositionID']==0:
        return None

    for e2 in g.out_edges(t['ParentGCID'], data=True):
        for t2 in e2[2]['data']:
            if t2['PositionID']==t['ParentPositionID']:
                return t2
            
    print '###', t['PositionID'], t['ParentPositionID'], t['GCID'], t['ParentGCID']
    
    return None
'''


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
