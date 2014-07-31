from datetime import datetime, timedelta
import math
import sets

import numpy
import pylab

from graphs import load_graphs
from helpers import constants
from utils import visualize, fit_powerlaw


def execute():
    if constants.DATASET=='etoro':
        #snapshot_times = ['20111001000000', '20120401000000', '20121001000000']
        snapshot_times = ['20110701000000', '20120101000000', '20120701000000', '20130101000000']
        plot_snapshot_evolution(snapshot_times, 90, 50)
        
        #snapshot_times = ['20110701000000', '20111001000000', '20120101000000', '20120401000000', '20120701000000', '20121001000000', '20130101000000', '20130401000000']
        snapshot_times = ['20110701000000', '20120101000000', '20120701000000', '20130101000000']
        plot_snapshot_degrees(snapshot_times, 90)

        start = datetime.strptime('20110701000000', constants.GENERAL_DATE_FORMAT)
        end = datetime.strptime('20130701000000', constants.GENERAL_DATE_FORMAT)
        plot_whole_network_degrees(start, end)


#####################################################################################
### part 2
#####################################################################################

def plot_snapshot_evolution(times, period, threshold):
    gs = []
    for time in times:
        start = datetime.strptime(time, constants.GENERAL_DATE_FORMAT)
        end = start + timedelta(days=period)
        g = load_graphs.load_period_network(start, end)
        gs.append(g)
    

    all_top_nodes = sets.Set()
    for g in gs:
        top_nodes = load_graphs.rank_network_nodes(g)
        top_nodes = top_nodes[-threshold:]
        all_top_nodes.union_update(top_nodes)    
    all_top_nodes = [v for v in all_top_nodes]
    
    
    sqrt_size = int( math.ceil( math.sqrt( len(all_top_nodes) ) ) )
    
    
    prev_top_nodes = None
    prev_g = None

    subplot_id = 1
    for i in range(len(times)):
        time = times[i]
        g = gs[i]
        
        top_nodes = load_graphs.rank_network_nodes(g)
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
                    size = prev_g.in_degree(v)
                else:
                    to_change = ignored
                    size = 1
            else:
                if prev_top_nodes==None or v in prev_top_nodes:
                    to_change = remained
                    size = g.in_degree(v)
                else:
                    to_change = added
                    size = g.in_degree(v)

            x = i%sqrt_size
            y = sqrt_size - 1 - i/sqrt_size
                      
            to_change[0].append(x)
            to_change[1].append(y)
            to_change[2].append(size)

    
        
        output_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + str(time) + '_snapshot_evolution'

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
        

def plot_snapshot_degrees(snapshot_times, period):
    loglog = True
    

    subplot_id = 1
    for time in snapshot_times:
        start = datetime.strptime(time, constants.GENERAL_DATE_FORMAT)
        end = start + timedelta(days=period)
        g = load_graphs.load_period_network(start, end)
        
        
        degrees = [g.in_degree(v) for v in g.node]       
        degrees = sorted(degrees)
        
        
        visualize.write_results(degrees, time + '_snapshot_degrees')

               
        X1, Y1, X2, Y2, xmin, alpha = fit_powerlaw.fit_data(degrees, discrete=True, original_data=False, xmin=2)      
  
   
        output_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + str(time) + '_snapshot_degrees'

        pylab.figure(figsize=(7.5, 7))
        pylab.rcParams.update({'font.size': 20})
    
        pylab.scatter(X1, Y1)
    
        pylab.plot(X2, Y2, '--')
    
        bounds = visualize.get_bounds(X1, Y1, loglog, loglog)

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


def plot_whole_network_degrees(start, end):
    loglog = True


    g = load_graphs.load_period_network(start, end)


    degrees = [g.in_degree(v) for v in g.node]
    degrees = sorted(degrees)
    
    
    visualize.write_results(degrees, '_whole_network_degrees')
    

    X1, Y1, X2, Y2, xmin, alpha = fit_powerlaw.fit_data(degrees, discrete=True, original_data=False, xmin=2)
    
    
    output_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + 'whole_network_degrees'

    pylab.figure(figsize=(7.5, 7))
    pylab.rcParams.update({'font.size': 20})

    pylab.scatter(X1, Y1)
    
    pylab.plot(X2, Y2, '--')
    
    bounds = visualize.get_bounds(X1, Y1, loglog, loglog)
    
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
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
