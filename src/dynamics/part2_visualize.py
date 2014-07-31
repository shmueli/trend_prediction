import sys
sys.path.insert(0, '../')

from datetime import datetime

from helpers import constants
from utils import visualize


def execute():
    plot_all()


def plot_all():
    times = visualize.load_results('times')

    #'''
    plot_data('removed_edges', times, False)
    plot_data('added_edges', times, False)
    #plot_data('inter_edges', times, norm, False)
    #plot_data('overall_edges', times, False)

    plot_data('removed_nodes', times, False)
    plot_data('added_nodes', times, False)
    plot_data('diff_removed_edges', times, False)
    plot_data('diff_added_edges', times, False)
    
    plot_data('inter_removed_edges', times, False)
    plot_data('inter_added_edges', times, False)


    '''
    plot_data('removed_edges', times, False, xmin=0.0175)
    plot_data('added_edges', times, False, xmin=0.025)
    #plot_data('inter_edges', times, norm, False)
    #plot_data('overall_edges', times, False)

    plot_data('removed_nodes', times, False, xmin=0.015)
    plot_data('added_nodes', times, False, xmin=0.0175)
    plot_data('diff_removed_edges', times, False, xmin=0.00675)
    plot_data('diff_added_edges', times, False, xmin=0.00875)
    
    plot_data('inter_removed_edges', times, False, xmin=0.015)
    plot_data('inter_added_edges', times, False, xmin=0.0175)

    #plot_data('individual_removed_edges', times, False)
    #plot_data('individual_added_edges', times, False)
    #plot_data('individual_overall_edges', times, False)
    '''

    #plot_data('pop_dist', times, norm, True)


def plot_shifts_constant_set(snapshot_times):
    for base_time in snapshot_times:
        print 'base time:', base_time

        times = visualize.load_results(base_time + '_times')
    
        plot_data('removed_edges', times, False, base_time + '_')
        plot_data('added_edges', times, False, base_time + '_')
        plot_data('overall_edges', times, False, base_time + '_')



def get_norm(varname, data, prefix):
    all_prev_g_nodes = visualize.load_results(prefix + 'prev_g_nodes')
    all_prev_g_edges = visualize.load_results(prefix + 'prev_g_edges')

    norm = None
    
    if varname.find('edges')>=0:
        norm = all_prev_g_edges
    elif varname.find('nodes')>=0:
        norm = all_prev_g_nodes
    else:
        norm = [1.0 for v in all_prev_g_edges]
            
    return norm
   

def plot_data(varname, times, onlyBins, prefix='', xmin=None):
    filtered_times, data = prepare_data(varname, times, prefix)

    print data
    
    visualize.plot_changes(filtered_times, data, prefix + varname, onlyBins, xmin=xmin)

    
def prepare_data(varname, times, prefix):
    if varname.find('overall')>=0:
        tempvarname = varname.replace('overall', 'removed')
        filtered_times, removed = prepare_data(tempvarname, times, prefix)

        tempvarname = varname.replace('overall', 'added')
        filtered_times, added = prepare_data(tempvarname, times, prefix)

        data = [removed[i] + added[i] for i in range(len(removed))]
    else:
        data_temp = visualize.load_results(prefix + varname)    
        norm = get_norm(varname, data_temp, prefix)
        data = [float(data_temp[i])/float(norm[i]) for i in range(len(times)) if include_time(varname, times, data_temp, norm, i)]
        filtered_times = [times[i] for i in range(len(times)) if include_time(varname, times, data_temp, norm, i)]

    return filtered_times, data

    
def include_time(varname, times, data, norm, i):
    time = times[i]
    dt = datetime.strptime(time, constants.GENERAL_DATE_FORMAT)

    if norm[i]==0:
        return False

    if constants.DATASET == 'etoro':
        start = datetime.strptime('20110701000000', constants.GENERAL_DATE_FORMAT)
        end = datetime.strptime('20130701000000', constants.GENERAL_DATE_FORMAT)

        if dt<start or dt>end:
            return False
        
        if dt.weekday()==6:
            return False

    if constants.DATASET == 'tweeter':
        print i, len(data), len(norm), len(times)
        if (float(data[i])/float(norm[i]))>2:
            return False

    if constants.DATASET == 'call':
        start = datetime.strptime('20101120000000', constants.GENERAL_DATE_FORMAT)
        end = datetime.strptime('20110301000000', constants.GENERAL_DATE_FORMAT)

        if dt<start or dt>end:
            return False
    
    return True


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
