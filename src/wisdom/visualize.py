import numpy
import pylab

#import scikits.bootstrap as bs

import json

from helpers import constants

from datetime import timedelta
from wisdom import winning_strategy
from returns import calc_returns

def execute(periods, unified, min_in_degrees, top, ind, repeats, replace, ordering_type, days, old):
    for min_in_degree in min_in_degrees:
        for p in periods:
            if unified==1 or p%unified==1:
                plot_all(periods, unified, p, min_in_degree, top, ind, repeats, replace, ordering_type, days, old)


def plot_all(periods, unified, p, min_in_degree, top, ind, repeats, replace, ordering_type, days, old):

    profit = load_var('profit', periods, unified, p, top, ind, repeats, replace, ordering_type, days, old, min_in_degree)
    invested = load_var('invested', periods, unified, p, top, ind, repeats, replace, ordering_type, days, old, min_in_degree)
    pos_trades = load_var('pos_trades', periods, unified, p, top, ind, repeats, replace, ordering_type, days, old, min_in_degree)
    neg_trades = load_var('neg_trades', periods, unified, p, top, ind, repeats, replace, ordering_type, days, old, min_in_degree)
    bal_trades = load_var('bal_trades', periods, unified, p, top, ind, repeats, replace, ordering_type, days, old, min_in_degree)
    ignored_trades = load_var('ignored_trades', periods, unified, p, top, ind, repeats, replace, ordering_type, days, old, min_in_degree)
    period = load_var('period', periods, unified, p, top, ind, repeats, replace, ordering_type, days, old, min_in_degree)
    ROI = load_var('ROI', periods, unified, p, top, ind, repeats, replace, ordering_type, days, old, min_in_degree)
    selected = load_var('selected', periods, unified, p, top, ind, repeats, replace, ordering_type, days, old, min_in_degree)


    #avg_invested = calc_avg_invested(periods, unified, p, days)
    avg_invested = days
    
    performance = {}
    risk = {}
    neg_risk = {}
    sharpe = {}
    sortino = {}
    for j in repeats:    
        performance[j] = {}
        risk[j] = {}
        neg_risk[j] = {}
        sharpe[j] = {}
        sortino[j] = {}
        for r in replace:
            performance[j][r] = {}
            risk[j][r] = {}
            neg_risk[j][r] = {}
            sharpe[j][r] = {}
            sortino[j][r] = {}
            for i in ind:
                performance[j][r][i] = {}
                risk[j][r][i] = {}
                neg_risk[j][r][i] = {}
                sharpe[j][r][i] = {}
                sortino[j][r][i] = {}
                for t in top:    
                    #temp_period = [(p if p!=None else 0) for p in period[j][r][i][t]]
                    #temp_ROI = [(p if p!=None else 0) for p in ROI[j][r][i][t]]
                    
                    temp_period = [period[j][r][i][t][k] for k in range(len(ROI[j][r][i][t])) if ROI[j][r][i][t][k]!=None]
                    temp_ROI = [ROI[j][r][i][t][k] for k in range(len(ROI[j][r][i][t])) if ROI[j][r][i][t][k]!=None]
                    
                    temp_neg_ROI = [roi for roi in temp_ROI if roi<0]
                    
                    temp_performance = [x/avg_invested*float(100) for x in temp_ROI]
                    #temp_performance = [temp_ROI[k]/temp_period[k]*float(100) for k in range(len(temp_ROI)) if temp_period[k]!=0]
                    
                    performance[j][r][i][t] = numpy.mean(temp_performance)
                    risk[j][r][i][t] = numpy.std(temp_performance)
                    #neg_risk[j][r][i][t] = numpy.std(temp_neg_ROI)
                    sharpe[j][r][i][t] = calc_sharpe(temp_performance)
                    #sortino[j][r][i][t] = calc_sortino(temp_ROI)#, 0, 365)

                    selected[j][r][i][t] = numpy.average(selected[j][r][i][t])
                    
                    #period[j][r][i][t] = numpy.average(temp_period)
                    ROI[j][r][i][t] = numpy.sum(temp_ROI)
                    
                    #profit[j][r][i][t] = numpy.average(profit[j][r][i][t])

                    #pos_trades[j][r][i][t] = numpy.average(pos_trades[j][r][i][t])
                    #neg_trades[j][r][i][t] = numpy.average(neg_trades[j][r][i][t])
                    #bal_trades[j][r][i][t] = numpy.average(bal_trades[j][r][i][t])
                    

    suffix = winning_strategy.get_suffix(ordering_type, days, old, min_in_degree, p)

    plot_data(performance, top, repeats, False, False, 'X', 'Daily ROI (%)', 'performance' + '_' + suffix)

    #plot_data(profit, top, repeats, False, False, 'X', 'profit', 'profit' + '_' + suffix)

    plot_data(ROI, top, repeats, False, False, 'X', 'profit', 'roi' + '_' + suffix)

    plot_data(selected, top, repeats, False, False, 'X', 'Number of selected users', 'selected' + '_' + suffix)

    #plot_per_sel(performance, selected, top, repeats, 'Number of selected users', 'Daily ROI (%)', 'performance_vs_selected' + '_' + suffix)

    plot_data(risk, top, repeats, False, False, 'X', 'risk', 'risk' + '_' + suffix)
    #plot_data(neg_risk, top, repeats, False, False, 'X', 'neg_risk', 'neg_risk' + '_' + suffix)
    plot_data(sharpe, top, repeats, False, False, 'X', 'Sharpe', 'sharpe' + '_' + suffix)
    #plot_data(sortino, top, repeats, False, False, 'X', 'Sortino', 'sortino' + '_' + suffix)

    #plot_beats(performance, top, repeats, '1', '0', 'X', '%', 'network_1_vs_crowd' + '_' + suffix)
    plot_beats(performance, top, repeats, '-1', '0', 'X', '%', 'network_inf_vs_crowd' + '_' + suffix)
    #plot_beats(performance, top, repeats, '-1', '1', 'X', '%', 'network_inf_vs_network_1' + '_' + suffix)



    '''
    plot_data(sum_invested, top, repeats, 'sum_invested', 'sum_invested' + '_' + suffix)
    plot_data(avg_invested, top, repeats, 'avg_invested', 'avg_invested' + '_' + suffix)
    plot_data(performance, top, repeats, 'performance', 'performance' + '_' + suffix)
    plot_data(pos_trades, top, repeats, 'pos_trades', 'pos_trades' + '_' + suffix)
    plot_data(neg_trades, top, repeats, 'neg_trades', 'neg_trades' + '_' + suffix)
    plot_data(bal_trades, top, repeats, 'bal_trades', 'bal_trades' + '_' + suffix)
    plot_data(ignored_trades, top, repeats, 'ignored_trades', 'ignored_trades' + '_' + suffix)
    plot_data(selected, top, repeats, 'selected', 'selected' + '_' + suffix)
    '''

    '''
    p_pos_trades = {}
    p_neg_trades = {}
    p_bal_trades = {}
    for j in repeats:
        p_pos_trades[j] = {}
        p_neg_trades[j] = {}
        p_bal_trades[j] = {}
        for r in replace:
            p_pos_trades[j][r] = {}
            p_neg_trades[j][r] = {}
            p_bal_trades[j][r] = {}
    
            for i in ind:
                p_pos_trades[j][r][i] = {}
                p_neg_trades[j][r][i] = {}
                p_bal_trades[j][r][i] = {}
        
                for t in top:
                    p = float(pos_trades[j][r][i][t]) / float(pos_trades[j][r][i][t] + neg_trades[j][r][i][t] + bal_trades[j][r][i][t])
                    p_pos_trades[j][r][i][t] = p
        
                    p = float(neg_trades[j][r][i][t]) / float(pos_trades[j][r][i][t] + neg_trades[j][r][i][t] + bal_trades[j][r][i][t])
                    p_neg_trades[j][r][i][t] = p
        
                    p = float(bal_trades[j][r][i][t]) / float(pos_trades[j][r][i][t] + neg_trades[j][r][i][t] + bal_trades[j][r][i][t])
                    p_bal_trades[j][r][i][t] = p

    plot_data(p_pos_trades, top, repeats, False, False, 'X', 'p_pos_trades', 'p_pos_trades' + '_' + suffix)
    plot_data(p_neg_trades, top, repeats, False, False, 'X', 'p_neg_trades', 'p_neg_trades' + '_' + suffix)
    plot_data(p_bal_trades, top, repeats, False, False, 'X', 'p_bal_trades', 'p_bal_trades' + '_' + suffix)
    '''
    
    
def calc_avg_invested(periods, unified, p, days):
    start = periods[p]['start']
    end = periods[p+unified-1]['end']
    
    invested = numpy.zeros(calc_returns.period_length(start, end) + days - 1)
    
    i = 0
    for i in range(len(invested)-days):
        time = start + timedelta(days=i) 

        if time.weekday()!=5 and time.weekday()!=6:
            for d in range(days):
                invested[i + d] = invested[i + d] + 1

    filtered_invested = []
    for i in range(len(invested)):
        time = start + timedelta(days=i) 
        if time.weekday()!=5 and time.weekday()!=6:
            filtered_invested.append(invested[i])
    
    avg_invested = numpy.mean(filtered_invested)
    
    return avg_invested
    

def load_var(varname, periods, unified, p, top, ind, repeats, replace, ordering_type, days, old, min_in_degree):
    var = load_single_var(varname, periods, p, top, ind, repeats, replace, ordering_type, days, old, min_in_degree)
    for cur_p in range(p+1, p+unified):
        cur_var = load_single_var(varname, periods, cur_p, top, ind, repeats, replace, ordering_type, days, old, min_in_degree)

        for j in repeats:    
            for r in replace:
                for i in ind:
                    for t in top:
                        var[j][r][i][t].extend(cur_var[j][r][i][t])
    
    return var


def load_single_var(varname, periods, p, top, ind, repeats, replace, ordering_type, days, old, min_in_degree):
    suffix = winning_strategy.get_suffix(ordering_type, days, old, min_in_degree, p)

    input_filename = constants.WISDOM_FOLDER_NAME + varname + '_' + suffix
    var = json.load(open(input_filename, 'r'))

    #'''    
    for j in repeats:    
        for r in replace:
            for i in ind:
                for t in top:
                    #print len(var[j][r][i][t])
                    
                    filtered = []    
                    time = periods[p]['start']
                    for v in var[j][r][i][t]:
                        if time.weekday()!=5 and time.weekday()!=6:
                            filtered.append(v)
                    
                        time = time + timedelta(days=1)
                    var[j][r][i][t] = filtered
                    
                    #print len(var[j][r][i][t])
    #'''

    return var
    
    
def plot_data(data, top, repeats, with_replace, error_bars, xlabel, ylabel, suffix):
    print suffix
    
    output_filename = constants.WISDOM_FOLDER_NAME + suffix

    pylab.figure(figsize=(15, 10))
    
    pylab.rcParams.update({'font.size': 30})

    X = top


    if error_bars:    
        Y, YErr = aggregate_repeats(data, top, repeats, 'false', '0')
        pylab.errorbar(X, Y, yerr=YErr, linewidth=2, color="red", marker='o', markersize=15, markeredgecolor="red", markerfacecolor="white")
    
        Y, YErr = aggregate_repeats(data, top, repeats, 'false', '1')
        pylab.errorbar(X, Y, yerr=YErr, linewidth=2, color="blue", marker='o', markersize=15, markeredgecolor="blue", markerfacecolor="white")
        
        Y, YErr = aggregate_repeats(data, top, repeats, 'false', '-1')
        pylab.errorbar(X, Y, yerr=YErr, linewidth=2, color="green", marker='o', markersize=15, markeredgecolor="green", markerfacecolor="white")
        
        if with_replace:
            Y, YErr = aggregate_repeats(data, top, repeats, 'true', '-1')
            pylab.errorbar(X, Y, yerr=YErr, linewidth=2, color="black", marker='o', markersize=15, markeredgecolor="black", markerfacecolor="white")

    else:
        Y, YErr = aggregate_repeats(data, top, repeats, 'true', '0')
        pylab.plot(X, Y, linewidth=2, color="red", marker='o', markersize=15, markeredgecolor="red", markerfacecolor="white")
    
        print Y
        Y, YErr = aggregate_repeats(data, top, repeats, 'true', '1')
        pylab.plot(X, Y, linewidth=2, color="blue", marker='o', markersize=15, markeredgecolor="blue", markerfacecolor="white")
        
        print Y
        
        Y, YErr = aggregate_repeats(data, top, repeats, 'true', '-1')
        pylab.plot(X, Y, linewidth=2, color="green", marker='o', markersize=15, markeredgecolor="green", markerfacecolor="white")
        
        print Y
        
        if with_replace:
            Y, YErr = aggregate_repeats(data, top, repeats, 'true', '-1')
            pylab.plot(X, Y, linewidth=2, color="black", marker='o', markersize=15, markeredgecolor="black", markerfacecolor="white")

    pylab.xscale('log', basex=10)

    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)

    pylab.legend(['Crowd', 'Network - 1', 'Network - Inf', 'Network - Inf - Replace'], loc='upper left')
    
    pylab.tight_layout()

    pylab.savefig(output_filename + '.pdf')


def plot_per_sel(performance, selected, top, repeats, xlabel, ylabel, suffix):
    print suffix

    output_filename = constants.WISDOM_FOLDER_NAME + suffix

    pylab.figure(figsize=(15, 10))
    
    pylab.rcParams.update({'font.size': 30})

    X, Y = aggregate_per_sel(performance, selected, top, repeats, 'true', '0')
    pylab.plot(X, Y, linewidth=2, color="red", marker='o', markersize=15, markeredgecolor="red", markerfacecolor="white")

    X, Y = aggregate_per_sel(performance, selected, top, repeats, 'true', '1')
    pylab.plot(X, Y, linewidth=2, color="blue", marker='o', markersize=15, markeredgecolor="blue", markerfacecolor="white")

    X, Y = aggregate_per_sel(performance, selected, top, repeats, 'true', '-1')
    pylab.plot(X, Y, linewidth=2, color="green", marker='o', markersize=15, markeredgecolor="green", markerfacecolor="white")

    pylab.xscale('log', basex=10)

    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)

    pylab.legend(['Crowd', 'Network - 1', 'Network - Inf'], loc='upper left')
    
    pylab.tight_layout()

    pylab.savefig(output_filename + '.pdf')


def plot_beats(data, top, repeats, i1, i2, xlabel, ylabel, suffix):
    print suffix
    
    output_filename = constants.WISDOM_FOLDER_NAME + suffix

    pylab.figure(figsize=(15, 10))
    
    pylab.rcParams.update({'font.size': 30})

    X = numpy.arange(len(top))
    Y1, Y2, Y3 = aggregate_beats(data, top, repeats, 'false', i1, i2)
    width = 0.5
    
    pylab.bar(X, Y1, width, color='green')
    pylab.bar(X, Y2, width, bottom=Y1, color='blue')
    pylab.bar(X, Y3, width, bottom=[Y1[i] + Y2[i] for i in range(len(X))], color='red')


    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)

    pylab.legend(['Wins', 'Draws', 'Losses'], loc='lower right')
    
    pylab.xticks(X+width/2., top)

    pylab.tight_layout()

    pylab.savefig(output_filename + '.pdf')


def aggregate_repeats(data, top, repeats, r, i):
    medians = []
    errors = []
    for t in top:
        t_agg = []
        for j in repeats:
            t_agg.append(data[j][r][i][t])
        t_median = numpy.median(t_agg)
        #t_median = numpy.mean(t_agg)
        t_error = 0#confidence_interval(t_agg)
        
        medians.append(t_median)
        errors.append(t_error)
        
    return medians, errors


def aggregate_beats(data, top, repeats, r, i1, i2):
    win = []
    draw = []
    loss = []
        
    for t in top:
        t_win = 0
        t_draw = 0
        t_loss = 0
        for j in repeats:
            if data[j][r][i1][t] > data[j][r][i2][t]:
                t_win = t_win + 1
            elif data[j][r][i1][t] == data[j][r][i2][t]:
                t_draw = t_draw + 1
            else:
                t_loss = t_loss + 1

        win.append(t_win)
        draw.append(t_draw)
        loss.append(t_loss)
        
    return win, draw, loss


# def confidence_interval(data):
#     h = bs.ci(data, statfunction=numpy.median, alpha=0.10, n_samples=1000, method='pi')
#     h = (h[1]-h[0])/2.0
#     return h


def aggregate_per_sel(performance, selected, top, repeats, r, i):
    data_agg = {}
    for t in top:
        for j in repeats:
            x = int(selected[j][r][i][t])
            y = performance[j][r][i][t]
            
            if x not in data_agg:
                data_agg[x] = []
            data_agg[x].append(y)

    for x in data_agg:
        data_agg[x] = numpy.median(data_agg[x])
        
    X = sorted(data_agg.keys())
    Y = [data_agg[x] for x in X]
    return X, Y


def calc_sharpe(returns):
    meanReturns = numpy.mean(returns)
    stdReturns = numpy.std(returns)
    return meanReturns / stdReturns


'''
def calc_sortino(returns, annualMAR, periodsPerYear):
    periodMAR=numpy.log(annualMAR+1)/periodsPerYear
    logreturns=numpy.log(numpy.array(returns)+1)
    underperformance=[(lr-periodMAR) for lr in logreturns if (lr-periodMAR)<0]
    downdeviation=(sum([x**2 for x in underperformance])/len(returns))**0.5
    retperperiod=sum(logreturns)/len(logreturns)
    periodsortino=(retperperiod-periodMAR)/downdeviation
    return periodsortino*(periodsPerYear**0.5)
'''

def calc_sortino(returns):
    neg_returns = [r for r in returns if r<0]

    meanReturns = numpy.mean(returns)
    stdReturns = numpy.std(neg_returns)
    return meanReturns / stdReturns
 
 
#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
