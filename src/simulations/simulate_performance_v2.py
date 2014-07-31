from datetime import datetime, timedelta
import pylab
import random
import sets

from helpers import constants
import networkx as nx
from utils import draw_powerlaw, visualize


output_folder = constants.MIRROR_FOLDER_NAME


def simulate():
    g = nx.DiGraph()
    #g = nx.erdos_renyi_graph(10, 0.1, 0, True)

    winning_period = {}
    loosing_period = {}

    winners = sets.Set()
    loosers = sets.Set()
    marked = sets.Set()

    node_id = 0

    start = constants.PERIODS[1]['start']
    end = constants.PERIODS[4]['end']

    times = []
    data = []
    
    
    #simulate
    time = start
    while time<end:
        print time

        #updating winners
        for v in g.node:            
            #if v in marked:
            #    continue
            
            if v in winners or v in loosers:
                continue
            
            winning = draw_is_winning()

            if winning:
                winning_time = draw_winning_time()
                
                winning_period[v] = [time, time+timedelta(days=winning_time)]

                winners.add(v)
                
                marked.add(v)


        existing_nodes = g.nodes()


        #adding nodes
        added_nodes = []
        nAddedNodes = draw_added_nodes(len(existing_nodes))
        for a in range(nAddedNodes):
            v = node_id
            node_id = node_id + 1
            
            g.add_node(v)
            added_nodes.append(v)
        




        all_nodes = g.nodes()
        
        if len(winners) > 0:
            pref_nodes_array = calc_pref_nodes_array(g, winners)
            
            #adding edges for existing nodes
            nAddedEdges = draw_added_edges_for_existing_nodes(len(winners))
            for e in range(nAddedEdges):
                v = selectPreferredNode(pref_nodes_array)
                
                r = random.randint(0, len(all_nodes)-1)
                            
                u = all_nodes[r]
                
                g.add_edge(u, v)



        '''
        if len(winners) > 0:
            pref_nodes_array = calc_pref_nodes_array(g, winners)
            
            #adding edges for existing nodes
            nAddedEdges = draw_added_edges_for_existing_nodes(len(winners))
            for e in range(nAddedEdges):
                v = selectPreferredNode(pref_nodes_array)
                
                r = random.randint(0, len(existing_nodes)-1)
                            
                u = existing_nodes[r]
                
                g.add_edge(u, v)
                
    
            #adding edges for new nodes
            for u in added_nodes:
                nAddedEdges = draw_added_edges_per_new_node()
                
                for e in range(nAddedEdges):
                    v = selectPreferredNode(pref_nodes_array)
    
                    g.add_edge(u, v)
        '''


        #removing edges for existing nodes
        pref_nodes_array = calc_pref_nodes_array(g, loosers)
        
        nRemovedEdges = draw_removed_edges_for_existing_nodes(len(loosers))
        for e in range(nRemovedEdges):
            if len(loosers) == 0:
                continue    

            v = selectPreferredNode(pref_nodes_array)
            
            #the calc_pref_nodes_array is kept un updated for efficiency reasons
            #if v not in loosers:
            #    continue
            
            if g.in_degree(v)==0:
                continue
            
            inEdges = list(g.in_edges(v))
            
            r = random.randint(0, len(inEdges)-1)
            
            u = inEdges[r][0]
            
            g.remove_edge(u, v)
            
            '''
            if g.in_degree(v) == 0:
                loosers.remove(v)
            '''
           

        '''        
        #remove nodes without links        
        for v in existing_nodes:
            if g.degree(v)==0:
                if v not in winners:
                    g.remove_node(v)
                    
                    if v in loosers:
                        loosers.remove(v)
        '''
                 
        pWinners = float(len(winners))/float(g.number_of_nodes())
        pLoosers = float(len(loosers))/float(g.number_of_nodes())

        
        #update winners and loosers   
        curr_winners = list(winners)
        for v in curr_winners:
            [open, close] = winning_period[v]
            
            if close==time:
                winners.remove(v)

                loosing_period[v] = [time+timedelta(days=1), time+timedelta(days=1)+(close-open)]

                loosers.add(v)

        curr_loosers = list(loosers)
        for v in curr_loosers:
            [open, close] = loosing_period[v]
            
            if close==time:
                loosers.remove(v)
  

        data.append(pWinners)
        times.append(time)

        print len(winners), len(loosers)
        print g.number_of_nodes(), g.number_of_edges()
        store_network(time, g)
            
        time = time + timedelta(days=1)

    #'''
    #data = [g.in_degree(v) for v in g.node]
    #data.sort(reverse=True)
    pylab.hist(data)
    pylab.show()
    visualize.plot_changes(times, data, 'winners', False)
    #'''
        

def store_network(time, g):
    output_file_name = output_folder + time.strftime(constants.GENERAL_DATE_FORMAT)
    
    output_file = open(output_file_name, 'w')
    
    for e in g.edges():
        line = str(e[0]) + ',' + str(e[1])
        
        output_file.write(line + '\n')
    
    output_file.close()    
        
    
    
    
def draw_is_winning():
    p = 0.1
    r = random.random()
    return r<p


def draw_winning_time():
    '''
    p = draw_powerlaw.draw_powerlaw(3, 100, 1, 100)
    n = int(p)
    
    return n
    '''
    return 5


def draw_added_nodes(curr_num_nodes):
    '''
    p = draw_powerlaw.draw_powerlaw(3, 100, 0, 1)
    n = int( p * float(curr_num_nodes) )
    
    return n
    '''
    return 5


def draw_added_edges_per_new_node():
    #return 5
    return 0


def draw_added_edges_for_existing_nodes(num_winners):
    #return 5*num_winners
    return 0


def draw_removed_edges_for_existing_nodes(num_loosers):
    #return 4*num_loosers
    return 0


def calc_pref_nodes_array(g, nodes):
    pref_nodes = []
    for v in nodes:
        d = g.degree(v)
        for i in range(d+1):
            pref_nodes.append(v)

    return pref_nodes


def selectPreferredNode(pref_nodes_array): 
    r = random.randint(0, len(pref_nodes_array)-1)
    
    return pref_nodes_array[r]


if __name__ == '__main__':
    simulate()
     
    print 'Done.'

