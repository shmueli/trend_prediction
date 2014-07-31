import sets
import os
import cPickle as pickle

_input_folder = '/spyder_workspace/trend_prediction/data/BT/'
_output_folder = '/spyder_workspace/trend_prediction/out/BT/'

def loadFiles():
    ensure_folder(_output_folder)
    
    filenames = os.listdir(_input_folder)
    filenames.sort()
    for filename in filenames:
        if not filename.startswith('HIDDEN'):
            continue
        
        print 'Loading ' + filename
        processFile(filename)
            

def processFile(filename):
    input_filename = _input_folder + filename

    adj = {}
    
    reader = open(input_filename, 'r')
    for line in reader:
        line = line.strip()
        fields = line.split(' ')        

        v1 = fields[0]
        v2 = fields[1]

        if v1 not in adj:
            adj[v1] = sets.Set()
            
        adj[v1].add(v2)
        
    for v1 in adj:
        adj[v1] = len(adj[v1])
    
    reader.close()
        
    output_filename = _output_folder + filename
    writer = open(output_filename, 'w')
    pickle.dump(adj, writer)
    writer.close()
    

def ensure_folder(folder_name):
    d = os.path.dirname(folder_name)
    if not os.path.exists(d):
        os.makedirs(d)


if __name__ == '__main__':
    loadFiles()

    print 'Done.'