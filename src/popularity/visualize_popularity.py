import matplotlib
matplotlib.use('Agg')

from datetime import datetime, timedelta
import json

import pylab

import helpers.constants as constants
from utils import visualize as vis


start = datetime.strptime('20110630000000', constants.GENERAL_DATE_FORMAT)
#end = datetime.strptime('20130701000000', constants.GENERAL_DATE_FORMAT)
end = datetime.strptime('20110801000000', constants.GENERAL_DATE_FORMAT)


def execute():
    top_nodes = vis.load_results_using_eval('top_nodes')
    #top_nodes = ['1852246']

    #plot_popularity(top_nodes)
    #plot_performance(top_nodes)
    plot_pop_and_per(top_nodes)


def plot_popularity(top_nodes):

    print 'Loading...'
    popularity = load_popularity()

    print 'Plotting...'    
    for v in top_nodes:
        print v
        
        ind_popularity = extract_popularity_array(popularity, v)
        plot_values(range(len(ind_popularity)), ind_popularity, 'Day', 'Number of mirroring traders', 'popularity_' + str(v))
        

def plot_performance(top_nodes):

    print 'Loading...'
    performance = load_performance()

    print 'Plotting...'    
    for v in top_nodes:        
        print v

        ind_performance = extract_performance_array(performance, v)
        ind_performance = aggregate_performance(ind_performance)
        
        plot_values(range(len(ind_performance)), ind_performance, 'Day', 'Performance', 'performance_' + str(v))


def plot_pop_and_per(top_nodes):

    print 'Loading...'
    popularity = load_popularity()
    performance = load_performance()

    print 'Plotting...'
    for v in top_nodes:     
        print v
        
        ind_popularity = extract_popularity_array(popularity, v)

        ind_performance = extract_performance_array(performance, v)
        ind_performance = aggregate_performance(ind_performance)

        plot_two_values(range(len(ind_popularity)), ind_popularity, ind_performance, 'Day', 'Number of followers', 'performance', 'pop_and_per_' + str(v))


def load_popularity():
    input_filename = 'X:/workspace/trend_prediction_out/etoro/daily_period/daily_popularity/popularity'
    
    popularity = json.load(open(input_filename, 'r'))
    return popularity
 

def load_performance():
    input_filename = 'X:/workspace/trend_prediction_out/etoro/daily_period/daily_returns/returns'

    popularity = json.load(open(input_filename, 'r'))
    return popularity

    
def extract_popularity_array(popularity, v):
    v = str(v)
    
    result = []
        
    time = start
    while time<end:
        time_str = datetime.strftime(time, constants.GENERAL_DATE_FORMAT) 

        if time.weekday()!=5 and time.weekday()!=6:
            result.append(popularity[v][time_str][0] if time_str in popularity[v] else 0)
        
        time = time + timedelta(days=1)
    
    
    return result


def extract_performance_array(performance, v):
    v = str(v)
    
    result = []
        
    time = start
    while time<end:
        time_str = datetime.strftime(time, constants.GENERAL_DATE_FORMAT) 

        if time.weekday()!=5 and time.weekday()!=6:
            result.append([performance[v][time_str][0], performance[v][time_str][1]] if time_str in performance[v] else [0, 0])
        
        time = time + timedelta(days=1)
    
    
    return result


def aggregate_performance(performance):
    period = 90
       
    agg_p = []
    for i in range(len(performance)):
        agg_p.append([])
        
        profit = 0.0
        invested = 0.0

        days = 0.0
        for j in range(max(0,i+1-period), i+1):
            profit = profit + performance[j][0]
            invested = invested + performance[j][1]
            
            days = days + 1.0

        invested = invested / days
            
        if invested>0:
            agg_p[i] = profit / invested
        else:
            agg_p[i] = 0.0
    
    return agg_p
    

def plot_values(X, Y, xlabel, ylabel, suffix):
    output_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + suffix

    
    pylab.figure(figsize=(8, 7))

    pylab.rcParams.update({'font.size': 20})

    pylab.plot(X, Y)
    
    '''
    #smoothing
    s = np.square(np.max(Y))
    tck = interpolate.splrep(X, Y, s=s)
    Y_smooth = interpolate.splev(X, tck)
    pylab.plot(X, Y_smooth)
    '''

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
