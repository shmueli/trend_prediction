from datetime import datetime, timedelta
import sets

import cPickle as pickle
from helpers import constants
import networkx as nx


def load_time_network_pkl(time):
    input_filename = constants.GRAPHS_FOLDER_NAME + 'pkl/' + time    
    reader = open(input_filename, 'r')
    g = pickle.load(reader)
    reader.close()
    
    return g
    

def load_time_network(time, data=False, nodes=None):
    time_str = datetime.strftime(time, constants.GENERAL_DATE_FORMAT)

    print 'Processing: ' + time_str

    if data:
        input_filename = constants.GRAPHS_FOLDER_NAME + time_str
    else:
        input_filename = constants.MIRROR_FOLDER_NAME + time_str
    
    g = nx.DiGraph()
    reader = open(input_filename, 'r')
    for line in reader:
        #line = clean_line(line)
        record = line.strip().replace('"', '').split(',')

        if constants.DATASET=='etoro':            
            if data:
                record[0] = int(float(record[0]))
                record[1] = int(float(record[1]))
                record[2] = datetime.strptime(record[2], '%Y-%m-%dT%H:%M:%SZ')
                record[3] = datetime.strptime(record[3], '%Y-%m-%dT%H:%M:%SZ')
                record[4] = int(float(record[4]))
                record[5] = int(float(record[5]))
                record[6] = int(float(record[6]))
                record[7] = int(float(record[7]))
                record[8] = str(record[8])
                record[9] = str(record[9])
                record[10] = str(record[10])
                record[11] = float(record[11])
                record[12] = float(record[12])
                
                if record[13].find('e')>=0 and len(record[13])>2 and record[13][-2:]=='.0':
                    record[13] = float(record[13][:-2]) 
                else:
                    record[13] = float(record[13]) 
                
                record[14] = float(record[14])
                record[15] = float(record[15])
                record[16] = float(record[16])
                record[17] = float(record[17])
               
                follower = record[1]
                followed = record[7]
    
                if follower==0:
                    print '$$$$$$$$$$ ERROR'
                
                #check with guy why this happens...
                if followed==0 or record[4]==0:
                    followed = follower
                    record[7] = record[1] #parentCID
                    record[4] = record[0] #parentPositionID
                    record[5] = record[0] #origParentPositionID
            else:
                record[0] = int(float(record[0]))
                record[1] = int(float(record[1]))
                #record[2] = datetime.strptime(record[2], '%Y-%m-%dT%H:%M:%SZ')
                #record[3] = datetime.strptime(record[3], '%Y-%m-%dT%H:%M:%SZ')
    
                follower = record[0]
                followed = record[1]
            
                if followed==0 or followed==-1:
                    #0 means that all of the mirrored trades were changed by the user
                    #-1 means that for all of the mirrored trades, we don't have the parent trade in our database
                    
                    g.add_node(follower)
                    continue
                
        elif constants.DATASET=='call':
            if record[3] == 'OUTGOING':
                follower = record[0]
                followed = record[1]
            else:
                follower = record[1]
                followed = record[0]
            
            follower = follower.upper()
            followed = followed.upper()

            if follower[0:2]!='FA' and follower[0:2]!='SP':
                continue 
            if followed[0:2]!='FA' and followed[0:2]!='SP':
                continue 
            

        elif constants.DATASET=='tweeter':
            if len(record)<3:
                continue
            
            follower = record[1]
            follower = extract_tweeter_username(follower)
            followed = record[2]
            followed = extract_tweeter_username(followed)
            
            if follower==None or followed==None:
                continue
            

        g.add_edge(follower, followed)

        if constants.DATASET=='etoro':            
            if data:
                if 'data' not in g.edge[follower][followed]:
                    g.edge[follower][followed]['data'] = []
    
                trade = {
                    'positionID': record[0],
                    'CID': record[1],
                    'openDate': record[2],
                    'closeDate': record[3],                
                    'parentPositionID': record[4],
                    'origParentPositionID': record[5],
                    'mirrorID': record[6],
                    'parentCID': record[7],
                    'buyOrSell': record[8],
                    'buyCurAbbreviation': record[9],
                    'sellCurAbbreviation': record[10],
                    'amount': record[11],
                    'leverage': record[12],
                    'unitsDecimal': record[13],
                    'openRate': record[14],
                    'closeRate': record[15],
                    'spread': record[16],
                    'nProfit': record[17],
                }
                
                if (nodes==None or follower in nodes):
                    g.edge[follower][followed]['data'].append(trade)

    #reader.close()

    #print nx.info(g)
    
    return g


def clean_line(line):
    #handle the amount field which may contain a comma
    r = ''
    last = -1
    open_quote = False
    for i in range(len(line)):
        if line[i]=='"':
            open_quote = not open_quote
        if open_quote and line[i]==',':
            r = r + line[last+1:i]
            last = i
    if last<len(line)-1:
        r = r + line[last+1:]
                
    return r

    
def load_period_network(start, end):
    print 'Processing: ' + 'mirror.csv' + str(start) + str(end)

    input_filename = constants.RAW_DATA_FOLDER_NAME + 'mirror.csv'
    
    g = nx.DiGraph()
    reader = open(input_filename, 'r')
    header = reader.readline().strip().split()
    for line in reader:
        record = line.strip().split(',')

        if constants.DATASET=='etoro':            
            follower = int(float(record[0]))
            followed = int(float(record[1]))
            
            openDate = datetime.strptime(record[3], '%Y-%m-%dT%H:%M:%SZ') + constants.SHIFT
            openDate = openDate.replace(second=0, minute=0, hour=0)
            closeDate = datetime.strptime(record[4], '%Y-%m-%dT%H:%M:%SZ') + constants.SHIFT
            closeDate = closeDate.replace(second=0, minute=0, hour=0)

            if followed==0 or followed==-1:
                continue

        elif constants.DATASET=='call':
            if record[3] == 'OUTGOING':
                follower = record[0]
                followed = record[1]
            else:
                follower = record[1]
                followed = record[0]

            follower = follower.upper()
            followed = followed.upper()

            if follower[0:2]!='FA' and follower[0:2]!='SP':
                continue 
            if followed[0:2]!='FA' and followed[0:2]!='SP':
                continue 

            openDate = datetime.strptime(record[2], '%m/%d/%Y %H:%M') + constants.SHIFT
            openDate = openDate.replace(second=0, minute=0, hour=0)
            closeDate = openDate + timedelta(days=10)

        elif constants.DATASET=='tweeter':
            if len(record)<3:
                continue
            
            follower = record[1]
            follower = extract_tweeter_username(follower)
            followed = record[2]
            followed = extract_tweeter_username(followed)
            
            if follower==None or followed==None:
                continue

            openDate = datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S') + constants.SHIFT
            openDate = openDate.replace(second=0, minute=0, hour=0)
            closeDate = openDate
    
        
        if openDate>end or closeDate<start:
            continue

        g.add_edge(follower, followed)

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
    ranked_nodes = [(g.in_degree(v), v) for v in g.nodes()]
    ranked_nodes.sort(reverse=True)
    ranked_nodes = [e[1] for e in ranked_nodes]
     
    return ranked_nodes


def extract_tweeter_username(s):
    s = s.strip()

    if s==None or s=='':
        return None
    
    end = 0
    while end<len(s) and (s[end].isalpha() or s[end].isdigit() or s[end]=='_'):
        end = end + 1
    
    if end==0:
        return None
    else:
        return s[0:end]
