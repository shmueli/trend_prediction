#ranked nodes - (tomorrow, end-of-trades)

import sys
sys.path.insert(0, '../')

from datetime import datetime, timedelta
import sets

from popularity import calc_individual_returns
from graphs import load_graphs
import helpers.constants as constants
from utils import visualize


def execute():
    #'''
    start = datetime.strptime('20110701000000', constants.GENERAL_DATE_FORMAT)
    end = datetime.strptime('20120101000000', constants.GENERAL_DATE_FORMAT)
    store_daily_returns_for_all_individuals(start, end, 'ranked_1')
    #'''

    #'''
    start = datetime.strptime('20120101000000', constants.GENERAL_DATE_FORMAT)
    end = datetime.strptime('20120701000000', constants.GENERAL_DATE_FORMAT)
    store_daily_returns_for_all_individuals(start, end, 'ranked_2')
    #'''

    #'''
    start = datetime.strptime('20120701000000', constants.GENERAL_DATE_FORMAT)
    end = datetime.strptime('20130101000000', constants.GENERAL_DATE_FORMAT)
    store_daily_returns_for_all_individuals(start, end, 'ranked_3')
    #'''

    #'''
    start = datetime.strptime('20130101000000', constants.GENERAL_DATE_FORMAT)
    end = datetime.strptime('20130701000000', constants.GENERAL_DATE_FORMAT)
    store_daily_returns_for_all_individuals(start, end, 'ranked_4')
    #'''


def store_daily_returns_for_all_individuals(start, end, suffix):
    top = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    ind = [0, 1, 2, -1]
    
    profit = {}
    sum_invested = {}
    avg_invested = {}
    performance = {}
    pos_trades = {}
    neg_trades = {}
    bal_trades = {}
    ignored_trades = {}
    for i in ind:
        profit[i] = []
        sum_invested[i] = []
        avg_invested[i] = []
        performance[i] = []
        pos_trades[i] = []
        neg_trades[i] = []
        bal_trades[i] = []
        ignored_trades[i] = []

        for t in range(len(top)):
            profit[i].append(0)
            sum_invested[i].append(0)
            avg_invested[i].append(0)
            performance[i].append(0)
            pos_trades[i].append(0)
            neg_trades[i].append(0)
            bal_trades[i].append(0)
            ignored_trades[i].append(0)

    time = start
    while time<end:
        #we look at the network today but start investing tomorrow - that's why 4 and 5 means Saturday and Sunday (instead of Friday and Saturday)
        if time.weekday()!=4 and time.weekday()!=5:
            #time_str = datetime.strftime(time, constants.GENERAL_DATE_FORMAT)
            
            num_nodes = max(top)
    
            g_edges = load_graphs.load_time_network(time, data=False)

            ordered_nodes = rank_network_nodes(g_edges)
            
            num_nodes = min(num_nodes, len(ordered_nodes))
 
            top_nodes = ordered_nodes[0:num_nodes]

            g_trades = load_graphs.load_time_network(time, data=True, nodes=top_nodes)

            individuals = {}
            for t in range(len(top)):
                for i in ind:
                    ind_top_nodes, dep_top_nodes = calc_independent_nodes(g_edges, top_nodes, top[t], i)

                    for v in ind_top_nodes:
                        if v not in individuals:
                            individuals[v] = calc_individual_returns.calc_returns_for_individual(g_trades, v, calc_individual_returns.tomorrow(time), end)
                            
                    [grp_profit, grp_invested, grp_pos_trades, grp_neg_trades, grp_bal_trades, grp_ignored_trades, grp_period, grp_ROI] = calc_individual_returns.calc_returns_for_group_given_individuals(individuals, ind_top_nodes) 
        
                    if grp_ROI!=None:
                        profit[i][t] = profit[i][t] + grp_ROI
                        
                    sum_invested[i][t] = sum_invested[i][t] + grp_period #invest one dollar in the group for the entire period

                    pos_trades[i][t] = pos_trades[i][t] + grp_pos_trades
                    neg_trades[i][t] = neg_trades[i][t] + grp_neg_trades
                    bal_trades[i][t] = bal_trades[i][t] + grp_bal_trades
                    ignored_trades[i][t] = ignored_trades[i][t] + grp_ignored_trades
                    
                    print top[t], i, profit[i][t], sum_invested[i][t], pos_trades[i][t], neg_trades[i][t], bal_trades[i][t], ignored_trades[i][t]
                 
             
        time = time + timedelta(days=1)

    period = calc_individual_returns.period_length(start, end)

    print 'Final Results'
    for t in range(len(top)):    
        for i in ind:
            avg_invested[i][t] = 0.0 if sum_invested[i][t]==0 else ( float(sum_invested[i][t]) / float(period) )
            performance[i][t] = 0.0 if sum_invested[i][t]==0 else ( profit[i][t] / float(avg_invested[i][t]) )
            print top[t], i, profit[i][t], sum_invested[i][t], avg_invested[i][t], performance[i][t], pos_trades[i][t], neg_trades[i][t], bal_trades[i][t], ignored_trades[i][t]

    visualize.write_results_using_str(profit, 'top_profit_overall_' + suffix)
    visualize.write_results_using_str(sum_invested, 'top_sum_invested_overall_' + suffix)
    visualize.write_results_using_str(avg_invested, 'top_avg_invested_overall_' + suffix)
    visualize.write_results_using_str(performance, 'top_performance_overall_' + suffix)
    visualize.write_results_using_str(pos_trades, 'top_pos_trades_overall_' + suffix)
    visualize.write_results_using_str(neg_trades, 'top_neg_trades_overall_' + suffix)
    visualize.write_results_using_str(bal_trades, 'top_bal_trades_overall_' + suffix)
    visualize.write_results_using_str(ignored_trades, 'top_ignored_trades_overall_' + suffix)


def rank_network_nodes(g, min_in_degree=None):
    ranked_nodes = [(real_in_degree(g, v), v) for v in g.nodes()]
    ranked_nodes.sort(reverse=True)
    
    if min_in_degree==None:
        ranked_nodes = [e[1] for e in ranked_nodes]
    else:
        ranked_nodes = [e[1] for e in ranked_nodes if e[0]>=min_in_degree]
    
    return ranked_nodes


def real_in_degree(g, v):
    d = g.in_degree(v) if g.has_node(v) else 0;
     
    return d



def calc_independent_nodes(g, top_nodes, top, hops, replace=False):
    ind_nodes = [top_nodes[0]]
    dep_nodes = []
    
    ancestors = reachable(g, top_nodes[0], 'out', hops)
    
    cnt = 1
    for i in range(1, len(top_nodes)):
        if cnt>=top:
            break
        
        v = top_nodes[i]

        r = reachable(g, v, 'out', hops)
        inter = r.intersection(ancestors)
        
        if len(inter)==0:
            ind_nodes.append(v)
            ancestors.union_update(r)
            
            if replace:
                cnt = cnt+1
        else:
            dep_nodes.append(v)

        if not replace:
            cnt=cnt+1
            
    #print replace, cnt, top
        
    return ind_nodes, dep_nodes

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
