import matplotlib
matplotlib.use('Agg')

import helpers.constants as constants
from utils import visualize as vis

import pylab
#import numpy as np
import sets

def execute():
    top_nodes = vis.load_results_using_eval('top_nodes')

    #plot_popularity(top_nodes)
    #plot_performance(top_nodes)
    plot_popularity(top_nodes)


def plot_popularity(top_nodes):

    for v in top_nodes:
        print v
        
        popularity = vis.load_results('popularity_' + str(v))
        popularity = aggregate_popularity(popularity)

        plot_values(range(len(popularity)), popularity, 'Day', 'Number of mirroring traders', 'popularity_' + str(v))
        

def plot_performance(top_nodes):
    for v in top_nodes:        
        print v

        performance = vis.load_results_using_eval('performance_' + str(v))
        performance = aggregate_performance(performance)
        
        plot_values(range(len(performance)), performance, 'Day', 'Performance', 'performance_' + str(v))


def plot_pop_and_per(top_nodes):
    for v in top_nodes:     
        print v
        
        popularity = vis.load_results('popularity_' + str(v))
        popularity = aggregate_popularity(popularity)

        performance = vis.load_results_using_eval('performance_' + str(v))
        performance = aggregate_performance(performance)

        plot_two_values(range(len(popularity)), popularity, performance, 'Day', 'Number of followers', 'performance', 'pop_and_per_' + str(v))


def aggregate_popularity(popularity):
    '''
    num_nodes = vis.load_results('num_nodes')
    popularity = [popularity[j]/num_nodes[j] for j in range(len(popularity))]
    '''
    
    '''
    last = 0
    for i in range(len(popularity)):
        if popularity[i]!=0:
            last = popularity[i]
        elif popularity[i]==0 and last!=0:
            popularity[i] = last
    '''

    #popularity = popularity[100:-50]
    
    return popularity


def aggregate_performance(performance):    
    agg_p = []
    for i in range(len(performance)):
        agg_p.append([])
        
        profit = 0.0
        invested = 0.0

        positions = sets.Set()
        
        days = 0.0
        for j in range(max(0,i+1-100), i+1):
            for p in performance[j]:
                if p['PositionID'] not in positions:        
                    profit = profit + p['NetProfit']
                    positions.add(p['PositionID'])
                    
                invested = invested + p['DollarsAmount']
            days = days+1.0

        invested = invested / days
            
        if invested>0:
            #print profit, invested
            agg_p[i] = profit / invested
        else:
            agg_p[i] = 0.0
    
    agg_p = agg_p[100:-50]

    return agg_p
    

def plot_values(X, Y, xlabel, ylabel, suffix):
    output_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + suffix

    
    pylab.figure(figsize=(8, 7))

    pylab.rcParams.update({'font.size': 20})

    #pylab.scatter(X, Y)
    pylab.plot(X, Y)

    pylab.axis(vis.get_bounds(X, Y, False, False))

    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)   

    pylab.tight_layout()

    pylab.savefig(output_filename + '.pdf')


def plot_two_values(X, Y1, Y2, xlabel, y1label, y2label, suffix):
    output_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + suffix

    pylab.figure(figsize=(15, 7))

    pylab.rcParams.update({'font.size': 20})

    pylab.xlabel(xlabel)

    ax1 = pylab.gca()
    ax1.plot(X, Y1, 'b')
    ax1.plot(X, [0.0 for x in X], 'b--')
    ax1.set_ylabel(y1label, color='b')   
    for tl in ax1.get_yticklabels():
        tl.set_color('b')
    

    ax2 = pylab.twinx()
    ax2.plot(X, Y2, 'r')
    ax2.plot(X, [0.0 for x in X], 'r--')
    ax2.set_ylabel(y2label, color='r')   
    for tl in ax2.get_yticklabels():
        tl.set_color('r')

    pylab.savefig(output_filename + '.pdf')


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
