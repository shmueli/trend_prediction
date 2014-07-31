import helpers.constants as constants
import os
import networkx as nx
import pylab
import sets
import numpy

BASE = 2

def execute():
    times = get_times()
    for threshold in [-1]:
        all_top_nodes = get_top_nodes(times, threshold)
        plot_shifts(times, all_top_nodes, 'top' + str(threshold))
    

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
    ranked_nodes = [(len(g.in_edges(v)), v) for v in g.node]
    ranked_nodes.sort()
    ranked_nodes = [e[1] for e in ranked_nodes]
     
    return ranked_nodes

     
def plot_shifts(times, nodes, suffix):
    shifts = []
    prev_state = None
    for time in times:
        g = load_time_network(time)
        
        state = calc_network_state(g, nodes)
        
        if prev_state!=None:
            shift = diff_network(prev_state, state, len(nodes))
            shifts.append( shift )
                
        prev_state = state

    print len(nodes)

    ##############################
    # ordered
    ##############################

    ###test
    const = numpy.median(shifts)
    shifts = [numpy.abs(s-const) for s in shifts]  
    ###
    
    values = [s for s in shifts]
    values.sort(reverse=True)
    plot_values(values, 'XXX')
    
    ###'''
    ##############################
    # bins 15
    ##############################



    Y = shifts
    minY = min(Y)
    maxY = max(Y)
    nBins = 15
    binSize = (maxY-minY)/float(nBins)
    bins = [minY + binSize*float(i) for i in range(nBins)]
    print bins

    N, tempbins, temppatches = pylab.hist(Y, bins)
    pylab.close()
    N = [float(n)/float(sum(N)) for n in N]
    N = [n for n in N]
    print N



    X = [bins[i+1] for i in range(len(N)) if bins[i+1]>0 and N[i]>0]
    Y1 = [N[i] for i in range(len(N)) if bins[i+1]>0 and N[i]>0]
    
    fit = pylab.polyfit(numpy.log(X), numpy.log(Y1), 1)
    fit_fn = pylab.poly1d(fit)
    Y2 = numpy.exp(fit_fn(numpy.log(X)))
    
    output_filename = constants.CHARTS_FOLDER_NAME + 'shifts_bins_15' + '_' + suffix
    
    pylab.figure(figsize=(9, 4))
    pylab.xscale('log')
    pylab.yscale('log')
    pylab.scatter(X, Y1)
    pylab.plot(X, Y2, '--')
    #pylab.xlabel('Distance between following network states')
    #pylab.ylabel('Probability')
    #pylab.title(output_filename)
    pylab.savefig(output_filename + '.pdf')
    pylab.close()
    

    #'''
    ##############################
    # bins 30
    ##############################

    Y = shifts
    minY = min(Y)
    maxY = max(Y)
    nBins = 30
    binSize = (maxY-minY)/float(nBins)
    bins = [minY + binSize*float(i) for i in range(nBins)]
    print bins

    N, tempbins, temppatches = pylab.hist(Y, bins)
    pylab.close()
    N = [float(n)/float(sum(N)) for n in N]
    N = [n for n in N]
    print N



    X = [bins[i+1] for i in range(len(N)) if bins[i+1]>0 and N[i]>0]
    Y1 = [N[i] for i in range(len(N)) if bins[i+1]>0 and N[i]>0]
    
    fit = pylab.polyfit(numpy.log(X), numpy.log(Y1), 1)
    fit_fn = pylab.poly1d(fit)
    Y2 = numpy.exp(fit_fn(numpy.log(X)))
    
    output_filename = constants.CHARTS_FOLDER_NAME + 'shifts_bins_30' + '_' + suffix
    
    pylab.figure(figsize=(9, 4))
    pylab.xscale('log')
    pylab.yscale('log')
    pylab.scatter(X, Y1)
    pylab.plot(X, Y2, '--')
    #pylab.xlabel('Distance between following network states')
    #pylab.ylabel('Probability')
    #pylab.title(output_filename)
    pylab.savefig(output_filename + '.pdf')
    pylab.close()
    #'''

def plot_time_histogram(by_times, by_nodes, nodes, time, suffix):
    ranking = [by_times[time][v] for v in by_times[time]]
    ranking.sort()

    Y = ranking
    minY = min(Y)
    nBins = 10
    bins = [minY + int(numpy.power(2, i)) for i in range(nBins)]
    print bins

    N, tempbins, temppatches = pylab.hist(Y, bins)
    H = [[bins[i+1], float(N[i])/sum(N)] for i in range(len(N)) if N[i]>0]
    print N
    pylab.close()


    X = [h[0] for h in H]
    Y1 = [h[1] for h in H]
    
    fit = pylab.polyfit(numpy.log(X), numpy.log(Y1), 1)
    fit_fn = pylab.poly1d(fit)
    Y2 = numpy.exp(fit_fn(numpy.log(X)))
    
    output_filename = constants.CHARTS_FOLDER_NAME + 'time_hist' + '_' + suffix

    pylab.figure(figsize=(5, 4))
    pylab.rcParams.update({'font.size': 20})
    pylab.xscale('log')
    pylab.yscale('log')
    pylab.scatter(X, Y1)
    pylab.plot(X, Y2, '--')
    #pylab.xlabel('# of edges')
    #pylab.ylabel('Probability')
    #pylab.title(output_filename)
    pylab.savefig(output_filename + '.pdf')
    pylab.close()


def plot_values(values, suffix):
    X = range(len(values))
    Y = values
    
    output_filename = constants.CHARTS_FOLDER_NAME + 'time_ordered' + '_' + suffix

    pylab.figure(figsize=(5, 4))
    pylab.rcParams.update({'font.size': 20})
    pylab.scatter(X, Y)
    pylab.savefig(output_filename + '.pdf')
    pylab.close()


#'''        
#calculating network structure shift
def calc_node_state(g, v):
    return [e[0] for e in g.in_edges(v)]

def calc_node_empty_state():
    return []

def calc_network_state(g, nodes):
    state = [(v, calc_node_state(g, v)) if v in g.node else (v, calc_node_empty_state()) for v in nodes ]
    state.sort()
    
    return state

def diff_network(state1, state2, norm_factor):
    return numpy.sqrt( numpy.average( [ numpy.square( diff_node(state1[i][1], state2[i][1], norm_factor, i) ) for i in range(len(state1)) ] ) )

def diff_node(state1, state2, norm_factor, i):
    s1 = sets.Set(state1)
    s2 = sets.Set(state2)
    u = s1.union(s2)
    i = s1.intersection(s2)
    
    if len(u)==0:
        return 0
    
    diff = float(1) - float(len(i))/float(len(u))

    return diff
#'''


if __name__ == '__main__':
    execute()

    print 'Done.'
