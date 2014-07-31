import helpers.constants as constants
import helpers.utils as utils
import topdf.topdf as topdf
import os
import networkx as nx
import pylab
import sets
import numpy
import math

BASE = 2

def execute():
    global by_nodes
    global by_times
    
    print 'Loading data...'
    by_nodes, by_times = load_data(False)
    print 'Finished loading data...'

    #plot_top(all_top_nodes, seq_top_nodes)
    #plot_node_dynamics(all_top_nodes, by_nodes)

    #'''
    for t in [len(by_nodes)]:
        all_top_nodes, seq_top_nodes = get_top_nodes(by_times, t)
        plot_shifts(by_times, by_nodes, all_top_nodes, 'top' + str(t))
    #'''

    #times = [0, 30, 60]
    
    '''
    plot_time_ordered_degrees(by_times, times[0], str(times[0]))
    plot_time_ordered_degrees(by_times, times[1], str(times[1]))
    plot_time_ordered_degrees(by_times, times[2], str(times[2]))
    '''
    
    '''
    all_top_nodes, seq_top_nodes = get_top_nodes(by_times, 0)
    plot_time_histogram(by_times, by_nodes, all_top_nodes, times[0], str(times[0]))
    plot_time_histogram(by_times, by_nodes, all_top_nodes, times[1], str(times[1]))
    plot_time_histogram(by_times, by_nodes, all_top_nodes, times[2], str(times[2]))
    '''

    #plot_time_network(by_times, by_nodes, times, 50)
    
    #plot_top_individuals_dynamics(by_times, by_nodes, '');
    

def load_data(from_cache):
    if from_cache:
        input_filename = constants.CHARTS_FOLDER_NAME + 'by_nodes'
        reader = open(input_filename, 'r')
        by_nodes = eval(reader.read())
        reader.close

        input_filename = constants.CHARTS_FOLDER_NAME + 'by_times'
        reader = open(input_filename, 'r')
        by_times = eval(reader.read())
        reader.close
    else:
        by_nodes = {}
        by_times = {}
        
        utils.ensure_folder(constants.CHARTS_FOLDER_NAME)

        filenames = os.listdir(constants.GRAPHS_FOLDER_NAME)
        filenames.sort()

        print len(filenames)
        
        time = 0
        for filename in filenames:
            print 'Processing: ' + filename
        
            input_filename = constants.GRAPHS_FOLDER_NAME + filename
            
            #g = nx.read_gpickle(input_filename)
            g = nx.read_edgelist(input_filename, create_using=nx.DiGraph())
            #for wifi data            
            #g = nx.read_edgelist(input_filename, '#', ',')
            
            for v in g.nodes():
                node_state = calc_node_state(g, v)
                
                if v not in by_nodes:
                    by_nodes[v] = {}
                by_nodes[v][time] = node_state
                
                if time not in by_times:
                    by_times[time] = {}
                by_times[time][v] = node_state
    
            time = time+1
            
        output_filename = constants.CHARTS_FOLDER_NAME + 'by_nodes'
        writer = open(output_filename, 'w')
        writer.write(str(by_nodes))
        writer.close
    
        output_filename = constants.CHARTS_FOLDER_NAME + 'by_times'
        writer = open(output_filename, 'w')
        writer.write(str(by_times))
        writer.close
    
        print len(by_times)
        print len(by_nodes)
        
    return by_nodes, by_times
        

def plot_time_ordered_degrees(by_times, time, suffix):
    print 'Handling ' + str(time)

    print len(by_times)
    
    degrees = [d for v,d in by_times[time].iteritems()]
    degrees.sort(reverse=True)

    print degrees


def plot_values(values, suffix):
    
    '''
    #bins = [math.pow(BASE, i) for i in range(int(math.log(max(degrees), BASE)))]
    bins = [i for i in range(max(degrees)+1) if i in degrees]
    print bins

    N, tempbins, temppatches = pylab.hist(degrees, bins)
    H = [[bins[i], float(N[i])/sum(N)] for i in range(len(N)) if N[i]>0]
    print N
    pylab.close()

    X = [h[0] for h in H if h[0]!=0]
    Y = [h[1] for h in H if h[0]!=0]
    '''

    X = range(len(values))
    Y = values
    
    output_filename = constants.CHARTS_FOLDER_NAME + 'time_ordered' + '_' + suffix

    pylab.figure(figsize=(9, 4))
    pylab.rcParams.update({'font.size': 20})
    #pylab.xscale('log')
    #pylab.yscale('log')
    pylab.scatter(X, Y)
    #pylab.xlabel('# of edges')
    #pylab.ylabel('Probability')
    #pylab.title(output_filename)
    pylab.savefig(output_filename + '.pdf')
    pylab.close()


def get_top_nodes(by_times, threshold):
    seq_top_nodes = []
    for time in by_times:
        top_nodes = rank_time_nodes(by_times, time)
        top_nodes = top_nodes[-threshold:]
        
        seq_top_nodes.append(top_nodes)

    all_top_nodes = sets.Set()
    for top_nodes in seq_top_nodes:
        all_top_nodes.union_update(top_nodes)
    ordered_nodes = []
    ordered_nodes.extend(all_top_nodes)
    all_top_nodes = ordered_nodes

    return all_top_nodes, seq_top_nodes


'''
def plot_top(all_top_nodes, seq_top_nodes):
    output_filename = _output_folder + 'top'

    X = []
    Y = []
    for x in range(len(all_top_nodes)):
        v = all_top_nodes[x]
        for y in range(len(seq_top_nodes)):
            if v in seq_top_nodes[y]:
                X.append(y)
                Y.append(x)
    
    pylab.figure()
    pylab.scatter(X,Y)
    pylab.xlabel('time')
    pylab.ylabel('node id')
    pylab.title(output_filename)
    pylab.savefig(output_filename + '.pdf')
            

def plot_node_dynamics(all_top_nodes, by_nodes):
    for i in range(len(all_top_nodes)):
        node = all_top_nodes[i]
        
        X = []
        Y = []
        for x,y in by_nodes[node].iteritems():
            X.append(x)
            Y.append(y)

        output_filename = _output_folder + 'dynamics_' + str(i)
        
        pylab.figure()
        pylab.scatter(X,Y)
        pylab.xlabel('time')
        pylab.ylabel('# of in edges')
        pylab.title(output_filename)
        pylab.savefig(output_filename + '.pdf')
'''

        
def plot_shifts(by_times, by_nodes, nodes, suffix):
    shifts = []
    times = by_times.keys()
    times.sort()
    prev_state = None
    for time in times:
        #get rid of saturdays and sundays
        #if time%7==1 or time%7==2:
        #if time%7==1:
        #    continue
        
        state = calc_network_state(by_times, nodes, time)
        
        if prev_state!=None:
            shift = diff_network(prev_state, state, len(by_nodes))
            shifts.append( shift )
                
        prev_state = state

    print len(nodes)
    print len(shifts)

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
    


def plot_time_network(by_times, by_nodes, times, threshold):
    prev_nodes = None

    all_nodes = sets.Set()
    for time in times:
        nodes = rank_time_nodes(by_times, time)
        nodes = nodes[-threshold:]
        all_nodes.union_update(nodes)
    all_nodes = [v for v in all_nodes]
    
    for time in times:
        '''
        filenames = os.listdir(_input_folder)
        filenames.sort()
        current_time = 0
        for filename in filenames:
            if current_time!=time:
                input_filename = _input_folder + filename
                g = nx.read_gpickle(input_filename)
                break
            else:
                time = time+1
        '''
        
        nodes = rank_time_nodes(by_times, time)
        nodes = nodes[-threshold:]
        
        g = nx.DiGraph()

        cnt = 0
        for i in range(len(all_nodes)):
            v = all_nodes[i]
            
            
            x = -165 + (i%12)*30
            y = -165 + (i/12)*30
            
            if v not in nodes:
                if prev_nodes!=None and v in prev_nodes:
                    fill = '#FF0000'
                    outline = '#000000'
                    size = 10
                else:
                    fill = '#000000'
                    outline = '#000000'
                    size = 2
            else:
                if prev_nodes==None or v in prev_nodes:
                    fill = '#0000FF'
                else:
                    fill = '#00FF00'
                cnt = cnt + 1
                outline = '#000000'

                size = 5 + 2*(int(numpy.sqrt( float(by_times[time][v])/math.pi ) ) + 1)
               
                #print str(by_times[time][v]) + '\t' + str(size)
                
            nodeAttributes = {
                'x': x,
                'y': y,
                'w': size,
                'h': size,
                'fill': fill,
                'type': 'ellipse',
                'outline': outline,
                'outline_width': 1.0
            }
            g.add_node(v, graphics=nodeAttributes)
    
        '''
        for e in g.edges():
            if e[0] in nodes and v[1] in nodes:
                g_filtered.add_edge(e[0], e[1])
        '''
    
        print cnt
        
        output_filename = constants.CHARTS_FOLDER_NAME + 'time_network' + '_' + str(time)
        
        nx.write_gml(g, output_filename + '.gml')
        topdf.toPDF(output_filename + '.gml')
        
        prev_nodes = nodes

        #break
        


'''
#calculating popularity shift
def calc_node_state(g, v):
    return len(g.in_edges(v))

def calc_node_empty_state():
    return 0

def calc_network_state(by_times, nodes, time):
    state = [(by_times[time][v],v) for v in nodes if v in by_times[time]]
    state.extend([(calc_node_empty_state(),v) for v in nodes if v not in by_times[time]])
    state.sort()
    state = [(state[i][1],state[i][0]) for i in range(len(state))]
    state.sort()
    
    return state

def diff_network(state1, state2, norm_factor):
    return numpy.sqrt( numpy.average( [ numpy.square( diff_node(state1[i][1], state2[i][1], norm_factor) ) for i in range(len(state1)) ] ) )

def diff_node(state1, state2, norm_factor):
    return float(state2-state1) / float(norm_factor)
'''


#'''        
#calculating network structure shift
def calc_node_state(g, v):
    return [e[0] for e in g.in_edges(v)]

def calc_node_empty_state():
    return []

def calc_network_state(by_times, nodes, time):
    state = [(by_times[time][v],v) for v in nodes if v in by_times[time]]
    state.extend([(calc_node_empty_state(),v) for v in nodes if v not in by_times[time]])
    state.sort()
    state = [(state[i][1],state[i][0]) for i in range(len(state))]
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

def rank_time_nodes(by_times, time):
    top_nodes = [(len(vs),v) for v,vs in by_times[time].iteritems()]
    top_nodes.sort()
    print str(top_nodes[-1][0]) + ',' + str(top_nodes[-2][0]) + ',' + str(top_nodes[0][0]) 

    top_nodes = [e[1] for e in top_nodes]
    
    
    return top_nodes

#'''











def plot_top_individuals_dynamics(by_times, by_nodes, suffix):
    top_nodes, seq_top_nodes = get_top_nodes(by_times, 10)
    
    for i in range(len(top_nodes)):
        node = top_nodes[i]
        
        Y = [len(by_times[time][node]) if node in by_times[time] else 0 for time in by_times]
        X = range(len(Y))
    
        output_filename = constants.CHARTS_FOLDER_NAME + 'top_' + str(i)
        
        pylab.figure(figsize=(9, 4))
        pylab.scatter(X, Y)
        pylab.savefig(output_filename + '.pdf')
        pylab.close()





if __name__ == '__main__':
    execute()

    print 'Done.'
