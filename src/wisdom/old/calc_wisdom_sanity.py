from utils import visualize


def execute():
    top = [1, 2, 5, 10, 20, 50, 100, 200, 500]
    
    performance = []
    for t in range(len(top)):
        temp = visualize.load_results_using_eval('top_performance_' + str(top[t]))
        performance.append(temp)
        sanity(performance, t)

    ind_performance = []
    for t in range(len(top)):
        temp = visualize.load_results_using_eval('ind_top_performance_' + str(top[t]))
        ind_performance.append(temp)
        sanity(ind_performance, t)




def sanity(performance, i):
    pos = 1.0
    poscnt = 0
    possum = 0
    neg = 1.0
    negcnt = 0
    negsum = 0
    zerocnt = 0
    for p in performance[i]:
        if p>0:
            pos = pos * (1.0+p)
            poscnt = poscnt + 1
            possum = possum + p
        elif p<0:
            neg = neg * (1.0+p)
            negcnt = negcnt + 1
            negsum = negsum + p
        else:
            zerocnt = zerocnt + 1
            
    print i, pos, neg, pos*neg, poscnt, negcnt, zerocnt, possum/poscnt, negsum/negcnt


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
