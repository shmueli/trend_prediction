import numpy
import pylab

#import scikits.bootstrap as bs

import json

from helpers import constants

from datetime import timedelta


#top = [str(t_int) for t_int in [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]]
top = [str(t_int) for t_int in [1, 2, 5, 10, 20, 50, 100]]
ind = [str(i_int) for i_int in [0, 1, 2, -1]]
replace = ['true', 'false']
repeats = ['1']
d = '10'

min_in_degree = 0
ordering_type = 'random'
returns_type = 'temp'
p = 1


def execute():
    data = load_data()
    suffix = ''
    plot_data(data, top, repeats, False, False, 'X', 'Accuracy', 'simulation' + '_' + suffix)


def load_data():
    data = {}
    for j in repeats:    
        data[j] = {}
        for r in replace:
            data[j][r] = {}
            for i in ind:
                data[j][r][i] = {}
                for t in top:    
                    data[j][r][i][t] = None

    
    input_filename = 'X:/workspace/wisdom/results_compiled/' + 'Means_results_v01_complete.csv'
    reader = open(input_filename)
    line = reader.readline()
    header = line.strip().split(',')
    for line in reader:
        fields = line.strip().split(',')
        
        i = fields[8]
        if i=='Inf':
            i = '-1'
        
        if fields[3]!=d:
            continue
        
        for t_index in range(len(top)):
            t = top[t_index]
            data['1']['false']['0'][t] = float(1) - float(fields[9+17*t_index])
            data['1']['true']['0'][t] = float(1) - float(fields[9+17*t_index])
            
            data['1']['false'][i][t] = float(1) - float(fields[10+17*t_index])
            data['1']['true'][i][t] = float(1) - float(fields[17+17*t_index])
        
    return data
        
    
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
        Y, YErr = aggregate_repeats(data, top, repeats, 'false', '0')
        pylab.plot(X, Y, linewidth=2, color="red", marker='o', markersize=15, markeredgecolor="red", markerfacecolor="white")
    
        Y, YErr = aggregate_repeats(data, top, repeats, 'false', '1')
        pylab.plot(X, Y, linewidth=2, color="blue", marker='o', markersize=15, markeredgecolor="blue", markerfacecolor="white")
        
        Y, YErr = aggregate_repeats(data, top, repeats, 'false', '-1')
        pylab.plot(X, Y, linewidth=2, color="green", marker='o', markersize=15, markeredgecolor="green", markerfacecolor="white")
        
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
