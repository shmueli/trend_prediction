import numpy
import pylab

from graphs import load_graphs
from helpers import constants
from utils import visualize, fit_powerlaw

import json

def execute():
    for p in constants.PERIODS:
        calc_degree_distribution(constants.PERIODS[p]['start'], constants.PERIODS[p]['end'], p)
        plot_degree_distribution(p)


def calc_degree_distribution(start, end, p):
    g = load_graphs.load_period_network(start, end)

    degrees = [g.in_degree(v) for v in g.node]
    degrees = sorted(degrees)
    
    output_filename = constants.STATS_FOLDER_NAME + 'degree_distribution' + '_' + str(p)
    
    json.dump(degrees, open(output_filename, 'w'))


def plot_degree_distribution(p):
    input_filename = constants.STATS_FOLDER_NAME + 'degree_distribution' + '_' + str(p)

    degrees = json.load(open(input_filename, 'r'))



    output_filename = constants.STATS_FOLDER_NAME + 'degree_distribution' + '_' + str(p)

    loglog = True

    X1, Y1, X2, Y2, xmin, alpha = fit_powerlaw.fit_data(degrees, discrete=True, original_data=False, xmin=2)
        
    pylab.figure(figsize=(15, 10))
    pylab.rcParams.update({'font.size': 30})

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
