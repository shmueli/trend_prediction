from datetime import datetime

from helpers import constants
from utils import visualize


def execute():
    times = visualize.load_results('times')

    plot_data('g_edges', times, 'Number of edges', suffix='edges_count')
    plot_data('g_nodes', times, 'Number of nodes', suffix='nodes_count')


def plot_data(varname, times, ylabel, prefix='', suffix=''):
    data = prepare_data(varname, times, prefix)

    X = range(len(data))
    #X = [((365*2)*x/len(data)) for x in X]
    visualize.plot_values(X, data, 'Day', ylabel, suffix)


def prepare_data(varname, times, prefix):
    data = visualize.load_results(prefix + varname)    

    data = [data[i] for i in range(len(times)) if include_time(times, data, i)]

    return data


def include_time(times, data, i):
    time = times[i]
    dt = datetime.strptime(time, constants.GENERAL_DATE_FORMAT)

    
    start = datetime.strptime('20200701000000', constants.GENERAL_DATE_FORMAT)
    end = datetime.strptime('20220701000000', constants.GENERAL_DATE_FORMAT)

    if dt<start or dt>end:
        return False
        
    return True


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
