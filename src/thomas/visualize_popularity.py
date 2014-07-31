import matplotlib
matplotlib.use('Agg')

import pylab

import helpers.constants as constants
from popularity import load_daily_popularity

from datetime import datetime, timedelta

def execute():
    plot_popularity()


def plot_popularity():

    print 'Loading...'
    popularity = load_daily_popularity.load(1)

    print 'Plotting...'
    X = []
    Y = []
    for v in popularity:
        for time_str in popularity[v]:
            pop = popularity[v][time_str]
            in_degree = pop[0]

            time = datetime.strptime(time_str, '%Y%m%d%H%M%S')
            time2 = time + timedelta(days=7)
            time_str2 = time2.strftime('%Y%m%d%H%M%S')

            if time_str2 not in popularity[v]:
                in_degree2 = 0
            else:
                pop2 = popularity[v][time_str2]
                in_degree2 = pop2[0]

            diff = in_degree2 - in_degree
            
            if in_degree<1:
                continue
            if diff<1:
                continue

            X.append(in_degree)
            Y.append(diff)

    #X = X[:100]
    #Y = Y[:100]

    plot_values(X, Y, 'in_degree', 'diff_in', 'preferential_attachment')


def plot_values(X, Y, xlabel, ylabel, suffix):
    output_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + suffix

    
    pylab.figure(figsize=(8, 7))

    pylab.rcParams.update({'font.size': 20})

    pylab.scatter(X, Y)
    
    '''
    #smoothing
    s = np.square(np.max(Y))
    tck = interpolate.splrep(X, Y, s=s)
    Y_smooth = interpolate.splev(X, tck)
    pylab.plot(X, Y_smooth)
    '''

    #pylab.axis(vis.get_bounds(X, Y, False, False))

    pylab.xscale('log')
    pylab.yscale('log')

    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)   

    #pylab.tight_layout()

    pylab.savefig(output_filename + '.pdf')


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
