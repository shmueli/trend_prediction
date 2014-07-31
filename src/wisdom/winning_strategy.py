# ranked nodes - (tomorrow, end-of-trades) - with net replace

import sys
sys.path.insert(0, '../')

from datetime import timedelta
from graphs import load_graphs
from returns import load_returns_1_new
from returns import load_returns_1_old
from returns import load_returns_30_new
from returns import load_returns_90_new
#from returns import load_returns_end_new
import random
import sets
import json

from helpers import constants


def execute(min_in_degrees, periods, top, ind, repeats, replace, ordering_type, days, old, limited_loss, invested_type):
    for min_in_degree in min_in_degrees:
        for p in periods:
            store_daily_returns_for_all_individuals(periods, p, min_in_degree, top, ind, repeats, replace, ordering_type, days, old, limited_loss, invested_type)


def store_daily_returns_for_all_individuals(periods, p, min_in_degree, top, ind, repeats, replace, ordering_type, days, old, limited_loss, invested_type):
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
                    ind_nodes, out_of = calc_independent_nodes(g_edges, top_nodes, max(top), i)
                    
                    for t in top:
                        #ind_top_nodes = ind_nodes[:min(t, len(ind_nodes))]
                        ind_top_nodes = get_independent_nodes(ind_nodes, out_of, r, t)
                        
                        [grp_profit, grp_invested, grp_pos_trades, grp_neg_trades, grp_bal_trades, grp_ignored_trades, grp_period, grp_ROI] = calc_returns_for_group(ind_top_nodes, time, days, old, limited_loss, invested_type)
            
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

    suffix = get_suffix(ordering_type, days, old, min_in_degree, p)
    
    json.dump(profit, open(constants.WISDOM_FOLDER_NAME + 'profit' + '_' + suffix, 'w'))
    json.dump(invested, open(constants.WISDOM_FOLDER_NAME + 'invested' + '_' + suffix, 'w'))
    json.dump(pos_trades, open(constants.WISDOM_FOLDER_NAME + 'pos_trades' + '_' + suffix, 'w'))
    json.dump(neg_trades, open(constants.WISDOM_FOLDER_NAME + 'neg_trades' + '_' + suffix, 'w'))
    json.dump(bal_trades, open(constants.WISDOM_FOLDER_NAME + 'bal_trades' + '_' + suffix, 'w'))
    json.dump(ignored_trades, open(constants.WISDOM_FOLDER_NAME + 'ignored_trades' + '_' + suffix, 'w'))
    json.dump(period, open(constants.WISDOM_FOLDER_NAME + 'period' + '_' + suffix, 'w'))
    json.dump(ROI, open(constants.WISDOM_FOLDER_NAME + 'ROI' + '_' + suffix, 'w'))
    json.dump(selected, open(constants.WISDOM_FOLDER_NAME + 'selected' + '_' + suffix, 'w'))


def get_suffix(ordering_type, days, old, min_in_degree, p):
    suffix = ordering_type + '_'
    suffix = suffix + str(days) + '_'
    if old:
        suffix = suffix + 'old_'
    else:
        suffix = suffix + 'new_'
    suffix = suffix + str(min_in_degree) + '_'
    suffix = suffix + str(p)
    
    return suffix


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


def calc_independent_nodes(g, top_nodes, top, hops):
    ind_nodes = [top_nodes[0]]
    dep_nodes = []
    out_of = [1]
    
    ancestors = reachable(g, top_nodes[0], 'out', hops)
    
    cnt = 0
    for i in range(1, len(top_nodes)):
        if cnt>=top:
            break
        
        v = top_nodes[i]

        r = reachable(g, v, 'out', hops)
        inter = r.intersection(ancestors)
        
        if len(inter)==0:            
            cnt = cnt+1
            
            ind_nodes.append(v)
            out_of.append(i+1)
            
            ancestors.union_update(r)
        else:
            dep_nodes.append(v)
            
    return ind_nodes, out_of


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


def get_independent_nodes(ind_nodes, out_of, r, t):
    if r:
        nodes = ind_nodes[:min(t, len(ind_nodes))]
    else:
        i = 0
        while i<len(out_of):
            if out_of[i]>t:
                break
            i = i+1
        nodes = ind_nodes[:i]
    return nodes


def calc_returns_for_group(group, date, days, old, limited_loss, invested_type):
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

        r = calc_return_for_individual(v, date, days, old, limited_loss, invested_type)
        
        if r==None:
            continue
        
        [ind_profit, ind_invested, ind_pos_trades, ind_neg_trades, ind_bal_trades, ind_ignored_trades, ind_period, ind_ROI] = r

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


def calc_return_for_individual(v, date, days, old, limited_loss, invested_type):
    r = None
    if days==1 and old==False:
        r = load_returns_1_new.get_return(v, date)
    elif days==1 and old==True:
        r = load_returns_1_old.get_return(v, date)
    elif days==30 and old==False:
        r = load_returns_30_new.get_return(v, date)
    elif days==90 and old==False:
        r = load_returns_90_new.get_return(v, date)
    #elif days=='end' and old==False:
    #    r = load_returns_end_new.get_return(v, date)
     
    if r==None:
        return None

    [ind_profit, ind_units, ind_amount, ind_leverage, ind_period] = r
    
    if invested_type=='amount':
        ind_invested = ind_amount
    elif invested_type=='proportional':
        ind_invested = [(ind_units[i]/ind_leverage[i] if ind_units[i]!=None else None) for i in range(len(ind_units))]
    elif invested_type=='units':
        ind_invested = ind_units
        
    temp_profit = ind_profit
    
    ind_profit = [x for x in ind_profit if x!=None]
    ind_invested = [x for x in ind_invested if x!=None]
    if limited_loss:
        temp_ind_profit = []
        for i in range(len(ind_profit)):
            #'''
            if ind_profit[i]>=0 or -ind_profit[i]<=ind_invested[i]:
                temp_ind_profit.append(ind_profit[i])
            else:
                temp_ind_profit.append(-ind_invested[i])
            #'''
            '''
            if ind_profit[i]>=0:
                temp_ind_profit.append(ind_profit[i])
            else:
                temp_ind_profit.append(0)
            '''
        ind_profit = temp_ind_profit
    ind_profit = sum(ind_profit)
    ind_invested = sum(ind_invested)
    
    ind_pos_trades = len([x for x in temp_profit if x!=None and x>0])
    ind_neg_trades = len([x for x in temp_profit if x!=None and x<0])
    ind_bal_trades = len([x for x in temp_profit if x!=None and x==0])
    ind_ignored_trades = len([x for x in temp_profit if x==None])
    ind_period = sum([x for x in ind_period if x!=None])
    
    if ind_invested==0:
        ind_ROI = 0
    else:
        ind_ROI = float(ind_profit) / float(ind_invested)
        
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
    