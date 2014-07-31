from datetime import datetime, timedelta
import random
import sets

from graphs import load_graphs
import helpers.constants as constants
from utils import visualize


start = datetime.strptime('20110701000000', constants.GENERAL_DATE_FORMAT)
end = datetime.strptime('20130701000000', constants.GENERAL_DATE_FORMAT)

def execute():
    
    store_samples(start, end)

    samples = load_samples()
    
    calc_shifts(start, end, samples)
    calc_performance(start, end, samples)
    

def store_samples(start, end):
    all_nodes = get_all_nodes(start, end)
    visualize.write_results_using_str(all_nodes, 'sample_all_nodes')

    samples = calc_samples(all_nodes, 10000, 100)
    visualize.write_results_using_str([len(samples)], 'sample_M')
    for m in range(len(samples)):
        visualize.write_results_using_str(samples[m], 'sample_' + str(m))


def load_samples():
    samples = []
    M = visualize.load_results_using_eval('sample_M')[0]
    for m in range(M):
        sample = visualize.load_results_using_eval('sample_' + str(m))
        samples.append(sample)
        
    return samples
        
    
def calc_samples(all_nodes, N, M):
    samples = {}

    for m in range(M):
        samples[m] = sample_nodes(all_nodes, N)
        
    return samples

    
def calc_shifts(start, end, samples):
    all_prev_g_edges = {}
    all_g_edges = {}
    all_added_edges = {}
    all_removed_edges = {}

    for m in range(len(samples)):
        all_prev_g_edges[m] = []
        all_g_edges[m] = []
        all_removed_edges[m] = []
        all_added_edges[m] = []


    prev_g = None
    time = start
    while time<end:
        g = load_graphs.load_time_network(time)

        if len(g.edges())==0:
            print '### ', time
            continue

        if prev_g != None:

            for m in range(len(samples)):
                sample = samples[m]
                
                prev_g_m = prev_g.subgraph(sample)
                g_m = g.subgraph(sample)

                ##################################
                ### calculating absolute change
                ##################################
    
                prev_g_edges = sets.Set(prev_g_m.edges())
                g_edges = sets.Set(g_m.edges())
                removed_edges = prev_g_edges.difference(g_edges)
                added_edges = g_edges.difference(prev_g_edges)
             
                prev_g_edges = len(prev_g_edges)
                g_edges = len(g_edges)
                removed_edges = len(removed_edges)
                added_edges = len(added_edges)
                
    
                ##################################
                ### appending the change
                ##################################
    
                all_prev_g_edges[m].append(prev_g_edges)
                all_g_edges[m].append(g_edges)
                all_removed_edges[m].append(removed_edges)
                all_added_edges[m].append(added_edges)
                                  
        prev_g = g

        time = time + timedelta(days=1)


    for m in range(len(samples)):
        visualize.write_results(all_prev_g_edges[m], 'sample_prev_g_edges_' + str(m))
        visualize.write_results(all_g_edges[m], 'sample_g_edges_' + str(m))
        visualize.write_results(all_removed_edges[m], 'sample_removed_edges_' + str(m))
        visualize.write_results(all_added_edges[m], 'sample_added_edges_' + str(m))


def calc_performance(all_times, samples):
    #recode this part...
    profit = []
    invested = []
    performance = []
    for m in range(len(samples)):
        profit.append(0.0)
        invested.append(0.0)
        performance.append(0.0)

    prev_g = None
    for i in range(len(all_times)):
        time = all_times[i]
        
        g = load_graphs.load_time_network(time, data=True)

        if len(g.edges())==0:
            print '### ', time
            continue

        if prev_g != None:

            for m in range(len(samples)):
                sample = samples[m]
                
                g_m = g.subgraph(sample)
                
                for e in g_m.out_edges(data=True):
                    data = e[2]['data']
                    for p in data:
                        closeDT = p[1]
                        netProfit = float(p[3])
                        dollarsAmount = float(p[4])

                        if closeDT[0:8]==time[0:8]:
                            profit[m] = profit[m] + netProfit
                            
                        invested[m] = invested[m] + dollarsAmount
          
        prev_g = g
        
        
    for m in range(len(samples)):
        invested[m] = invested[m]/float(len(all_times))
        
        performance[m] = profit[m]/invested[m]
        
            
    for m in range(len(samples)):
        visualize.write_results([performance[m]], 'sample_performance_' + str(m))


def get_all_nodes(start, end):
    all_nodes = load_graphs.load_period_network(start, end)
    all_nodes = list(all_nodes.nodes())
    return all_nodes


def sample_nodes(all_nodes, n):
    random.shuffle(all_nodes)
    return all_nodes[-n:]
        


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
