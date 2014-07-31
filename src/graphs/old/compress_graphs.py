import helpers.constants as constants
import times
import networkx as nx
import cPickle as pickle

output_folder = constants.GRAPHS_FOLDER_NAME

def execute():
    all_times = times.get_times()
    for time in all_times:
        compress_time_network(time)
        
        
def compress_time_network(time):
    print 'Processing: ' + time

    input_filename = constants.GRAPHS_FOLDER_NAME + time
    
    g = nx.DiGraph()
    reader = open(input_filename, 'r')
    for line in reader:
        line = line.strip()
        
        fields = line.split('\t')
        
        if len(fields)<2:
            #print line
            continue;
        
        follower = fields[0]
        followed = fields[1]
        
        if follower=='0' or followed=='0':
            #print line
            continue
        
        g.add_edge(follower, followed)
        if 'data' not in g.edge[follower][followed]:
            g.edge[follower][followed]['data'] = []
        g.edge[follower][followed]['data'].append(fields[2:])

    reader.close()
    
    
    output_filename = constants.GRAPHS_FOLDER_NAME + 'pkl/' + time
    writer = open(output_filename, 'w')
    pickle.dump(g, writer)
    writer.close()


if __name__ == '__main__':
    execute()

    print 'Done.'
