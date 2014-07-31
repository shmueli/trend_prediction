#this module tries to predict the changes in currency

from datetime import datetime, timedelta
import sets

import daily_currency_rates5
from graphs import load_graphs
import helpers.constants as constants
from utils import visualize


def execute():
    daily_currency_rates5.load()
    
    #'''
    start = datetime.strptime('20110701000000', constants.GENERAL_DATE_FORMAT)
    end = datetime.strptime('20111001000000', constants.GENERAL_DATE_FORMAT)
    predict_daily_currency_pair(start, end, '1')
    #'''

    '''
    start = datetime.strptime('20120101000000', constants.GENERAL_DATE_FORMAT)
    end = datetime.strptime('20120701000000', constants.GENERAL_DATE_FORMAT)
    predict_daily_currency_pair(start, end, '2')
    '''

    '''
    start = datetime.strptime('20120701000000', constants.GENERAL_DATE_FORMAT)
    end = datetime.strptime('20130101000000', constants.GENERAL_DATE_FORMAT)
    predict_daily_currency_pair(start, end, '3')
    '''

    '''
    start = datetime.strptime('20130101000000', constants.GENERAL_DATE_FORMAT)
    end = datetime.strptime('20130701000000', constants.GENERAL_DATE_FORMAT)
    predict_daily_currency_pair(start, end, '4')
    '''

def predict_daily_currency_pair(start, end, suffix):
    top = [1, 2, 5, 10, 20, 50, 100, 200, 500, 2000]
    ind = [0, 1, 2, -1]
    
    curr1 = 'EUR'
    curr2 = 'USD'
    
    num_nodes = max(top)
    
    ground_truth = []

    prediction = {}
    confidence = {}
    performance = {}
    for i in ind:
        prediction[i] = []
        confidence[i] = []
        performance[i] = []

        for t in range(len(top)):
            prediction[i].append([])
            confidence[i].append([])
            performance[i].append(0)

    period = 0

    time = start
    while time<end:
        #we look at the network today but start investing tomorrow - that's why 4 and 5 means Saturday and Sunday (instead of Friday and Saturday)
        if time.weekday()!=5 and time.weekday()!=6:
            #time_str = datetime.strftime(time, constants.GENERAL_DATE_FORMAT)
            
            g_edges = load_graphs.load_time_network(time, data=False)
    
    
            top_nodes = rank_network_nodes(g_edges)
            top_nodes = top_nodes[-num_nodes:]
            
            g_trades = load_graphs.load_time_network(time, data=True, nodes=top_nodes)
    
            gt = ground_truth_currency_pair(time, curr1, curr2)
            ground_truth.append(gt)

            if gt!=None:
                for t in range(len(top)):
                    for i in ind:            
                        ind_top_nodes = calc_independent_nodes(g_edges, top_nodes[-top[t]:], i)
    
                        group_prediction = predict_daily_currency_pair_like_group(g_trades, ind_top_nodes, time, start, end, curr1, curr2)
    
                        if group_prediction!=None:
                            performance[i][t] = performance[i][t] + group_prediction[gt]
                            
                        print i, top[t], group_prediction, gt
                 
                period = period + 1
             
        time = time + timedelta(days=1)



    for t in range(len(top)):    
        for i in ind:    
            print top[t], i, (performance[i][t]/period), period


    visualize.write_results_using_str(ground_truth, 'ground_truth_' + suffix)

    visualize.write_results_using_str(prediction, 'top_prediction_' + suffix)
    visualize.write_results_using_str(confidence, 'top_confidence_' + suffix)
    visualize.write_results_using_str(performance, 'top_performance_' + suffix)


def ground_truth_currency_pair(time, curr1, curr2):

    open_time = time
    close_time = tomorrow(time)
    #while close_time.weekday()==5 or close_time.weekday()==6:
    #    close_time = tomorrow(close_time)
    
    open_rate = daily_currency_rates5.get_rate(curr1, curr2, open_time, accuracy=timedelta(hours=1)) #todo
    close_rate = daily_currency_rates5.get_rate(curr1, curr2, close_time, accuracy=timedelta(hours=1)) #todo
    
    if open_rate==None or close_rate==None:
        return None

    if open_rate<=close_rate:
        return 'Buy'
    else:
        return 'Sell'


def predict_daily_currency_pair_like_group(g, top_nodes, time, start, end, curr1, curr2):
    prediction = {'Sell': 0, 'Buy': 0}
    
    sumAll = 0
    for i in range(len(top_nodes)):
        v = top_nodes[i]

        ind_prediction = predict_daily_currency_pair_like_individual(g, v, time, start, end, curr1, curr2)
    
        if ind_prediction!=None:    
            for p in ind_prediction:
                prediction[p] = prediction[p] + ind_prediction[p]
                
            sumAll = sumAll + 1
        

    if sumAll>0:
        for p in prediction:
            prediction[p] = float(prediction[p])/float(sumAll)                  
        return prediction;
    else:
        return None


def predict_daily_currency_pair_like_individual(g, v, time, start, end, curr1, curr2):

    prediction = {'Sell': 0, 'Buy': 0}

    sumAll = 0
    if g.has_node(v):
        for e in g.out_edges(v, data=True):
            for t in e[2]['data']:
                if t['buyCurAbbreviation']==curr1 and t['sellCurAbbreviation']==curr2:
                    p = t['buyOrSell']
                    units = t['unitsDecimal']

                    prediction[p] = prediction[p] + units
                    
                    sumAll = sumAll + units
    

    if sumAll>0:    
        for p in prediction:
            prediction[p] = float(prediction[p])/float(sumAll)       
        return prediction;
    else:
        return None


def tomorrow(time):
    tomorrow = datetime(time.year, time.month, time.day) + timedelta(days=1)
    return tomorrow


def period_length(start, end):
    period = (end - start).days + 1

    return period


def oppP(p):
    if p=='Sell':
        return 'Buy'
    elif p=='Buy':
        return 'Sell'
    else:
        return None
    

def rank_network_nodes(g):
    ranked_nodes = [(real_in_degree(g, v), v) for v in g.nodes()]
    ranked_nodes.sort()
    ranked_nodes = [e[1] for e in ranked_nodes]
     
    return ranked_nodes


def real_out_degree(g, v):
    d = g.out_degree(v) if g.has_node(v) else 0;
         
    return d


def real_in_degree(g, v):
    d = g.in_degree(v) if g.has_node(v) else 0;
     
    return d


def calc_overall_performance(top, performance):
    overall = {}
    for i in range(len(top)):
        o = 1.0
        for p in performance[i]:
            o = o * (1.0 + p)
        overall[top[i]] = o
    return overall


def calc_independent_nodes(g, top_nodes, hops):
    independent_nodes = [top_nodes[-1]]
    
    for i in range(2, len(top_nodes)+1):
        v = top_nodes[-i]
        if independent(g, independent_nodes, v, hops):
            independent_nodes.insert(0, v)
    
    return independent_nodes


def independent(g, nodes, v, hops):

    r = reachable(g, v, 'out', hops)
    r.union_update( reachable(g, v, 'in', hops) )
    
    r.intersection_update(nodes)
    
    return len(r)==0


def reachable(g, v, direction, hops):
    
    visited = sets.Set()
    visited.add(v)   
    visiting = [(v, 0)]
    while len(visiting)>0:
        first = visiting[0]
        visiting.remove(first)
        v1 = first[0]
        cur_hops = first[1]

        if cur_hops==hops:
            break

        if direction=='out':
            edges = g.out_edges(v1)
        else:
            edges = g.in_edges(v1)
           
        for e in edges:
            if direction=='out':
                v2 = e[1]
            else:
                v2 = e[0]
            
            if v2 not in visited:
                visited.add(v2)
                visiting.append((v2, cur_hops+1))

    return visited



#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
