from datetime import timedelta
import networkx as nx
import sets
import pymongo


shift = timedelta(seconds=int(150*60))


db = None


def init_connection():
    connection_string = "mongodb://localhost"
    
    connection = pymongo.MongoClient(connection_string)
  
    global db  
    db = connection.trades
    

def get_db():
    return db


def load_time_network(time, data=False, filterQ=None):
    start = time
    end = start + timedelta(days=1)
    
    return load_times_network(start, end, data, filterQ)



def load_times_network(start, end, data=False, filterQ=None):
    print 'Processing:', start, end

    start = start - shift
    end = end - shift
        
    query = {'openDate': {'$lt': end}, '$or': [{'closeDate': None}, {'closeDate': {'$gte': start}}]}
    if filterQ!=None:
        query.update(filterQ)
    
    if data==False: 
        trades = db.mirror.find(query)
    else:
        trades = db.trades.find(query).hint([('openDate', pymongo.ASCENDING)])
    
    g = nx.DiGraph()
    for t in trades:
        #print 'aaa'
         
        follower = int(t['CID'])
        followed = int(t['parentCID'])

        if follower==0 or followed==0:
            #print line
            continue
        
        if data==False and ('mirrorID' not in t or t['mirrorID']==0):
            continue
        
        g.add_edge(follower, followed)
        if data:
            if 'data' not in g.edge[follower][followed]:
                g.edge[follower][followed]['data'] = []
            g.edge[follower][followed]['data'].append(t)
            
        #print 'bbb'

    print 'Finished processing:', start.weekday(), g.number_of_nodes(), g.number_of_edges()

    return g


def load_period_network(start, end, data=False, filterQ=None):
    return load_times_network(start, end, data, filterQ)


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
    ranked_nodes.sort()
    ranked_nodes = [e[1] for e in ranked_nodes]
     
    return ranked_nodes
