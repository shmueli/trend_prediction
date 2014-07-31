import matplotlib
import load_attractiveness
matplotlib.use('Agg')

import pylab
from scipy import stats

from utils import visualize as vis

from dynamics import load_dynamics

from datetime import datetime

from helpers import constants


def execute():
    attr_times = load_attractiveness.load('attr_times')
    attr_daily_in_degree = to_dict(attr_times, load_attractiveness.load('attr_daily_in_degree'))
    #attr_daily_in_degree = to_dict(attr_times, load_attractiveness.load('attr_daily_dist'))
    #attr_pos = to_dict(attr_times, load_attractiveness.load('pos'))
    #attr_neg = to_dict(attr_times, load_attractiveness.load('neg'))


    dyn_times = load_dynamics.load('times')
    dyn_nodes = to_dict(dyn_times,load_dynamics.load('g_nodes'))
    dyn_edges = to_dict(dyn_times, load_dynamics.load('prev_g_edges'))
    dyn_added_edges = to_dict(dyn_times, load_dynamics.load('added_edges'))
    #dyn_removed_edges = to_dict(dyn_times, load_dynamics.load('removed_edges'))

    data1 = []
    data2 = []
    data1_norm = []
    data2_norm = []
    for time_str in attr_times:
        if time_str not in dyn_nodes:
            continue
        
        time = datetime.strptime(time_str, '%Y%m%d%H%M%S')
        
        if time.weekday() == 5 or time.weekday() == 6:
            continue
         
        #'''
        d1 = float(attr_daily_in_degree[time_str])
        n1 = float(dyn_edges[time_str])
        d2 = float(dyn_added_edges[time_str])
        #d2 = float(dyn_removed_edges[time_str])
        n2 = float(dyn_edges[time_str])
        #'''

        data1.append(d1)
        data2.append(d2)
        data1_norm.append(d1/n1)
        data2_norm.append(d2/n2)

    plot_values(range(len(data1)), data1, 'attr', 'added', 'data1')
    plot_values(range(len(data2)), data2, 'attr', 'added', 'data2')
    plot_values(data1, data2, 'attr', 'added', 'data_contrast')
    slope, intercept, r_value, p_value, std_err = stats.linregress(data1, data2)
    print r_value, r_value**2

    plot_values(range(len(data1_norm)), data1_norm, 'attr', 'added', 'data1_norm')
    plot_values(range(len(data2_norm)), data2_norm, 'attr', 'added', 'data2_norm')
    plot_values(data1_norm, data2_norm, 'attr', 'added', 'data_norm_contrast')
    slope, intercept, r_value, p_value, std_err = stats.linregress(data1_norm, data2_norm)
    print r_value, r_value**2
    
    

def plot_values(X, Y, xlabel, ylabel, suffix, ptype='plot'):
    output_filename = constants.ATTRACTIVENESS_FOLDER_NAME + constants.DATASET + '_' + suffix

    X1 = [X[i] for i in range(len(X)) if X[i]>0 and Y[i]>0]
    Y1 = [Y[i] for i in range(len(X)) if X[i]>0 and Y[i]>0]
    X = X1
    Y = Y1
    
    pylab.close("all")
    
    pylab.figure(figsize=(8, 7))

    #pylab.rcParams.update({'font.size': 20})

    pylab.scatter(X, Y)
    
    #pylab.axis(vis.get_bounds(X, Y, False, False))

    #pylab.xscale('log')
    pylab.yscale('log')

    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)   
    #pylab.xlim(0.1,1)
    #pylab.ylim(ymin=0.01)
    #pylab.tight_layout()

    pylab.savefig(output_filename + '.pdf')


def to_dict(a1, a2):
    d = {}
    for i in range(len(a1)):
        d[a1[i]] = a2[i]
    return d

#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
