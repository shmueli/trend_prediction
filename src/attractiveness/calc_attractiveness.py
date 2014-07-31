import matplotlib
matplotlib.use('Agg')

from datetime import datetime, timedelta

import numpy as np
from popularity import load_daily_popularity
from ranked_nodes import load_ranked_nodes

from helpers import constants

import json

start = constants.PERIODS[1]['start']
end = constants.PERIODS[4]['end']


def execute():
    top_nodes = load_ranked_nodes.get_ranked_nodes()
    #top_nodes = top_nodes[:10000]
    plot_popularity_attractiveness(top_nodes)
    
    
def plot_popularity_attractiveness(top_nodes):

    print 'Computing attractiveness and plotting...'  

    times = get_times()
    n_days = len(times)

    period_dist = []
    daily_dist = np.zeros(n_days)
    daily_in_degree = np.zeros(n_days)
    
    for v in top_nodes:
        print v
        try:
            ind_values = extract_attractiveness_array(v)
            vv = np.array(ind_values)
            ind_popularity = vv[:,0]
            ind_attractive, regions = calc_attractiveness_std(ind_values, 0.5, 1.0)
            
            period_dist = update_period_distribution(period_dist, regions)
            daily_dist = update_daily_distribution(daily_dist, regions)
            daily_in_degree = update_daily_in_degree(daily_in_degree, regions, ind_values)
            
            # tmp disabled
#             Y = np.array((ind_popularity, ind_attractive)).T
#             Ylabel = ['Number of mirroring traders', 'Attractiveness']
#             plot_mul_values(range(len(ind_popularity)), Y, 'Day', Ylabel, 'pop_and_attr_' + str(v))
        except:
            print 'Failed to process node %d' % v
    
    period_dist = [int(x) for x in period_dist]
    daily_dist = [int(x) for x in daily_dist]
    daily_in_degree = [int(x) for x in daily_in_degree]

    output_folder = constants.ATTRACTIVENESS_FOLDER_NAME
    json.dump(period_dist, open(output_folder + 'attr_period_dist', 'w'))
    json.dump(daily_dist, open(output_folder + 'attr_daily_dist', 'w'))
    json.dump(daily_in_degree, open(output_folder + 'attr_daily_in_degree', 'w'))

    json.dump(times, open(output_folder + 'attr_times', 'w'))
    
    #vis.plot_bins(period_dist, True, True, 'Period size', 'Density', 'attr_period_dist', xminPlot=None)
    #vis.plot_bins(daily_dist, True, True, 'Number of attractive nodes', 'Density', 'attr_daily_dist', xminPlot=None)


def calc_attractiveness_std(values, c1=0.5, c2=1.0, mag_c=0.3):
    v = np.array(values)
    vabs = v[:,0]
    vdiff = ema(v[:,1], 7) # vdiff = v[:,1]
    stdev = np.std(np.abs(vdiff)) # stdev = np.std(vdiff)
    result = np.zeros(len(vdiff))
    
    i = 0
    s = 0
    e = 0
    regions = []
    while (i < len(vdiff)):
        # find attractiveness start
        # NOTE: sign is important - will only take the 'up' direction (attractive)
        if (vdiff[i] > c1 * stdev):
            s = i
            j = s + 1
            
            while (j < len(vdiff)):
                # test becoming unattractive
                if (vdiff[j] < 0):
                    val = abs(vdiff[j])
                    
                    if (val > c2 * stdev):
                        i = j
                        e = j - 1
                        break
                
                j = j + 1
                
                if (j == len(vdiff)):
                    # reached the end
                    i = j
                    e = j
                
            if (e > s):
                regions.append(s)
                regions.append(e)
#                 print '(%d, %d)' % (s, e)
                #             result[s:e] = np.add(v[s:e,0],0.3) # margin (0.3) is temporary - for visualization
                result[s:e] = 1
            
        i = i + 1
    
    # trace-back (EWMA correction)
    regions, result = ema_traceback(vabs, regions, result)
    
    ## Filter phase
    
    # merge weak spaces
    filtered_regions = []
    for i in range(2, len(regions), 2):
        prev_region_max = max(vabs[regions[i-2]:regions[i-1]])
        space_min = min(vabs[regions[i-1]:regions[i]])
        
        if ( (prev_region_max - space_min)/float(prev_region_max) < mag_c ):
            result[regions[i-1]:regions[i]] = 1
            filtered_regions.append(regions[i])
            filtered_regions.append(regions[i-1])
    for i in range(len(filtered_regions)):
        regions.remove(filtered_regions[i])
    
    # filter out insignificant regions
    filtered_regions = []
    for i in range(0, len(regions), 2):
        sval = vabs[regions[i]]
        region_max = max(vabs[regions[i]:regions[i+1]])
        if ( (region_max - sval)/float(region_max) < mag_c ):
            result[regions[i]:regions[i+1]] = 0
            filtered_regions.append(regions[i])
            filtered_regions.append(regions[i-1])
    for i in range(len(filtered_regions)):
        regions.remove(filtered_regions[i])
    
    # trace-back (EWMA correction)
    regions, result = ema_traceback(vabs, regions, result)
    
    return result, regions

    
def update_period_distribution(period_dist, regions):
    for i in range(0, len(regions), 2):
        region_size = regions[i+1] - regions[i]

        period_dist.append(region_size)
    
    return period_dist
        
        
def update_daily_distribution(attr_dist, regions):
    for i in range(0, len(regions), 2):
        for j in range(regions[i], regions[i+1]): # todo: check if need -1 offset
            attr_dist[j] = attr_dist[j] + 1
    
    return attr_dist
    

def update_daily_in_degree(daily_in_degree, regions, ind_values):
    for i in range(0, len(regions), 2):
        for j in range(regions[i], regions[i+1]): # todo: check if need -1 offset
            daily_in_degree[j] = daily_in_degree[j] + ind_values[j][0]
    
    return daily_in_degree

'''
def plot_distribution(attr_dist):
    n = max(attr_dist.keys())
    
    dist = []
    for i in range(1,n):
        if (i in attr_dist):
            dist.append(attr_dist[i])
        else:
            dist.append(0)
    
    pylab.bar(range(0,len(dist)),dist)
#     pylab.show()
#     output_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_attractiveness_dist'
#     pylab.savefig(output_filename + '.pdf')
    plot_values(range(len(dist)), dist, 'Attractiveness period', 'Size', 'attractiveness_dist', 'bar')
    vis.write_results_using_str(dist, 'attractiveness_dist_list')
#     plot_values(np.log(range(len(dist))), np.log(dist), 'Attractiveness period', 'Size', 'attractiveness_loglog_dist', 'bar')
    print 'Okay'
'''
 
    
# TODO: move to Utils if relevant
def ema(s, n):
    """
    returns an n period exponential moving average for
    the time series s

    s is a list ordered from oldest (index 0) to most
    recent (index -1)
    n is an integer

    returns a numeric array of the exponential
    moving average
    """
    s = np.array(s)
    ema = []
    j = 1

    #get n sma first and calculate the next n period ema
    sma = sum(s[:n]) / n
    multiplier = 2 / float(1 + n)
    ema.append(sma)

    #EMA(current) = ( (Price(current) - EMA(prev) ) x Multiplier) + EMA(prev)
    ema.append(( (s[n] - sma) * multiplier) + sma)

    #now calculate the rest of the values
    for i in s[n+1:]:
        tmp = ( (i - ema[j]) * multiplier) + ema[j]
        j = j + 1
        ema.append(tmp)

    return np.concatenate((np.zeros(n-1), ema))

# trace-back (EWMA correction)
def ema_traceback(vabs, regions, result):
    for i in range(0, len(regions), 2):
        st_idx = 0 # previous region's end or 0 if first
        end_idx = regions[i+1]
        if (i > 0):
            st_idx = regions[i-1] + 1
        
        # find global min/max idx for this region
        vabs_sub = vabs[st_idx:end_idx]
        region_max = (np.where(vabs_sub==max(vabs_sub)))[0][0]
#         vabs_sub_max = vabs_sub[:region_max]
#         region_min = (np.where(vabs_sub_max==min(x for x in vabs_sub_max if x > 0) ))[0][0]
#         vabs_sub_min = vabs_sub[region_min:]
#         region_max = (np.where(vabs_sub_min==max(vabs_sub_min)))[0][0]

        # re-init as 0, then correct
#         min_offset = st_idx+region_min
        min_offset = regions[i] # TODO: improve this - setting region mean as start point to prevent traceback for the left edge
#         max_offset = st_idx+region_min+region_max+1
        max_offset = st_idx+region_max+1
        if (min_offset < max_offset): # Sanity check. Could be improved
            result[st_idx:end_idx] = 0
            result[min_offset:max_offset] = 1
            regions[i] = min_offset
            regions[i+1] = max_offset
    
    return regions, result
        

def ema2(s, n):
    """
    returns an n period exponential moving average for
    the time series s

    s is a list ordered from oldest (index 0) to most
    recent (index -1)
    n is an integer

    returns a numeric array of the exponential
    moving average
    """
    s = np.array(s)
    ema = []
    j = n #     j = 1

    #get n sma first and calculate the next n period ema
    # NOTE - GUY: pad all first elements with the sma
    for i in range(n):
        sma = sum(s[:i+1]) / (i+1)
        ema.append(sma)
    
#     sma = sum(s[:n]) / n
#     ema.append(sma)
    multiplier = 2 / float(1 + n)

    #EMA(current) = ( (Price(current) - EMA(prev) ) x Multiplier) + EMA(prev)
    sma = sum(s[:n]) / n
    ema.append(( (s[n] - sma) * multiplier) + sma)
    
    #now calculate the rest of the values
    for i in s[n+1:]:
        tmp = ( (i - ema[j]) * multiplier) + ema[j]
        j = j + 1
        ema.append(tmp)

    return ema

'''
def plot_popularity(top_nodes):

    print 'Plotting...'    
    for v in top_nodes:
        print v
        
        # NOTE: Guy - extract_popularity_array take the the dict popularity and key (node) v,
        # and extracts the popularity (in_degree).
        ind_popularity = extract_popularity_array(v)
        plot_values(range(len(ind_popularity)), ind_popularity, 'Day', 'Number of mirroring traders', 'popularity_' + str(v))
        

def plot_performance(top_nodes):

    print 'Plotting...'    
    for v in top_nodes:        
        print v

        ind_performance = extract_performance_array(v)
        ind_performance = aggregate_performance(ind_performance)
        
        plot_values(range(len(ind_performance)), ind_performance, 'Day', 'Performance', 'performance_' + str(v))


def plot_pop_and_per(top_nodes):

    print 'Plotting...'
    for v in top_nodes:     
        print v
        
        ind_popularity = extract_popularity_array(v)

        ind_performance = extract_performance_array(v)
        ind_performance = aggregate_performance(ind_performance)

        plot_two_values(range(len(ind_popularity)), ind_popularity, ind_performance, 'Day', 'Number of followers', 'performance', 'pop_and_per_' + str(v))
'''

def extract_attractiveness_array(v):
    v = str(v)
    
    result = []
        
    time = start
    while time<end:
        pop = load_daily_popularity.get_popularity(v, time)
        result.append([
            pop[0] if pop!=None else 0,
            pop[2] if pop!=None else 0
        ]) 
        
        time = time + timedelta(days=1)
    
    
    return result


def get_times():

    times = []
    
    time = start
    while time<end:
        time_str = datetime.strftime(time, constants.GENERAL_DATE_FORMAT) 

        times.append(time_str)
            
        time = time + timedelta(days=1)
    
    return times


'''
def extract_popularity_array(popularity, v):
    v = str(v)
    
    result = []
        
    time = start
    while time<end:
        if time.weekday()!=5 and time.weekday()!=6:
            pop = load_daily_popularity.get_popularity(v, time)
            result.append(pop[0] if pop!=None else 0)
        
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
    '''

'''
def plot_values(X, Y, xlabel, ylabel, suffix, ptype='plot'):
    output_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + suffix

    
    pylab.figure(figsize=(8, 7))

    pylab.rcParams.update({'font.size': 20})

    if (ptype == 'bar'):
        pylab.bar(X, Y)
    else:
        pylab.plot(X, Y)
    
    pylab.axis(vis.get_bounds(X, Y, False, False))

    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)   

    pylab.tight_layout()

    pylab.savefig(output_filename + '.pdf')
'''
    

'''

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
'''

'''
def plot_mul_values(X, Y, xlabel, Ylabel, suffix):
    output_filename = constants.ATTRACTIVENESS_FOLDER_NAME + constants.DATASET + '_' + suffix

    pylab.figure(figsize=(15, 7))

    pylab.rcParams.update({'font.size': 20})

    pylab.xlabel(xlabel)
    
    Y1 = Y[:,0]
    y1label = Ylabel[0]
    ax1 = pylab.gca()
    ax1.plot(X, Y1, 'b')
    ax1.plot(X, [0.0 for x in X], 'b--')
    ax1.set_ylabel(y1label, color='b')   
    for tl in ax1.get_yticklabels():
        tl.set_color('b')
    
    m = np.size(Y,1)
    for i in range(1, m):
        Yi = Y[:,i]
        yilabel = Ylabel[i]
        ax2 = pylab.twinx()
        ax2.plot(X, Yi, 'r')
        ax2.plot(X, [0.0 for x in X], 'r--')
        ax2.set_ylabel(yilabel, color='r')
        pylab.ylim( (0, 1.02) )   
        for tl in ax2.get_yticklabels():
            tl.set_color('r')

    pylab.savefig(output_filename + '.pdf')
'''
 
#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
