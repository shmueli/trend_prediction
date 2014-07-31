#random nodes - (tomorrow, end-of-trades)

import sys
sys.path.insert(0, '../')

from datetime import datetime, timedelta
import random

from popularity import calc_individual_returns
from graphs import load_graphs
import helpers.constants as constants
from utils import visualize
import winning_strategy_part1


def execute():
    min_in_degrees = [0, 1, 10]
    
    random.seed(1)
        
    for min_in_degree in min_in_degrees:
        #'''
        start = datetime.strptime('20110701000000', constants.GENERAL_DATE_FORMAT)
        end = datetime.strptime('20120101000000', constants.GENERAL_DATE_FORMAT)
        store_daily_returns_for_all_individuals(start, end, min_in_degree, 'random_' + str(min_in_degree) + '_1')
        #'''
    
        #'''
        start = datetime.strptime('20120101000000', constants.GENERAL_DATE_FORMAT)
        end = datetime.strptime('20120701000000', constants.GENERAL_DATE_FORMAT)
        store_daily_returns_for_all_individuals(start, end, min_in_degree, 'random_' + str(min_in_degree) + '_2')
        #'''
    
        #'''
        start = datetime.strptime('20120701000000', constants.GENERAL_DATE_FORMAT)
        end = datetime.strptime('20130101000000', constants.GENERAL_DATE_FORMAT)
        store_daily_returns_for_all_individuals(start, end, min_in_degree, 'random_' + str(min_in_degree) + '_3')
        #'''
    
        #'''
        start = datetime.strptime('20130101000000', constants.GENERAL_DATE_FORMAT)
        end = datetime.strptime('20130701000000', constants.GENERAL_DATE_FORMAT)
        store_daily_returns_for_all_individuals(start, end, min_in_degree, 'random_' + str(min_in_degree) + '_4')
        #'''


def store_daily_returns_for_all_individuals(start, end, min_in_degree, suffix):
    top = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    ind = [0, 1, 2, -1]
    repeats = 5
    
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

            ordered_nodes = winning_strategy_part1.rank_network_nodes(g_edges, min_in_degree=min_in_degree)
            
            num_nodes = min(num_nodes, len(ordered_nodes))
 
            random_nodes = []
            for repeat in range(5):
                random.shuffle(ordered_nodes)
                random_nodes.extend(ordered_nodes[0:num_nodes])

            g_trades = load_graphs.load_time_network(time, data=True, nodes=random_nodes)

            for repeat in range(repeats):
    
                top_nodes = random_nodes[num_nodes*repeat:num_nodes*(repeat+1)]
    
                individuals = {}
                for t in range(len(top)):
                    for i in ind:
                        ind_top_nodes, dep_top_nodes = winning_strategy_part1.calc_independent_nodes(g_edges, top_nodes, top[t], i)
    
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



#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
