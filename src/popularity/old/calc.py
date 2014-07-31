from datetime import datetime, timedelta
from graphs import load_graphs
from utils import visualize
from helpers import constants


def execute():
    start = datetime.strptime(constants.START_DATE, constants.GENERAL_DATE_FORMAT)
    end = datetime.strptime(constants.END_DATE, constants.GENERAL_DATE_FORMAT)
    #calc_pop_and_per(start, end, 100)
    calc_pop(start, end, 100)
    

def calc_pop(start, end, num_nodes):
    top_nodes = load_graphs.load_period_network(start, end)
    top_nodes = load_graphs.rank_network_nodes(top_nodes)
    top_nodes = top_nodes[-num_nodes:]
    print 'top_nodes:', len(top_nodes)

    #top_nodes = ['1927218']
    
    num_nodes = []
    
    popularity = []
    for i in range(len(top_nodes)):
        popularity.append([])

    time =start
    while time<end:
        g_edges = load_graphs.load_time_network(time, data=False)
    
        for v_index in range(len(top_nodes)):
            v = top_nodes[v_index]
            
            v_popularity = calc_node_popularity(g_edges, v)
            popularity[v_index].append(v_popularity)   
            
        time = time + timedelta(days=1)



    visualize.write_results_using_str(num_nodes, 'num_nodes')

    visualize.write_results_using_str(top_nodes, 'top_nodes')

    for v_index in range(len(top_nodes)):
        visualize.write_results_using_str(popularity[v_index], 'popularity_' + str(top_nodes[v_index]))


def calc_pop_and_per(start, end, num_nodes):
    top_nodes = load_graphs.load_period_network(start, end)
    top_nodes = load_graphs.rank_network_nodes(top_nodes)
    top_nodes = top_nodes[-num_nodes:]
    print 'top_nodes:', len(top_nodes)

    #top_nodes = ['1927218']
    
    num_nodes = []
    
    popularity = []
    performance = []
    for i in range(len(top_nodes)):
        popularity.append([])
        performance.append([])

    time =start
    while time<end:
        g_edges = load_graphs.load_time_network(time, data=False, filterQ={'ParentGCID': {'$in' : top_nodes}})
        g_trades = load_graphs.load_time_network(time, data=True, filterQ={'GCID': {'$in' : top_nodes}})
    
        for v_index in range(len(top_nodes)):
            v = top_nodes[v_index]
            
            v_popularity = calc_node_popularity(g_edges, v)
            popularity[v_index].append(v_popularity)   

            v_performance = calc_node_performance(g_trades, v)
            performance[v_index].append(v_performance)   
            
    time = time + timedelta(days=1)



    visualize.write_results(num_nodes, 'num_nodes')

    visualize.write_results(top_nodes, 'top_nodes')

    for v_index in range(len(top_nodes)):
        visualize.write_results(popularity[v_index], 'popularity_' + str(top_nodes[v_index]))
        visualize.write_results(performance[v_index], 'performance_' + str(top_nodes[v_index]))


def calc_node_popularity(g, v):
    popularity = g.in_degree(v) if g.has_node(v) else 0
            
    return popularity
    

def calc_node_performance(g, v):
    performance = []
    if g.has_node(v):
        for e in g.out_edges(v, data=True):
            data = e[2]['data']
            performance.extend(data)

    return performance


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
