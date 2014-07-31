import matplotlib
matplotlib.use('Agg')

import numpy
import pylab

from utils import visualize as vis
from utils import fit_powerlaw


from helpers import constants


def execute():
    data = load_results_using_eval()
    plot_attractiveness(data)
    


def load_results_using_eval():
    input_filename = constants.ATTRACTIVENESS_FOLDER_NAME + 'etoro_attractiveness_dist_list'

    reader = open(input_filename, 'r')
    line = reader.readline()

    data = eval(line)

    reader.close()
    
    return data


def plot_attractiveness(data):
    loglog = True
    
    X1, Y1, X2, Y2, xmin, alpha = fit_powerlaw.fit_data(data, discrete=True, original_data=False, xmin=2)
    
    
    output_filename = constants.ATTRACTIVENESS_FOLDER_NAME + 'attractiveness'

    pylab.figure(figsize=(7.5, 7))
    pylab.rcParams.update({'font.size': 20})

    pylab.scatter(X1, Y1)
    
    pylab.plot(X2, Y2, '--')
    
    bounds = vis.get_bounds(X1, Y1, loglog, loglog)
    
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
