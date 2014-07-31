from datetime import datetime

from helpers import constants
from utils import visualize


def execute():
    plot_all()

    #snapshot_times = ['20120101000000', '20120701000000', '20130101000000']
    #plot_shifts_constant_set(snapshot_times)


def plot_all():
    times = visualize.load_results('times')

    #'''
    #plot_data('removed_edges', times, False)
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
    if prefix!='':
        norm = [1.0 for v in data]
    
    else:
        all_prev_g_nodes = visualize.load_results(prefix + 'prev_g_nodes')
        all_g_nodes = visualize.load_results(prefix + 'g_nodes')
        all_prev_g_edges = visualize.load_results(prefix + 'prev_g_edges')
        all_g_edges = visualize.load_results(prefix + 'g_edges')
        all_inter_edges = visualize.load_results('inter_edges')
        all_union_edges = visualize.load_results('union_edges')
    
        #norm = [1.0 for i in range(len(times))]
        #norm = all_prev_g_nodes
        #norm = all_g_nodes
        #norm = [float(all_prev_g_nodes[i]+all_g_nodes[i])/2.0 for i in range(len(all_prev_g_nodes))]
        #norm = all_prev_g_edges
        #norm = all_g_edges
        #norm = [float(all_prev_g_edges[i]+all_g_edges[i])/2.0 for i in range(len(all_prev_g_edges))]
        #norm = [min(all_prev_g_edges[i], all_g_edges[i]) for i in range(len(all_prev_g_edges))]
        #norm = all_inter_edges
        #norm = all_union_edges
        
        #norm = [np.mean(all_prev_g_edges[:i+1]) for i in range(len(all_prev_g_edges))]
        

        #'''
        norm = None
        
        if constants.DATASET == 'etoro': 
            if varname.find('edges')>=0:
                '''
                if varname.find('removed')>=0:
                    norm = all_g_edges
                elif varname.find('added')>=0:
                    norm = all_prev_g_edges
                '''
                norm = all_prev_g_edges
            elif varname.find('nodes')>=0:
                '''
                if varname.find('removed')>=0:
                    norm = all_g_nodes
                elif varname.find('added')>=0:
                    norm = all_prev_g_nodes
                '''
                norm = all_prev_g_nodes
        else:
            norm = [1.0 for v in all_prev_g_edges]
            
        #'''
        '''
        if varname.find('removed')>=0:
            norm = [np.sqrt(v) for v in all_g_edges]
        elif varname.find('added')>=0:
            norm = [np.sqrt(v) for v in all_prev_g_edges]
        '''
        #norm = [1.0 for v in all_prev_g_edges]
        #norm = all_prev_g_nodes

        '''
        if varname.find('removed')>=0:
            norm = all_g_nodes
        elif varname.find('added')>=0:
            norm = all_prev_g_nodes
        '''
        
        #norm = all_prev_g_nodes
        
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
        data = visualize.load_results(prefix + varname)    
        norm = get_norm(varname, data, prefix)
        data = [float(data[i])/float(norm[i]) for i in range(len(times)) if include_time(varname, times, data, norm, i)]
        filtered_times = [times[i] for i in range(len(times)) if include_time(varname, times, times, norm, i)]

    return filtered_times, data

    
def include_time(varname, times, data, norm, i):
    time = times[i]
    dt = datetime.strptime(time, constants.GENERAL_DATE_FORMAT)

    '''
    if dt.weekday()==5 or dt.weekday()==6 or dt.weekday()==0:
        return False
    '''

    '''
    if dt.weekday()==6:
        return False
    '''

    '''
    if varname.find('removed')>=0:
        if dt.weekday()==6 or dt.weekday()==0:
            return False

    if varname.find('added')>=0:
        if dt.weekday()==5 or dt.weekday()==6:
            return False
    '''

    '''
    if dt.weekday()==6:
        return False
    '''
    

    '''
    if dt.weekday()==0:
        return False
    '''
    
    '''
    if constants.DATASET == 'etoro':
        if i<90:
            return False
    else:
        if i==len(times)-1:
            return False
    '''
    
    '''
    if constants.DATASET == 'etoro':
        start = datetime.strptime('20200701000000', constants.GENERAL_DATE_FORMAT)
        end = datetime.strptime('20220701000000', constants.GENERAL_DATE_FORMAT)

        if dt<start or dt>end:
            return False
        
        #if data[i]==0:
        #    return False
    ''' 
    
    if norm[i]==0:
        return False
    
    return True


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
