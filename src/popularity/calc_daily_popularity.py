from datetime import datetime, timedelta
import sets
import json

from graphs import load_graphs
import helpers.constants as constants


periods = {
    1: {'start': datetime.strptime('20110701000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20120101000000', '%Y%m%d%H%M%S')},
    2: {'start': datetime.strptime('20120101000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20120701000000', '%Y%m%d%H%M%S')},
    3: {'start': datetime.strptime('20120701000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20130101000000', '%Y%m%d%H%M%S')},
    4: {'start': datetime.strptime('20130101000000', '%Y%m%d%H%M%S'), 'end': datetime.strptime('20130701000000', '%Y%m%d%H%M%S')}
}

shift = timedelta(seconds=int(150*60))


def execute():
    for p in periods:
        store_daily_popularity_for_all_individuals(periods[p]['start'], periods[p]['end'], p)


def store_daily_popularity_for_all_individuals(start, end, period):
    output_filename = 'X:/workspace/trend_prediction_out/etoro/daily_period/popularity/daily_popularity' + '_' + str(period)

    popularity = {}

    start = start - timedelta(days=1)        
    
    g_prev = None
    time = start
    while time<end:
        time_str = datetime.strftime(time, constants.GENERAL_DATE_FORMAT) 
        
        g = load_graphs.load_time_network(time)

        if g_prev!=None:
            
            all_vs = sets.Set()
            all_vs.union_update(g.node)     
            all_vs.union_update(g_prev.node)     

            for v in all_vs:
                pop = calc_popularity_for_individual(g, g_prev, v)
                
                if v not in popularity:
                    popularity[v] = {}
                popularity[v][time_str] = pop
                        
        g_prev = g
             
        time = time + timedelta(days=1)

    json.dump(popularity, open(output_filename, 'w'))


def calc_popularity_for_individual(g, g_prev, v):

    in_degree = g.in_degree(v) if g.has_node(v) else 0
    out_degree = g.out_degree(v) if g.has_node(v) else 0
    prev_in_degree = g_prev.in_degree(v) if g_prev.has_node(v) else 0
    prev_out_degree = g_prev.out_degree(v) if g_prev.has_node(v) else 0
    diff_in = in_degree - prev_in_degree
    diff_out = out_degree - prev_out_degree

    in_nodes_ = in_nodes(g, v)
    prev_in_nodes_ = in_nodes(g_prev, v)
    added_in_nodes = in_nodes_.difference(prev_in_nodes_)
    removed_in_nodes = prev_in_nodes_.difference(in_nodes_)

    out_nodes_ = out_nodes(g, v)
    prev_out_nodes_ = out_nodes(g_prev, v)
    added_out_nodes = out_nodes_.difference(prev_out_nodes_)
    removed_out_nodes = prev_out_nodes_.difference(out_nodes_)
                    
    return [
        in_degree,
        prev_in_degree,
        diff_in,
        len(added_in_nodes),
        len(removed_in_nodes),

        out_degree,
        prev_out_degree,
        diff_out,
        len(added_out_nodes),
        len(removed_out_nodes)
    ] 


def in_nodes(g, v):
    nodes = sets.Set()
    if g.has_node(v):
        for e in g.in_edges(v):
            nodes.add(e[0])
    return nodes


def out_nodes(g, v):
    nodes = sets.Set()
    if g.has_node(v):
        for e in g.out_edges(v):
            nodes.add(e[1])
    return nodes
        

def tomorrow(time):
    tomorrow = datetime(time.year, time.month, time.day) + timedelta(days=1)
    return tomorrow


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
