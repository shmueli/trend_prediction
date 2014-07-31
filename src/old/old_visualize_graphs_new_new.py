import helpers.constants as constants
import os
import networkx as nx
import pylab
import sets
import numpy
import math
from datetime import datetime
import powerlaw
# import plfit
# import plplot
# import plfit2
# import plpva


def execute():
    all_times = get_times()

    #'''
    for threshold in [-1]:
        all_top_nodes = get_top_nodes(all_times, threshold)
        print '####', len(all_top_nodes)
        
        plot_shifts(all_times, all_top_nodes, 'top' + str(threshold))
    #'''

    '''
    if constants.DATASET=='etoro':
        times = ['20120101000000', '20120401000000', '20120701000000']
        plot_snapshot_evolution(times, 30, all_times, 50)
        plot_snapshot_degrees(times, 30, all_times)
        plot_whole_network_degrees(all_times)
    '''



#####################################################################################
### part 1
#####################################################################################

def plot_shifts(times, nodes, suffix):
    '''
    nodes_popularity = {}
    network_shifts_by_individuals = []
    '''

    '''
    int_added_edges = []
    int_removed_edges = []
    int_overall_edges = []
    int_number_edges = []
    int_number_nodes = []

    diff_added_edges = []
    diff_removed_edges = []
    diff_overall_edges = []
    diff_number_edges = []
    diff_added_nodes = []
    diff_removed_nodes = []
    diff_overall_nodes = []
    diff_number_nodes = []
    '''

    #nodes_shifts = {}
    
    existing_nodes = sets.Set()
      
    degrees_in = []
    degrees_out = []
    degrees_overall = []

    edges_removed = []
    edges_added = []
    edges_overall = []


    prev_g = None
    for i in range(len(times)):
        time = times[i]
        
        g = load_time_network(time)

        #'''
        if constants.DATASET=='etoro':
            dt = datetime.strptime(time, constants.GENERAL_DATE_FORMAT)
            if dt.weekday()==5 or dt.weekday()==6:
                continue
        if len(g.nodes())==0:
            print '### ', time
            continue
        #'''

        print str(time) + ':' + str(len(g.edges()))
               
        '''
        for v in nodes:
            popularity = g.in_degree(v) if v in g.node else 0
            
            if v not in nodes_popularity:
                nodes_popularity[v] = []                    
            nodes_popularity[v].append(popularity)
        '''
        
        if prev_g != None:

            '''
            shift = 0
            #nodes_to_iterate = nodes
            nodes_to_iterate = existing_nodes
            for v in nodes_to_iterate:
                s1 = sets.Set(prev_g.edges(v) if v in prev_g else [])
                s2 = sets.Set(g.edges(v) if v in g else [])
                u = s1.union(s2)
                i = s1.intersection(s2)
                
                diff = 0 if len(u)==0 else float(1) - float(len(i)) / float(len(u))
                #diff = len(u) - len(i)
                #diff = len(s1) - len(s2)
                
                shift = shift + numpy.square(diff)
            shift = float(shift) / float(len(nodes_to_iterate))
            shift = numpy.sqrt(shift)
            network_shifts_by_individuals.append(shift)
            '''

            '''
            #inter = existing_nodes
            inter = (sets.Set(prev_g.nodes())).intersection((sets.Set(g.nodes())))
            diff1 = (sets.Set(prev_g.nodes())).difference(inter)
            diff2 = (sets.Set(g.nodes())).difference(inter)

            inter_inter = (sets.Set(prev_g.edges(inter))).intersection((sets.Set(g.edges(inter))))
            inter_diff1 = (sets.Set(prev_g.edges(inter))).difference(inter_inter)
            inter_diff2 = (sets.Set(g.edges(inter))).difference(inter_inter)

            
            inter_number_nodes = len(inter)
            inter_number_edges = len(inter_inter)
            inter_removed_edges = len(inter_diff1)
            inter_added_edges = len(inter_diff2)
            inter_overall_edges = inter_removed_edges + inter_added_edges
        
            diff_removed_nodes = len(diff1)
            diff_added_nodes = len(diff2)
            diff_overall_nodes = diff_removed_nodes + diff_added_nodes 
            diff_removed_edges = len(prev_g.edges(diff1))
            diff_added_edges = len(g.edges(diff2))
            diff_overall_edges = diff_removed_edges + diff_added_edges

            print inter_number_nodes, inter_number_edges, inter_removed_edges, inter_added_edges, inter_overall_edges, diff_removed_nodes, diff_added_nodes, diff_overall_nodes, diff_removed_edges, diff_added_edges, diff_overall_edges  

            added.append(inter_added_edges)
            removed.append(inter_removed_edges)
            '''

            nodesNormFactor = float(len(existing_nodes))

            state1 = [prev_g.in_degree(v) if v in prev_g.node else 0 for v in nodes]
            state2 = [g.in_degree(v) if v in g.node else 0 for v in nodes]
            distance = numpy.average( [(state1[i]-state2[i])**2 for i in range(len(nodes))] ) ** 0.5
            distance = distance / nodesNormFactor
            degrees_in.append(distance)

            state1 = [prev_g.out_degree(v) if v in prev_g.node else 0 for v in nodes]
            state2 = [g.out_degree(v) if v in g.node else 0 for v in nodes]
            distance = numpy.average( [(state1[i]-state2[i])**2 for i in range(len(nodes))] ) ** 0.5
            distance = distance / nodesNormFactor
            degrees_out.append(distance)

            state1 = [prev_g.degree(v) if v in prev_g.node else 0 for v in nodes]
            state2 = [g.degree(v) if v in g.node else 0 for v in nodes]
            distance = numpy.average( [(state1[i]-state2[i])**2 for i in range(len(nodes))] ) ** 0.5
            distance = distance / nodesNormFactor
            degrees_overall.append(distance)
            
            
            
            
            state1 = sets.Set(prev_g.edges())
            state2 = sets.Set(g.edges())

            distance = len( state1.difference(state2) )
            distance = float(distance) / nodesNormFactor
            edges_removed.append(distance)

            distance = len( state2.difference(state1) )
            distance = float(distance) / nodesNormFactor
            edges_added.append(distance)

            distance = edges_removed[-1] + edges_added[-1]
            edges_overall.append(distance)

            '''
            #prev_g_existing = prev_g.subgraph(existing_nodes)
            #g_existing = g.subgraph(existing_nodes)
            #prev_g_existing = prev_g
            #g_existing = g.subgraph(prev_g.nodes())
            prev_g_existing = prev_g.subgraph(inter)
            g_existing = g.subgraph(inter)

            prev_edges = sets.Set(prev_g_existing.edges())
            edges = sets.Set(g_existing.edges())
            m1 = edges.difference(prev_edges)
            m2 = prev_edges.difference(edges)
            #u = prev_edges.union(edges)

            #nodesNormFactor = float(len(existing_nodes))
            #nodesNormFactor = float(len((sets.Set(prev_g_existing.nodes())).union((sets.Set(g_existing.nodes())))))
            #nodesNormFactor = len(inter)
            nodesNormFactor = 1.0
            #edgesNormFactor = nodesNormFactor * (nodesNormFactor - 1.0)
            #edgesNormFactor = float(len(u))
            #edgesNormFactor = nodesNormFactor
            #edgesNormFactor = float(len(prev_edges))
            edgesNormFactor = 1.0
            
            print nodesNormFactor, edgesNormFactor

            
            shift = float(len(m1)+len(m2))
            if constants.DATASET=='etoro':
                shift = shift / edgesNormFactor
            network_shifts.append(shift)
                
            added = float(len(m1))
            if constants.DATASET=='etoro':
                added = added / edgesNormFactor
            network_added_edges.append(added)

            removed = float(len(m2))
            if constants.DATASET=='etoro':
                removed = removed / edgesNormFactor
            network_removed_edges.append(removed)

            number = float(len(edges))
            if constants.DATASET=='etoro':
                number = number / edgesNormFactor
            network_number_edges.append(number)


            if constants.DATASET=='etoro':
                m3 = sets.Set(g.nodes())
                #m3 = m3.difference(existing_nodes)
                m3 = m3.difference(inter)
                new_nodes = float(len(m3)) / nodesNormFactor
                network_new_nodes.append(new_nodes)
    
                m4 = g.edges(m3)
                new_edges = float(len(m4)) / nodesNormFactor
                network_new_edges.append(new_edges)


                for v in nodes:
                    prev_edges = sets.Set(prev_g.edges(v) if v in prev_g else [])
                    edges = sets.Set(g.edges(v) if v in g else [])
                    m1 = edges.difference(prev_edges)
                    m2 = prev_edges.difference(edges)

                    shift = float(len(m1)+len(m2)) / nodesNormFactor
                    
                    if v not in nodes_shifts:
                        nodes_shifts[v] = []                    
                    nodes_shifts[v].append(shift)
            '''

        if constants.DATASET=='etoro':    
            existing_nodes.union_update(g.nodes())
        else:
            if prev_g==None:
                existing_nodes.union_update(g.nodes())
                  
        #print len(existing_nodes)

        prev_g = g

    #'''
    plot_changes(degrees_in, 'degrees_in')
    plot_changes(degrees_out, 'degrees_out')
    plot_changes(degrees_overall, 'degrees_overall')
    #'''

    plot_changes(edges_removed, 'edges_removed')
    plot_changes(edges_added, 'edges_added')
    plot_changes(edges_overall, 'edges_overall')
    
    '''    
    if constants.DATASET=='bt':
        #temp = network_shifts_by_individuals
        #network_shifts_by_individuals = []
        #network_shifts_by_individuals.extend(temp[0:53])
        #network_shifts_by_individuals.extend(temp[75:])

        temp = network_shifts
        network_shifts = []
        network_shifts.extend(temp[0:53])
        network_shifts.extend(temp[75:])
    
        temp = network_added_edges
        network_added_edges = []
        network_added_edges.extend(temp[0:53])
        network_added_edges.extend(temp[75:])
    
        temp = network_removed_edges
        network_removed_edges = []
        network_removed_edges.extend(temp[0:53])
        network_removed_edges.extend(temp[75:])    

        temp = network_number_edges
        network_number_edges = []
        network_number_edges.extend(temp[0:53])
        network_number_edges.extend(temp[75:])    
    '''

    '''
    if constants.DATASET=='etoro':
        firstday = 60
        network_shifts = network_shifts[firstday:]
        network_added_edges = network_added_edges[firstday:]
        network_removed_edges = network_removed_edges[firstday:]
        network_number_edges = network_number_edges[firstday:]
        network_new_nodes = network_new_nodes[firstday:]
        network_new_edges = network_new_edges[firstday:]
    '''


    '''
    ### individuals nodes
    for v in nodes_shifts:
        ###shifts
        s_values = [s for s in nodes_shifts[v]]
        plot_values(range(len(s_values)), s_values, False, 'nodes_shifts_' + str(v))
        s_values.sort(reverse=True)
        plot_values(range(len(s_values)), s_values, False, 'nodes_shifts_sorted_' + str(v))

        ###popularity
        p_values = [p for p in nodes_popularity[v]]
        plot_values(range(len(p_values)), p_values, False, 'nodes_popularity_' + str(v))
        p_values.sort(reverse=True)
        plot_values(range(len(p_values)), p_values, False, 'nodes_popularity_sorted_' + str(v))
    '''
        
    '''
    ###network shifts by individuals   
    const = numpy.median(network_shifts_by_individuals)
    network_shifts_by_individuals = [numpy.max([s, const])/numpy.min([s, const]) for s in network_shifts_by_individuals]
    #network_shifts_by_individuals = [numpy.abs(s-const) for s in network_shifts_by_individuals]
    #network_shifts_by_individuals = [numpy.abs(s-const)/const for s in network_shifts_by_individuals]

    plot_values(range(len(network_shifts_by_individuals)), network_shifts_by_individuals, False, 'network_shifts_by_individuals')

    network_shifts_by_individuals.sort(reverse=True)
    plot_values(range(len(network_shifts_by_individuals)), network_shifts_by_individuals, False, 'network_shifts_by_individuals_sorted')
    
    plot_bins(network_shifts_by_individuals, nBins, True, 'network_shifts_by_individuals_bins_' + str(nBins))
    '''

    '''
    loglog = True
    logbins = False
    
    if constants.DATASET=='etoro':
        nBins = 20
        fromconstant = False
    else:
        nBins = 100
        fromconstant = True
    
    ###network shifts
    if fromconstant:
        const = numpy.mean(network_shifts)
        #network_shifts = [numpy.max([s, const])/numpy.min([s, const]) for s in network_shifts]
        network_shifts = [numpy.abs(s-const) for s in network_shifts]
        #network_shifts = [numpy.abs(s-const)/const for s in network_shifts]
    
    plot_values(range(len(network_shifts)), network_shifts, 'network_shifts')

    network_shifts.sort(reverse=True)
    plot_values(range(len(network_shifts)), network_shifts, 'network_shifts_sorted')
    
    plot_bins(network_shifts, nBins, loglog, logbins, 'network_shifts_bins_' + str(nBins))
    
    
    ###network added edges
    if fromconstant:
        const = numpy.mean(network_added_edges)
        #network_added_edges = [numpy.max([s, const])/numpy.min([s, const]) for s in network_added_edges]
        network_added_edges = [numpy.abs(s-const) for s in network_added_edges]
        #network_added_edges = [numpy.abs(s-const)/const for s in network_added_edges]

    plot_values(range(len(network_added_edges)), network_added_edges, 'network_added_edges')

    network_added_edges.sort(reverse=True)
    plot_values(range(len(network_added_edges)), network_added_edges, 'network_added_edges_sorted')
    
    plot_bins(network_added_edges, nBins, loglog, logbins, 'network_added_edges_bins_' + str(nBins))


    ###network removed edges
    if fromconstant:
        const = numpy.mean(network_removed_edges)
        #network_removed_edges = [numpy.max([s, const])/numpy.min([s, const]) for s in network_removed_edges]
        network_removed_edges = [numpy.abs(s-const) for s in network_removed_edges]
        #network_removed_edges = [numpy.abs(s-const)/const for s in network_removed_edges]

    plot_values(range(len(network_removed_edges)), network_removed_edges, 'network_removed_edges')

    network_removed_edges.sort(reverse=True)
    plot_values(range(len(network_removed_edges)), network_removed_edges, 'network_removed_edges_sorted')
    
    plot_bins(network_removed_edges, nBins, loglog, logbins, 'network_removed_edges_bins_' + str(nBins))


    ###network number edges
    plot_values(range(len(network_number_edges)), network_number_edges, 'network_number_edges')


    if constants.DATASET=='etoro':
        ###network new nodes
        plot_values(range(len(network_new_nodes)), network_new_nodes, 'network_new_nodes')
    
        network_new_nodes.sort(reverse=True)
        plot_values(range(len(network_new_nodes)), network_new_nodes, 'network_new_nodes_sorted')
        
        plot_bins(network_new_nodes, nBins, loglog, logbins, 'network_new_nodes_bins_' + str(nBins))
        
    
        ###network new edges
        plot_values(range(len(network_new_edges)), network_new_edges, 'network_new_edges')
    
        network_new_edges.sort(reverse=True)
        plot_values(range(len(network_new_edges)), network_new_edges, 'network_new_edges_sorted')
        
        plot_bins(network_new_edges, nBins, loglog, logbins, 'network_new_edges_bins_' + str(nBins))

        ### all nodes
        all_nodes_shifts = []
        for v in nodes_shifts:
            all_nodes_shifts.extend(nodes_shifts[v])

        #all_nodes_shifts.sort(reverse=True)
        #plot_values(range(len(all_nodes_shifts)), all_nodes_shifts, 'all_nodes_shifts_sorted')

        plot_bins(all_nodes_shifts, nBins, loglog, logbins, 'all_nodes_shifts_bins_' + str(nBins))
        '''
        

def plot_changes(data, suffix):
    fromconstant = (constants.DATASET!='etoro')
    loglog = True 
    
    data = [d for d in data if d!=max(data)]
        
    '''
    X = range(len(data))
    Y1 = data
    
    fit = pylab.polyfit(X, Y1, 1)
    fit_fn = pylab.poly1d(fit)
    Y2 = fit_fn(X)
    
    data = [Y1[i]/Y2[i] for i in range(len(X))]
    '''

    if fromconstant:
        const = numpy.mean(data)
        #data = [numpy.abs(s-const) for s in data]
        data = [max(s, const)/min(s, const) for s in data]
    
    plot_values(range(len(data)), data, suffix)

    data.sort(reverse=True)
    plot_values(range(len(data)), data, suffix + '_sorted')
    
    for nBins in [100]:
        plot_bins(data, nBins, loglog, True, suffix + '_log_bins_' + str(nBins))
        #plot_bins(data, nBins, loglog, False, suffix + '_lin_bins_' + str(nBins))


def plot_values(X, Y, suffix):
    output_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + suffix

    
    if constants.DATASET=='etoro':
        yfactor = 1.0 #100000
        Y = [y*yfactor for y in Y]
    
    
    pylab.figure(figsize=(7.5, 7))

    pylab.rcParams.update({'font.size': 20})

    pylab.scatter(X, Y)

    pylab.axis(get_bounds(X, Y, False))
    
    pylab.xlabel('Day')
    if constants.DATASET=='etoro':
        pylab.ylabel('Change (*10^' + str(int(math.log10(yfactor))) + ')')
    else:
        pylab.ylabel('Change')
    

    pylab.tight_layout()

    pylab.savefig(output_filename + '.pdf')


def plot_bins(Y, nBins, loglog, logbins, suffix):
    output_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + suffix


    X1, Y1, X2, Y2, alpha = fit_data(Y, False, False)      

    
    
    pylab.figure(figsize=(7.5, 7))
    
    pylab.rcParams.update({'font.size': 20})

    pylab.scatter(X1, Y1)

    #pylab.plot(X2, Y2, '--')

    bounds = get_bounds(X1, Y1, loglog)

    if loglog:
        pylab.xscale('log')
        pylab.yscale('log')
        xtext = numpy.exp(numpy.log(bounds[0])+(numpy.log(bounds[1])-numpy.log(bounds[0]))*0.65)
        ytext = numpy.exp(numpy.log(bounds[2])+(numpy.log(bounds[3])-numpy.log(bounds[2]))*0.65)
    else:
        xtext = (bounds[0]+bounds[1])/2.0
        ytext = (bounds[2]+bounds[3])/2.0            

    pylab.axis(bounds)

    pylab.text(xtext, ytext, '$gamma$='+'{0:.2f}'.format(alpha))
    
    pylab.xlabel('Change')
    pylab.ylabel('Density')

    pylab.tight_layout()

    pylab.savefig(output_filename + '.pdf')




#####################################################################################
### part 2
#####################################################################################

def plot_snapshot_evolution(times, period, all_times, threshold):
    all_top_nodes = sets.Set()
    for time in times:
        g = load_period_network(time, period, all_times)
        
        top_nodes = rank_network_nodes(g)
        top_nodes = top_nodes[-threshold:]
        all_top_nodes.union_update(top_nodes)
    
    all_top_nodes = [v for v in all_top_nodes]
    
    
    sqrt_size = int( math.ceil( math.sqrt( len(all_top_nodes) ) ) )
    
    
    prev_top_nodes = None
    prev_g = None

    subplot_id = 1
    for time in times:
        g = load_period_network(time, period, all_times)
        
        top_nodes = rank_network_nodes(g)
        top_nodes = top_nodes[-threshold:]

        ignored = [[], [], []]
        remained = [[], [], []]
        added = [[], [], []]
        removed = [[], [], []]
                
        for i in range(len(all_top_nodes)):
            v = all_top_nodes[i]
            
            
            if v not in top_nodes:
                if prev_top_nodes!=None and v in prev_top_nodes:
                    to_change = removed
                    size = prev_g.degree(v)
                else:
                    to_change = ignored
                    size = 1
            else:
                if prev_top_nodes==None or v in prev_top_nodes:
                    to_change = remained
                    size = g.degree(v)
                else:
                    to_change = added
                    size = g.degree(v)

            x = i%sqrt_size
            y = sqrt_size - 1 - i/sqrt_size
                      
            to_change[0].append(x)
            to_change[1].append(y)
            to_change[2].append(size)

    
        
        output_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + 'snapshot_evolution_' + str(time)

        pylab.figure(figsize=(7.5, 7))
        pylab.rcParams.update({'font.size': 20})
    
        #pylab.scatter(ignored[0], ignored[1], s=ignored[2], c='black')
        pylab.scatter(remained[0], remained[1], s=remained[2], c='blue')
        pylab.scatter(added[0], added[1], s=added[2], c='green')
        pylab.scatter(removed[0], removed[1], s=removed[2], c='red')

        pylab.axis([-1, sqrt_size, -1, sqrt_size])

        pylab.gca().xaxis.set_visible(False)
        pylab.gca().yaxis.set_visible(False)
                
        pylab.title('Snapshot ' + str(subplot_id))

        pylab.tight_layout()
        pylab.savefig(output_filename + '.pdf')

        
        prev_top_nodes = top_nodes
        prev_g = g

        subplot_id = subplot_id + 1
        

def plot_snapshot_degrees(times, period, all_times):
    loglog = True
    

    subplot_id = 1
    for time in times:
        g = load_period_network(time, period, all_times)
        
        
        popularities = [g.in_degree(v) for v in g.node]
        
               
        X1, Y1, X2, Y2, alpha = fit_data(popularities, True)      
  
   
        output_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + 'snapshot_degrees_' + str(time)

        pylab.figure(figsize=(7.5, 7))
        pylab.rcParams.update({'font.size': 20})
    
        pylab.scatter(X1, Y1)
    
        pylab.plot(X2, Y2, '--')
    
        bounds = get_bounds(X1, Y1, loglog)

        if loglog:
            pylab.xscale('log')
            pylab.yscale('log')
            xtext = numpy.exp(numpy.log(bounds[0])+(numpy.log(bounds[1])-numpy.log(bounds[0]))*0.65)
            ytext = numpy.exp(numpy.log(bounds[2])+(numpy.log(bounds[3])-numpy.log(bounds[2]))*0.65)
        else:
            xtext = (bounds[0]+bounds[1])/2.0
            ytext = (bounds[2]+bounds[3])/2.0            
    
        pylab.axis(bounds)

        pylab.text(xtext, ytext, '$\\gamma$='+'{0:.2f}'.format(alpha))
        
        pylab.title('Snapshot ' + str(subplot_id))

        pylab.xlabel('Degree')
        pylab.ylabel('Density')
        
        pylab.tight_layout()
    
        pylab.savefig(output_filename + '.pdf')
        
        subplot_id = subplot_id + 1


def plot_whole_network_degrees(all_times):
    loglog = True


    g = load_period_network(all_times[0], len(all_times), all_times)


    popularities = [g.in_degree(v) for v in g.node]
    

    X1, Y1, X2, Y2, alpha = fit_data(popularities, True)
    
    
    output_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + 'whole_network_degrees'

    pylab.figure(figsize=(7.5, 7))
    pylab.rcParams.update({'font.size': 20})

    pylab.scatter(X1, Y1)
    
    pylab.plot(X2, Y2, '--')
    
    bounds = get_bounds(X1, Y1, loglog)
    
    if loglog:
        pylab.xscale('log')
        pylab.yscale('log')
        xtext = numpy.exp(numpy.log(bounds[0])+(numpy.log(bounds[1])-numpy.log(bounds[0]))*0.65)
        ytext = numpy.exp(numpy.log(bounds[2])+(numpy.log(bounds[3])-numpy.log(bounds[2]))*0.65)
    else:
        xtext = (bounds[0]+bounds[1])/2.0
        ytext = (bounds[2]+bounds[3])/2.0            
    
    pylab.axis(bounds)
    
    pylab.text(xtext, ytext, '$\\gamma$='+'{0:.2f}'.format(alpha))
    
    pylab.ylabel('Density')
    pylab.xlabel('Degree')

    pylab.tight_layout()

    pylab.savefig(output_filename + '.pdf')
 
        



#####################################################################################
### utils
#####################################################################################

def get_times():
    filenames = os.listdir(constants.GRAPHS_FOLDER_NAME)
    filenames.sort()
    return filenames;


def load_time_network(time):
    print 'Processing: ' + time

    input_filename = constants.GRAPHS_FOLDER_NAME + time
    
    #g = nx.read_gpickle(input_filename)
    #g = nx.read_edgelist(input_filename, create_using=nx.DiGraph(), delimiter='\t', encoding='ANSI')

    g = nx.DiGraph()
    reader = open(input_filename, 'r')
    for line in reader:
        line = line.strip()
        
        fields = line.split('\t')
        
        if len(fields)<2:
            #print line
            continue;
        
        g.add_edge(fields[0], fields[1])

    reader.close()
    return g


def load_period_network(time, period, all_times):
    g = nx.DiGraph()
    time_idx = all_times.index(time)
    for t in all_times[time_idx:time_idx+period]:
        g_time = load_time_network(t)
        g.add_edges_from(g_time.edges())

    return g


def get_top_nodes(times, threshold):
    all_top_nodes = sets.Set()
    for time in times:
        g = load_time_network(time)
        ranked_nodes = rank_network_nodes(g)
        if threshold<0:
            top_nodes = ranked_nodes
        else:
            top_nodes = ranked_nodes[-threshold:]
        
        all_top_nodes.union_update(top_nodes)
    
    return all_top_nodes


def rank_network_nodes(g):
    ranked_nodes = [(g.in_degree(v), v) for v in g.nodes()]
    ranked_nodes.sort()
    ranked_nodes = [e[1] for e in ranked_nodes]
     
    return ranked_nodes


def fit_data(Y, discrete, pdf=True):
    Y = [y for y in Y if y>0]


    fit = powerlaw.Fit(Y, discrete=discrete)
    alpha = fit.alpha
    xmin = fit.xmin
    print 'alpha:', alpha, 'xmin:', xmin

    if pdf:
        X1, Y1 = fit.pdf()
    else:
        X1, Y1 = fit.ccdf()
    X1 = [X1[i] for i in range(len(Y1)) if Y1[i]>0]
    Y1 = [Y1[i] for i in range(len(Y1)) if Y1[i]>0]

    pl = powerlaw.Power_Law(
        xmin = fit.xmin,
        xmax = fit.xmax,
        discrete = fit.discrete,
        estimate_discrete = fit.estimate_discrete,
        fit_method = fit.fit_method,
        data = fit.data,
        parameter_range = fit.parameter_range,
        parent_Fit = fit
    )
    X2 = X1
    if pdf:
        Y2 = pl.pdf(data=X2)
    else:
        Y2 = pl.ccdf(data=X2)
    
    '''
    [p, gof] = plpva.plpva(Y, xmin, 'reps', 2)
    print 'p:', p
    '''
    
    '''
    R, p = fit.distribution_compare('power_law', 'exponential', normalized_ratio=True)
    print 'power_law > exponential', R, p
    R, p = fit.distribution_compare('power_law', 'lognormal', normalized_ratio=True)
    print 'power_law > lognormal', R, p
    '''
    '''
    R, p = fit.distribution_compare('truncated_power_law', 'exponential', normalized_ratio=True)
    print 'truncated_power_law > exponential', R, p
    R, p = fit.distribution_compare('truncated_power_law', 'lognormal', normalized_ratio=True)
    print 'truncated_power_law > lognormal', R, p
    '''


    
    '''
    results = plfit.plfit(popularities)
    alpha = results[0]
    xmin = results[1]
    print 'alpha:', alpha, 'xmin:', xmin
    '''

    '''
    results = plfit2.plfit(popularities, discrete=True, quiet=False, verbose=True)
    results.plotpdf()
    pylab.show()
    return
    '''
    
    '''
    X, Y1, Y2, fit = data_into_bins(popularities, 100, loglog, True)
    '''


    return X1, Y1, X2, Y2, alpha


def get_bounds(X, Y, loglog):
    if loglog:
        minX = min(X) / 1.5           
        maxX = max(X) * 1.5
        minY = min(Y) / 2.0
        maxY = max(Y) * 2.0
    else:
        marginX = float(max(X) - min(X))/10.0
        marginY = float(max(Y) - min(Y))/10.0
        minX = min(X) - marginX
        maxX = max(X) + marginX
        minY = min(Y) - marginY
        maxY = max(Y) + marginY
        
    return [minX, maxX, minY, maxY]



#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'




#####################################################################################
### old
#####################################################################################

'''
def data_into_bins(Y, nBins, loglog, logbins):
    if logbins:
        Y = [y for y in Y if y>0]
    
    xmax = max(Y)
    xmin = min(Y)
    
    
    if logbins:
        log_min_size = numpy.log10(xmin)
        log_max_size = numpy.log10(xmax)
        bins = numpy.logspace( log_min_size, log_max_size, num=nBins )

        #coeff = numpy.power(xmax/xmin, 1.0/float(nBins))
        #bins = [float(xmax)/float(numpy.power(coeff, nBins-i)) for i in range(nBins+1)]
    else:
        bins = numpy.linspace( xmin, xmax, num=nBins )
        
    N, edges = numpy.histogram(Y, bins, density=True)

    X = [(edges[i] + edges[i+1])/2.0 for i in range(len(N)) if N[i]>0]
    Y1 = [N[i] for i in range(len(N)) if N[i]>0]
    
    Y2, alpha = fit_powerlaw(Y, X, Y1)
    
    return X, Y1, Y2, alpha


def fit_powerlaw(data, binsx, binsy):
    #fit = pylab.polyfit(numpy.log(X), numpy.log(Y1), 1)
    #fit_fn = pylab.poly1d(fit)
    #Y2 = numpy.exp(fit_fn(numpy.log(X)))

    results = powerlaw.Fit(data)
    alpha = results.alpha
    #print min(data), results.xmin, max(data), results.xmax, results.alpha, results.sigma, results.sigma_threshold
    
    Y2 = [numpy.power(x, (-1.0)*results.alpha) for x in binsx]
    
    return Y2, alpha
''' 
