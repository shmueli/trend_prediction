import helpers.constants as constants
import numpy
import fit_powerlaw
import datetime
#from bson import ObjectId

import matplotlib 
matplotlib.use('Agg') 
import pylab


def write_results(data, varname):
    output_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + varname

    writer = open(output_filename, 'w')
    writer.write('[')
    for i in range(len(data)):
        v = data[i]
        writer.write(str(v))
        if i!=len(data)-1:
            writer.write(', ')            
    writer.write(']')
    writer.close()


def load_results(varname):
    input_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + varname

    reader = open(input_filename, 'r')
    line = reader.readline()
    line = line.replace('\'', '')
    values = line[1:-1].split(', ')
    if varname.find('times')>=0:
        data = [v for v in values]
    else:
        data = [float(v) for v in values]
    reader.close()
    
    return data


def write_results_using_str(data, varname):
    input_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + varname
    writer = open(input_filename, 'w')

    line = str(data)
    
    writer.write(line)
    
    writer.close()


def load_results_using_eval(varname):
    input_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + varname
    reader = open(input_filename, 'r')
    line = reader.readline()

    data = eval(line)

    reader.close()
        
    return data


def plot_changes(filtered_times, data, suffix, onlyBins, xmin=None):
    print suffix
    
    '''
    if constants.DATASET=='bt':
        temp = data
        data = []
        data.extend(temp[0:53])
        data.extend(temp[75:])
    '''
    
    #fromconstant = (constants.DATASET!='etoro')
    fromconstant = False
    loglog = True
    
    '''
    X = range(len(data))
    Y1 = data
    
    fit = pylab.polyfit(X, Y1, 1)
    fit_fn = pylab.poly1d(fit)
    Y2 = fit_fn(X)
    
    data = [Y1[i]/Y2[i] for i in range(len(X))]
    '''

    if fromconstant:
        const = float(numpy.mean(data))
        #data = [numpy.abs(s-const) for s in data]
        data = [max(s, const)-min(s, const) for s in data]

    #print data
    
    if not onlyBins:
        plot_values_with_day_color(filtered_times, data, 'Day', 'Change', suffix)
    
        data = sorted(data, reverse=True)
        plot_values(range(len(data)), data, 'Day', 'Change', suffix + '_sorted')
    
    plot_bins(data, loglog, True, 'Change', 'Density', suffix + '_log_bins', xminPlot=xmin)


def plot_values(X, Y, xlabel, ylabel, output_filename):
    pylab.figure(figsize=(15, 10))

    pylab.rcParams.update({'font.size': 30})

    pylab.scatter(X, Y)

    #pylab.yscale('log')
    pylab.axis(get_bounds(X, Y, False, False))

    #pylab.axis(get_bounds(X, Y, False))
    
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)   

    pylab.tight_layout()

    pylab.savefig(output_filename + '.pdf')


def plot_values_with_day_color(days, Y, xlabel, ylabel, suffix):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    output_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + suffix

    X = range(len(days))
    Xi = []
    Yi = []
    for i in range(7):
        Xi.append([])
        Yi.append([])
        
    for j in range(len(days)):
        time_str = days[j]
        time = datetime.datetime.strptime(time_str, '%Y%m%d%H%M%S')
        
        i = time.weekday()
        Xi[i].append(X[j])
        Yi[i].append(Y[j])
    
    pylab.figure(figsize=(7.5, 7))

    pylab.rcParams.update({'font.size': 20})

    for i in range(7):
        pylab.scatter(Xi[i], Yi[i], color=colors[i])

    #pylab.yscale('log')
    pylab.axis(get_bounds(X, Y, False, False))

    #pylab.axis(get_bounds(X, Y, False))
    
    pylab.xlabel(xlabel)
    if constants.DATASET=='etoro':
        pylab.ylabel(ylabel)   

    pylab.tight_layout()

    pylab.savefig(output_filename + '.pdf')


def plot_values_side_by_side(X, Y1, Y2, xlabel, ylabel, suffix):
    output_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + suffix

    #'''
    X = X[:-1]
    Y1 = Y1[:-1]
    Y2 = [Y2[i+1]-Y2[i] for i in range(len(Y2)-1)]
    #'''
    
    Y1 = numpy.abs(Y1)
    Y2 = numpy.abs(Y2)

    Y1 = [float(y)/float(max(Y1)) for y in Y1]
    Y2 = [float(y)/float(max(Y2)) for y in Y2]
    
    '''
    Y1 = sorted(Y1)
    Y2 = sorted(Y2)
    '''
    
    
    pylab.figure(figsize=(7.5, 7))

    pylab.rcParams.update({'font.size': 20})

    '''
    pylab.scatter(X, Y1, c='r')
    pylab.scatter(X, Y2, c='b')
    pylab.axis(get_bounds(X, Y1+Y2, False, False))
    '''
    
    pylab.scatter(Y1, Y2, c='b')
    pylab.axis(get_bounds(Y1, Y2, False, False))
    

    #pylab.axis(get_bounds(X, Y, False))
    
    pylab.xlabel(xlabel)
    if constants.DATASET=='etoro':
        pylab.ylabel(ylabel)   

    pylab.tight_layout()

    pylab.savefig(output_filename + '.pdf')
    

def plot_bins(Y, loglog, logbins, xlabel, ylabel, suffix, xminPlot=None):
    output_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + suffix


    X1Temp, Y1Temp, X2Temp, Y2Temp, xmin, alpha = fit_powerlaw.fit_data(Y, discrete=False, pdf=False, original_data=True, xmin=None)
    X1, Y1, X2, Y2, xminPlot, alphaPlot = fit_powerlaw.fit_data(Y, discrete=False, pdf=True, original_data=False, xmin=None)

    
    
    pylab.figure(figsize=(7.5, 7))
    
    pylab.rcParams.update({'font.size': 20})

    pylab.scatter(X1, Y1)

    pylab.plot(X2, Y2, '--')

    bounds = get_bounds(X1, Y1, loglog, loglog)

    if loglog:
        pylab.xscale('log', basex=2)
        pylab.yscale('log')
        xtext = numpy.exp(numpy.log(bounds[0])+(numpy.log(bounds[1])-numpy.log(bounds[0]))*0.65)
        ytext = numpy.exp(numpy.log(bounds[2])+(numpy.log(bounds[3])-numpy.log(bounds[2]))*0.65)
    else:
        xtext = (bounds[0]+bounds[1])/2.0
        ytext = (bounds[2]+bounds[3])/2.0

    pylab.axis(bounds)

    pylab.text(xtext, ytext, '$gamma$='+'{0:.2f}'.format(alpha))
    
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)

    pylab.tight_layout()

    pylab.savefig(output_filename + '.pdf')


def get_bounds(X, Y, logx, logy):
    if logx:
        minX = min(X) / 1.5           
        maxX = max(X) * 1.5
    else:
        marginX = float(max(X) - min(X))/10.0
        minX = min(X) - marginX
        maxX = max(X) + marginX

    if logy:
        minY = min(Y) / 2.0
        maxY = max(Y) * 2.0
    else:
        marginY = float(max(Y) - min(Y))/10.0
        minY = min(Y) - marginY
        maxY = max(Y) + marginY
        
    return [minX, maxX, minY, maxY]
