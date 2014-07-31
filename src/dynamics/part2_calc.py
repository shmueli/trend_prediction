import sys
sys.path.insert(0, '../')

from datetime import datetime, timedelta
import sets

from graphs import load_graphs
import helpers.constants as constants
from utils import visualize

import gc


start = datetime.strptime('20110630000000', constants.GENERAL_DATE_FORMAT)
end = datetime.strptime('20130701000000', constants.GENERAL_DATE_FORMAT)


def execute():
    print gc.isenabled()
    
    calc_shifts()


def calc_shifts():
    times = []
    
    all_number_nodes = []
    all_removed_edges = []
    all_added_edges = []
    all_inter_edges = []
    all_overall_edges = []
    all_removed_nodes = []
    all_added_nodes = []
    all_diff_removed_edges = []
    all_diff_added_edges = []
    all_inter_removed_edges = []
    all_inter_added_edges = []
    
    all_individual_removed_edges = {}
    all_individual_added_edges = {}
    all_individual_overall_edges = {}

    all_prev_g_nodes = []
    all_g_nodes = []
    all_prev_g_edges = []
    all_g_edges = []
    all_union_edges = []

    all_degrees = []
    removed_degrees = []
    added_degrees = []
    removed_neighbors_degrees = []
    added_neighbors_degrees = []


    '''
    all_nodes = load_graphs.load_period_network(all_times[0], len(all_times), all_times)
    all_nodes = all_nodes.nodes()
    print 'all_nodes:', len(all_nodes)
    '''
    

    prev_g = None
    time = start
    while time<end:
        time_str = datetime.strftime(time, constants.GENERAL_DATE_FORMAT)
        
        g = load_graphs.load_time_network(time)

        if prev_g != None:
            ##################################
            ### calculating absolute change
            ##################################
 
            prev_g_nodes = sets.Set(prev_g.nodes())
            g_nodes = sets.Set(g.nodes())
            prev_g_edges = sets.Set(prev_g.edges())
            g_edges = sets.Set(g.edges())
             
            number_nodes = prev_g_nodes
            removed_edges = prev_g_edges.difference(g_edges)
            added_edges = g_edges.difference(prev_g_edges)
            inter_edges = prev_g_edges.intersection(g_edges)
            union_edges = prev_g_edges.union(g_edges)
            removed_nodes = prev_g_nodes.difference(g_nodes)
            added_nodes = g_nodes.difference(prev_g_nodes)
            diff_removed_edges = sets.Set( prev_g.edges(removed_nodes) )
            diff_added_edges = sets.Set( g.edges(added_nodes) )
 
            inter_nodes = prev_g_nodes.intersection(g_nodes)
            prev_g_common = (prev_g.subgraph(inter_nodes))
            g_common = (g.subgraph(inter_nodes))
            prev_g_common_edges = sets.Set(prev_g_common.edges())
            g_common_edges = sets.Set(g_common.edges())
            inter_removed_edges = prev_g_common_edges.difference(g_common_edges)
            inter_added_edges = g_common_edges.difference(prev_g_common_edges)
             
            number_nodes = len(number_nodes)
            removed_edges = len(removed_edges)
            added_edges = len(added_edges)
            inter_edges = len(inter_edges)
            union_edges = len(union_edges)
            removed_nodes = len(removed_nodes)
            added_nodes = len(added_nodes)
            diff_removed_edges = len(diff_removed_edges)
            diff_added_edges = len(diff_added_edges)
            inter_removed_edges = len(inter_removed_edges)
            inter_added_edges = len(inter_added_edges)
             
 
            ##################################
            ### appending the change
            ##################################
 
            times.append(time_str)
 
            all_number_nodes.append(number_nodes)
            all_removed_edges.append(removed_edges)
            all_added_edges.append(added_edges)
            all_inter_edges.append(inter_edges)
            all_overall_edges.append(removed_edges + added_edges)
            all_removed_nodes.append(removed_nodes)
            all_added_nodes.append(added_nodes)
            all_diff_removed_edges.append(diff_removed_edges)
            all_diff_added_edges.append(diff_added_edges)
            all_inter_removed_edges.append(inter_removed_edges)
            all_inter_added_edges.append(inter_added_edges)
 
 
            all_prev_g_nodes.append(len(prev_g_nodes))
            all_g_nodes.append(len(g_nodes))
            all_prev_g_edges.append(len(prev_g_edges))
            all_g_edges.append(len(g_edges))
            all_union_edges.append(union_edges)
 
            '''
            ##################################
            ### handling individuals
            ##################################
            for v in all_nodes:
                prev_v_edges = sets.Set(prev_g.edges(v) if v in prev_g_nodes else [])
                v_edges = sets.Set(g.edges(v) if v in g_nodes else [])
                union_edges = prev_v_edges.union(v_edges)
                v_removed_edges = prev_v_edges.difference(v_edges)
                v_added_edges = v_edges.difference(prev_v_edges)
                 
                if len(union_edges)==0:
                    continue
                 
                v_removed_edges = float(len(v_removed_edges))
                v_added_edges = float(len(v_added_edges))
                v_overall_edges = v_removed_edges + v_added_edges
                 
                if v not in all_individual_removed_edges:
                    all_individual_removed_edges[v] = []
                all_individual_removed_edges[v].append(v_removed_edges)                
                if v not in all_individual_added_edges:
                    all_individual_added_edges[v] = []
                all_individual_added_edges[v].append(v_added_edges)
                if v not in all_individual_overall_edges:
                    all_individual_overall_edges[v] = []
                all_individual_overall_edges[v].append(v_overall_edges)
            '''
             
            '''
            ##################################
            ### degrees distributions 
            ##################################
            ds = [float(prev_g.degree(v))/float(len(prev_g_nodes)) for v in prev_g_nodes]
            all_degrees.extend(ds)
             
            ds = [float(prev_g.degree(v))/float(len(prev_g_nodes)) for v in prev_g_nodes.difference(g_nodes)]
            removed_degrees.extend(ds)
             
            ds = [float(g.degree(v))/float(len(g_nodes)) for v in g_nodes.difference(prev_g_nodes)]
            added_degrees.extend(ds)
 
            for v in prev_g_nodes.difference(g_nodes):
                ds = [float(prev_g.degree(u))/float(len(prev_g_nodes)) for u in prev_g.neighbors(v)]
                removed_neighbors_degrees.extend(ds)
 
            for v in g_nodes.difference(prev_g_nodes):
                ds = [float(g.degree(u))/float(len(g_nodes)) for u in g.neighbors(v)]
                added_neighbors_degrees.extend(ds)
            '''
            
        prev_g = g
        
        gc.collect()

        time = time + timedelta(days=1)


    '''
    temp = all_individual_removed_edges
    all_individual_removed_edges = []
    for v in temp:
        all_individual_removed_edges.extend(temp[v])
    temp = all_individual_added_edges
    all_individual_added_edges = []
    for v in temp:
        all_individual_added_edges.extend(temp[v])
    temp = all_individual_overall_edges
    all_individual_overall_edges = []
    for v in temp:
        all_individual_overall_edges.extend(temp[v])
    ''' 


    visualize.write_results(times, 'times')

    visualize.write_results(all_removed_edges, 'removed_edges')
    visualize.write_results(all_added_edges, 'added_edges')
    visualize.write_results(all_inter_edges, 'inter_edges')
    visualize.write_results(all_overall_edges, 'overall_edges')

    visualize.write_results(all_removed_nodes, 'removed_nodes')
    visualize.write_results(all_added_nodes, 'added_nodes')
    visualize.write_results(all_diff_removed_edges, 'diff_removed_edges')
    visualize.write_results(all_diff_added_edges, 'diff_added_edges')
    visualize.write_results(all_inter_removed_edges, 'inter_removed_edges')
    visualize.write_results(all_inter_added_edges, 'inter_added_edges')

    visualize.write_results(all_individual_removed_edges, 'individual_removed_edges')
    visualize.write_results(all_individual_added_edges, 'individual_added_edges')
    visualize.write_results(all_individual_overall_edges, 'individual_overall_edges')

    visualize.write_results(all_prev_g_nodes, 'prev_g_nodes')
    visualize.write_results(all_g_nodes, 'g_nodes')
    visualize.write_results(all_prev_g_edges, 'prev_g_edges')
    visualize.write_results(all_g_edges, 'g_edges')
    visualize.write_results(all_union_edges, 'union_edges')
    
    visualize.write_results(all_degrees, 'all_degrees')
    visualize.write_results(removed_degrees, 'removed_degrees')
    visualize.write_results(added_degrees, 'added_degrees')
    visualize.write_results(removed_neighbors_degrees, 'removed_neighbors_degrees')
    visualize.write_results(added_neighbors_degrees, 'added_neighbors_degrees')


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
