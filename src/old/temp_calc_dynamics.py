import helpers.constants as constants
import sets
from datetime import datetime
from graphs import load_graphs
from graphs import times
from utils import visualize
import numpy
import random


def execute():
    all_times = times.get_times()
    
    calc_shifts(all_times)

    #snapshot_times = ['20111101000000', '20120301000000', '20120701000000']
    #calc_shifts_constant_set(all_times, snapshot_times, 90)


def calc_shifts(all_times):
    times = []
    
    all_pop_dist = []

    all_nodes = load_graphs.load_period_network(all_times[0], len(all_times), all_times)
    all_nodes = all_nodes.nodes()
    print 'all_nodes:', len(all_nodes)

    samples = []
    for j in range(10000):
        random.shuffle(all_nodes)
        samples.append( all_nodes[:30] )
        
    prev_g_all = None
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

        g_all = load_graphs.load_time_network(time)

        if prev_g_all != None:
            
            for s in samples:
                prev_g = prev_g_all.subgraph(s)
                g = g_all.subgraph(s)

                prev_g_nodes = sets.Set(prev_g.nodes())
                g_nodes = sets.Set(g.nodes())
    
                union_nodes = list(prev_g_nodes.union(g_nodes))
                
                pop_dist = numpy.sqrt(numpy.mean([numpy.square( ( (g.degree(v) if v in g.node else 0) - (prev_g.degree(v) if v in prev_g.node else 0) ) / float(len(union_nodes)) ) for v in union_nodes]))
                #pop_dist = numpy.sqrt(numpy.mean([numpy.square( ( (g.degree(v) if v in g.node else 0) - (prev_g.degree(v) if v in prev_g.node else 0) ) / float(len(all_nodes)) ) for v in union_nodes]))
                
                times.append(time)
    
                all_pop_dist.append(pop_dist)

            
        prev_g_all = g_all

    visualize.write_results(all_pop_dist, 'pop_dist')



#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
