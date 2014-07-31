from datetime import datetime, timedelta
from helpers import etoro, funf, tweeter
import helpers.constants as constants
import helpers.utils as utils
import networkx as nx



def execute():
    records = etoro.loadFiles()
    store_graphs(records, constants.GRAPHS_FOLDER_NAME)

    #records = funf.loadFiles()
    #store_graphs(records, constants.GRAPHS_FOLDER_NAME)
    
    #records = tweeter.loadFiles()
    #store_graphs(records, constants.GRAPHS_FOLDER_NAME)
    
def store_graphs(records, output_folder):
    utils.ensure_folder(output_folder)

    start = datetime.strptime(constants.START_DATE, constants.GENERAL_DATE_FORMAT)
    end = datetime.strptime(constants.END_DATE, constants.GENERAL_DATE_FORMAT)

    sensitivity = timedelta(seconds=int(constants.SENSITIVITY))
    period = timedelta(seconds=int(constants.PERIOD))

    periodStart = start
    periodEnd = periodStart + period
    
    while periodEnd<=end:
        currentRecords = [r for r in records if r[0]>=periodStart and r[0]<periodEnd]

        store_graph(periodEnd, currentRecords, output_folder)
     
        periodStart = periodStart + sensitivity
        periodEnd = periodEnd + sensitivity


def store_graph(periodEnd, currentRecords, output_folder):
    print 'Handling ' + periodEnd.strftime(constants.GENERAL_DATE_FORMAT)

    g = nx.DiGraph()
    
    for r in currentRecords:
        g.add_edge(r[1], r[2])

    output_filename = output_folder + periodEnd.strftime(constants.GENERAL_DATE_FORMAT)

    #nx.write_gpickle(g, output_filename)  
    nx.write_edgelist(g, output_filename)
    
    #print nx.info(g)


if __name__ == '__main__':
    execute()

    print 'Done.'
