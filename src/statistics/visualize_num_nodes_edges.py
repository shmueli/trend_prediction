from datetime import datetime

from dynamics import load_dynamics
from helpers import constants
from utils import visualize


start = constants.PERIODS[1]['start']
end = constants.PERIODS[4]['end']


def execute():
    times = load_dynamics.load('times')

    plot_data('g_edges', times, 'Number of edges', suffix='edges_count')
    plot_data('g_nodes', times, 'Number of nodes', suffix='nodes_count')


def plot_data(varname, times, ylabel, prefix='', suffix=''):
    output_filename = constants.STATS_FOLDER_NAME + suffix
    
    data = prepare_data(varname, times, prefix)

    X = range(len(data))

    visualize.plot_values(X, data, 'Day', ylabel, output_filename)


def prepare_data(varname, times, prefix):
    data = load_dynamics.load(varname)    

    data = [data[i] for i in range(len(times)) if include_time(times, data, i)]

    return data


def include_time(times, data, i):
    time = times[i]
    dt = datetime.strptime(time, constants.GENERAL_DATE_FORMAT)

    if dt<start or dt>end:
        return False
        
    return True


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
    