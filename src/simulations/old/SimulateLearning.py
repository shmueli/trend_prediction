import sets
import random
import networkx as nx
import pylab
import numpy
import powerlaw


def update_p(p_true, observation, cp):
    p = p_true if observation==True else 1.0-p_true
     
    new_p = (p*cp) / ((1.0-p)*(1.0-cp) + p*cp)
    new_p = new_p if observation==True else 1.0-new_p
    
    #print 'p_true:', p_true, 'state:', state, 'new_p:', new_p

    return new_p


def update_state(p_true, sigma):
    if p_true > sigma:
        new_state = True
    else:
        if p_true < 1.0-sigma:
            new_state = False
        else:
            new_state = None
    
    return new_state

def plot_bins(Y, loglog, logbins, suffix):
    X1, Y1, X2, Y2, alpha = fit_data(Y, True, pdf=True)      

    
    
    pylab.figure(figsize=(7.5, 7))
    
    pylab.rcParams.update({'font.size': 20})

    pylab.scatter(X1, Y1)

    pylab.plot(X2, Y2, '--')

    bounds = get_bounds(X1, Y1, loglog, loglog)

    if loglog:
        pylab.xscale('log')
        pylab.yscale('log')
        xtext = numpy.exp(numpy.log(bounds[0])+(numpy.log(bounds[1])-numpy.log(bounds[0]))*0.65)
        ytext = numpy.exp(numpy.log(bounds[2])+(numpy.log(bounds[3])-numpy.log(bounds[2]))*0.65)
    else:
        xtext = (bounds[0]+bounds[1])/2.0
        ytext = (bounds[2]+bounds[3])/2.0

    pylab.axis(bounds)

    pylab.text(xtext, ytext, '$gamma$='+'{0:.2f}'.format(alpha))
    
    pylab.xlabel('Change')
    pylab.ylabel('Density')

    pylab.tight_layout()

    pylab.show()


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


def fit_data(Y, discrete, pdf=True):
    Y = [y for y in Y if y>0]

    print len(Y)

    fit = powerlaw.Fit(Y, discrete=discrete)
    alpha = fit.alpha
    xmin = fit.xmin
    print 'alpha:', alpha, 'xmin:', xmin

    if pdf:
        X1, Y1 = fit.pdf(original_data=True)
    else:
        X1, Y1 = fit.ccdf(original_data=True)
    X1 = [X1[i] for i in range(len(Y1)) if Y1[i]>0]
    Y1 = [Y1[i] for i in range(len(Y1)) if Y1[i]>0]

    pl = powerlaw.Power_Law(
        xmin = fit.xmin,
        xmax = fit.xmax,
        discrete = fit.discrete,
        estimate_discrete = fit.estimate_discrete,
        fit_method = fit.fit_method,
        data = fit.data,
        parameter_range = fit.parameter_range,
        parent_Fit = fit
    )
    X2 = sorted(numpy.unique(X1))
    if pdf:
        Y2 = pl.pdf(data=X2)
    else:
        Y2 = pl.ccdf(data=X2)
    X2 = X2[-len(Y2):]

    
    '''
    [p, gof] = plpva.plpva(Y, xmin, 'reps', 100)
    print 'p:', p
    '''
    
    '''
    R, p = fit.distribution_compare('power_law', 'truncated_power_law', normalized_ratio=True)
    print 'power_law > truncated_power_law', R, p
    R, p = fit.distribution_compare('power_law', 'exponential', normalized_ratio=True)
    print 'power_law > exponential', R, p
    R, p = fit.distribution_compare('power_law', 'lognormal', normalized_ratio=True)
    print 'power_law > lognormal', R, p
    R, p = fit.distribution_compare('truncated_power_law', 'exponential', normalized_ratio=True)
    print 'truncated_power_law > exponential', R, p
    R, p = fit.distribution_compare('truncated_power_law', 'lognormal', normalized_ratio=True)
    print 'truncated_power_law > lognormal', R, p
    '''


    
    '''
    results = plfit.plfit(popularities)
    alpha = results[0]
    xmin = results[1]
    print 'alpha:', alpha, 'xmin:', xmin
    '''

    '''
    results = plfit2.plfit(popularities, discrete=True, quiet=False, verbose=True)
    results.plotpdf()
    pylab.show()
    return
    '''
    
    '''
    X, Y1, Y2, fit = data_into_bins(popularities, 100, loglog, True)
    '''


    return X1, Y1, X2, Y2, alpha


def calcR(conclusions, b):
    R = []
    for v in conclusions:
        v_conclusions = conclusions[v]
        if len(v_conclusions) == 0:
            continue
        
        r = float(v_conclusions.count(b)) / float(len(v_conclusions))
        R.append(r)
    
    if len(R)==0:
        return 0
    
    R = numpy.mean(R)
    return R


def simulate():
    avalanches = []
    conclusions = {}
    
    D = 8
    A = 1000
    b = True
    S = A/20
    r = 0.55
    sigma = 0.8
    #cp = 0.63
    cp = 0.55
    n = int(0.8 * float(A))
    
    
    #create network
    p = float(D) / float(A)
    g = nx.erdos_renyi_graph(A, p)
    nodes = g.nodes()
    
    for v in nodes:
        g.node[v]['P'] = 0.5
        g.node[v]['state'] = None
        conclusions[v] = []
        
    sensors = ['s'+str(i) for i in range(S)]
    for i in range(S):
        g.add_edge(nodes[i], sensors[i])
        
    #print nx.info(g)
    
    #simulate
    for i in range(1000):
        print '### Iteration:', i
        
        changed = sets.Set()
        
        communicating = sets.Set()
        cascade_communicating = sets.Set()
        
        s = sensors[random.randint(0, len(sensors)-1)]
        g.node[s]['state'] = True if random.random()<r else False
        communicating.add(s)
    
        for v in nodes:
            if g.node[v]['state']!=None:
                communicating.add(v)
                conclusions[v].append(g.node[v]['state'])
    
        while len(communicating)>0:          
            new_states = {}
            for v in nodes:
                n_v = sets.Set(g.neighbors(v))
                n_v.intersection_update(communicating)
                
                for u in n_v:
                    g.node[v]['P'] = update_p(g.node[v]['P'], g.node[u]['state'], cp)
    
                new_states[v] = update_state(g.node[v]['P'], sigma)
                if g.node[v]['state']!=new_states[v] and new_states[v]!=None:
                    cascade_communicating.add(v)
                    changed.add(v)
        
            for v in new_states:
                g.node[v]['state'] = new_states[v]
                
            communicating = cascade_communicating
            cascade_communicating = sets.Set()
    
               
        cnt_true = 0
        cnt_false = 0
        for v in nodes:
            if g.node[v]['state']==True:
                cnt_true = cnt_true + 1
            if g.node[v]['state']==False:
                cnt_false = cnt_false + 1
    
        #probs = [g.node[nodes[i]]['P'] for i in range(S)]
        #print probs
                        
        print cnt_true, cnt_false
        print len(changed)
    
        avalanches.append(len(changed))
        
        if cnt_true>n or cnt_false>n:
            break

    R = calcR(conclusions, b)
    
    return R, avalanches



avalanches = []
R = []
for i in range(100):
    iR, iavalanches = simulate() 
    avalanches.extend(iavalanches)
    R.append(iR)
    print '#############################', numpy.mean(R)
R = numpy.mean(R)

 
print R   
plot_bins(avalanches, True, True, '')