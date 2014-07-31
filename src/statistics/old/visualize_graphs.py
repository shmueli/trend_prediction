import helpers.constants as constants
from utils import visualize
import numpy
from datetime import datetime
from graphs import times
from graphs import load_graphs

def execute():
    all_times = times.get_times()

    plot_shifts(all_times)


def plot_shifts(all_times):
    nodes = []
    edges = []
    numpos = []
    lenpos = []
    
    prev_g = None
    for i in range(len(all_times)):
        time = all_times[i]
        
        #'''
        dt = datetime.strptime(time, constants.GENERAL_DATE_FORMAT)
        if constants.DATASET=='etoro':
            #if dt.weekday()==6 or dt.weekday()==0:
            if dt.weekday()==5 or dt.weekday()==6:
            #if dt.weekday()==6:
                continue
        else:
            #if dt.weekday()==6 or dt.weekday()==0:
            if dt.weekday()==6:
                continue
        #'''

        g = load_graphs.load_time_network(time, data=True)

        if g.number_of_edges() == 0:
            continue
        
        if prev_g != None:
            nodes.append(prev_g.number_of_nodes())
            edges.append(prev_g.number_of_edges())
            
            cntpos = 0
            lengths = []
            for e in prev_g.edges(data=True):
                for pos in e[2]['data']:
                    cntpos = cntpos + 1
                
                    openDT = datetime.strptime(pos[0], constants.GENERAL_DATE_FORMAT)
                    closeDT = datetime.strptime(pos[1], constants.GENERAL_DATE_FORMAT)
                    length = (closeDT - openDT).total_seconds()/60/60/24
                    lengths.append(length)
                
            numpos.append(cntpos)
            lengths = numpy.mean(lengths)
            lenpos.append(lengths)
                 
        prev_g = g


    visualize.plot_values(range(len(nodes)), nodes, 'stats_nodes')
    visualize.plot_values(range(len(edges)), edges, 'stats_edges')
    visualize.plot_values(range(len(numpos)), numpos, 'stats_numpos')
    visualize.plot_values(range(len(lenpos)), lenpos, 'stats_lenpos')


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
