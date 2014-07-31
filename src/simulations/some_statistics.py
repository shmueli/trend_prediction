from datetime import datetime, timedelta

import pylab

import helpers.constants as constants
from utils import visualize

from graphs import load_graphs


def execute():
    #test_mirror_period_lengths()
    
    test_out_degree()


def test_mirror_period_lengths():
    data = []
    
    input_filename = constants.RAW_DATA_FOLDER_NAME + 'mirror.csv'
    
    reader = open(input_filename, 'r')
    header = reader.readline().strip().split()
    i = 0
    for line in reader:
        fields = line.strip().split(',')

        CID = int(float(fields[0]))
        parentCID = int(float(fields[1]))
        
        openDate = datetime.strptime(fields[2], '%Y-%m-%dT%H:%M:%SZ')
        closeDate = datetime.strptime(fields[3], '%Y-%m-%dT%H:%M:%SZ')
    
        if parentCID==0:
            continue

        seconds = (closeDate - openDate).total_seconds()

        data.append(seconds)
        
        if i==10000:
            break
        i = i + 1
        
    reader.close()
    
    print 'plotting'


    #pylab.hist(data)
    #pylab.show()
    
    visualize.plot_bins(data, True, True, 'length', 'density', 'temp')

    
    #data.sort(reverse=True)
    #visualize.plot_values(range(len(data)), data, 'sorted degrees', 'degree', 'temp')



def test_out_degree():
    start = datetime.strptime('20110701000000', constants.GENERAL_DATE_FORMAT)
    end = datetime.strptime('20120101000000', constants.GENERAL_DATE_FORMAT)

    data = []
    
    time = start
    while time<end:
        g = load_graphs.load_time_network(time)
        
        print 'plotting'
    
        daily_data = [g.out_degree(v) for v in g.node]
        
        data.extend(daily_data)
        
        time = time + timedelta(days=1)
    
    pylab.hist(data)
    pylab.show()
    
    
    
    
if __name__ == '__main__':
    execute()
     
    print 'Done.'

