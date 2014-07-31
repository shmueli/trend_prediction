# ranked nodes - (tomorrow, end-of-trades) - with net replace

import sys
sys.path.insert(0, '../')

from datetime import timedelta
from graphs import load_graphs
from returns import load_daily_returns, load_daily_limited_returns, load_daily_old_returns, load_daily_old_limited_returns, load_period_returns, load_period_limited_returns
import random
import sets
import json

from helpers import constants


min_in_degrees = [0]
top = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
ind = [0, 1, 2, -1]
repeats = 1
replace = [True, False]
ordering_type = 'ranked'
returns_type = 'period'


def execute():
    for min_in_degree in min_in_degrees:
        for p in constants.PERIODS_TRI_MONTHLY:
            store_daily_returns_for_all_individuals(constants.PERIODS_TRI_MONTHLY, p, min_in_degree, top, ind, repeats, replace, ordering_type, returns_type)


def store_daily_returns_for_all_individuals(periods, p, min_in_degree, top, ind, repeats, replace, ordering_type, returns_type):
    start = periods[p]['start']
    end = periods[p]['end'] 
    
    profit = {}
    invested = {}
    pos_trades = {}
    neg_trades = {}
    bal_trades = {}
    ignored_trades = {}
    period = {}
    ROI = {}
    selected = {}
    for j in range(repeats):
        profit[j] = {}
        invested[j] = {}
        pos_trades[j] = {}
        neg_trades[j] = {}
        bal_trades[j] = {}
        ignored_trades[j] = {}
        period[j] = {}
        ROI[j] = {}
        selected[j] = {}        
        for r in replace:
            profit[j][r] = {}
            invested[j][r] = {}
            pos_trades[j][r] = {}
            neg_trades[j][r] = {}
            bal_trades[j][r] = {}
            ignored_trades[j][r] = {}
            period[j][r] = {}
            ROI[j][r] = {}
            selected[j][r] = {}
    
            for i in ind:
                profit[j][r][i] = {}
                invested[j][r][i] = {}
                pos_trades[j][r][i] = {}
                neg_trades[j][r][i] = {}
                bal_trades[j][r][i] = {}
                ignored_trades[j][r][i] = {}
                period[j][r][i] = {}
                ROI[j][r][i] = {}
                selected[j][r][i] = {}
        
                for t in top:
                    profit[j][r][i][t] = []
                    invested[j][r][i][t] = []
                    pos_trades[j][r][i][t] = []
                    neg_trades[j][r][i][t] = []
                    bal_trades[j][r][i][t] = []
                    ignored_trades[j][r][i][t] = []
                    period[j][r][i][t] = []
                    ROI[j][r][i][t] = []
                    selected[j][r][i][t] = []

    time = start
    while time < end:

        g_edges = load_graphs.load_time_network(time, data=False)

        ordered_nodes = rank_network_nodes(g_edges, min_in_degree=min_in_degree)
        
        num_nodes = len(ordered_nodes)

        random_nodes = []
        for j in range(repeats):
            if ordering_type == 'random':
                random.shuffle(ordered_nodes)
            random_nodes.extend(ordered_nodes)

        for j in range(repeats):    
            top_nodes = random_nodes[num_nodes * j : num_nodes * (j + 1)]

            for r in replace:
                for i in ind:
                    ind_nodes = calc_independent_nodes(g_edges, top_nodes, max(top), i, r)
                    
                    for t in top:
                        ind_top_nodes = list(ind_nodes[:min(t, len(ind_nodes))])
                        
                        if returns_type == 'daily':
                            [grp_profit, grp_invested, grp_pos_trades, grp_neg_trades, grp_bal_trades, grp_ignored_trades, grp_period, grp_ROI] = load_daily_returns.calc_returns_for_group(ind_top_nodes, time)
                        elif returns_type == 'daily_limited':
                            [grp_profit, grp_invested, grp_pos_trades, grp_neg_trades, grp_bal_trades, grp_ignored_trades, grp_period, grp_ROI] = load_daily_limited_returns.calc_returns_for_group(ind_top_nodes, time)
                        elif returns_type == 'daily_old':
                            [grp_profit, grp_invested, grp_pos_trades, grp_neg_trades, grp_bal_trades, grp_ignored_trades, grp_period, grp_ROI] = load_daily_old_returns.calc_returns_for_group(ind_top_nodes, time)
                        elif returns_type == 'daily_old_limited':
                            [grp_profit, grp_invested, grp_pos_trades, grp_neg_trades, grp_bal_trades, grp_ignored_trades, grp_period, grp_ROI] = load_daily_old_limited_returns.calc_returns_for_group(ind_top_nodes, time)
                        elif returns_type == 'period':
                            [grp_profit, grp_invested, grp_pos_trades, grp_neg_trades, grp_bal_trades, grp_ignored_trades, grp_period, grp_ROI] = load_period_returns.calc_returns_for_group(ind_top_nodes, time)
                        elif returns_type == 'period_limited':
                            [grp_profit, grp_invested, grp_pos_trades, grp_neg_trades, grp_bal_trades, grp_ignored_trades, grp_period, grp_ROI] = load_period_limited_returns.calc_returns_for_group(ind_top_nodes, time)
            
                        profit[j][r][i][t].append(grp_profit)
                        invested[j][r][i][t].append(grp_invested)        
                        pos_trades[j][r][i][t].append(grp_pos_trades)
                        neg_trades[j][r][i][t].append(grp_neg_trades)
                        bal_trades[j][r][i][t].append(grp_bal_trades)
                        ignored_trades[j][r][i][t].append(grp_ignored_trades)

                        period[j][r][i][t].append(grp_period)
                        ROI[j][r][i][t].append(grp_ROI)
                            
                        
                        selected[j][r][i][t].append(len(ind_top_nodes))
             
        time = time + timedelta(days=1)

    suffix = ordering_type + '_' + returns_type + '_' + str(min_in_degree) + '_' + str(p)
    
    json.dump(profit, open(constants.WISDOM_FOLDER_NAME + 'profit' + '_' + suffix, 'w'))
    json.dump(invested, open(constants.WISDOM_FOLDER_NAME + 'invested' + '_' + suffix, 'w'))
    json.dump(pos_trades, open(constants.WISDOM_FOLDER_NAME + 'pos_trades' + '_' + suffix, 'w'))
    json.dump(neg_trades, open(constants.WISDOM_FOLDER_NAME + 'neg_trades' + '_' + suffix, 'w'))
    json.dump(bal_trades, open(constants.WISDOM_FOLDER_NAME + 'bal_trades' + '_' + suffix, 'w'))
    json.dump(ignored_trades, open(constants.WISDOM_FOLDER_NAME + 'ignored_trades' + '_' + suffix, 'w'))
    json.dump(period, open(constants.WISDOM_FOLDER_NAME + 'period' + '_' + suffix, 'w'))
    json.dump(ROI, open(constants.WISDOM_FOLDER_NAME + 'ROI' + '_' + suffix, 'w'))
    json.dump(selected, open(constants.WISDOM_FOLDER_NAME + 'selected' + '_' + suffix, 'w'))


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
        
    return ind_nodes


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
