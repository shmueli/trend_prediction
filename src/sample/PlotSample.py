from utils import fit_powerlaw, visualize


def execute():
    #gof_vs_performance()
    concat_changes()
    

def concat_changes():
    concat_added_edges = []
    
    M = visualize.load_results_using_eval('sample_M')[0]
    for m in range(M):
        print m
        
        prev_g_edges = visualize.load_results_using_eval('sample_prev_g_edges_' + str(m))
        added_edges = visualize.load_results_using_eval('sample_added_edges_' + str(m))
        
        added_edges = [float(added_edges[i])/float(prev_g_edges[i]) for i in range(len(prev_g_edges))]
        
        concat_added_edges.extend(added_edges)
       
    print 'visualizing'
    visualize.plot_bins(concat_added_edges, True, True, 'Change', 'Density', 'sample_concat_added_edges')


def gof_vs_performance():
    X1 = []
    X2 = []
    Y = []
    M = visualize.load_results_using_eval('sample_M')[0]
    for m in range(M):
        p, gof, performance = calc_sample_gof(m)
        
        X1.append(p)
        X2.append(gof)
        Y.append(performance)
        
    visualize.plot_values(X1, Y, 'ps', 'performance', 'sample_ps')
    visualize.plot_values(X2, Y, 'gof', 'performance', 'sample_gofs')


def calc_sample_gof(m):
    prev_g_edges = visualize.load_results_using_eval('sample_prev_g_edges_' + str(m))
    added_edges = visualize.load_results_using_eval('sample_added_edges_' + str(m))
    performance = visualize.load_results_using_eval('sample_performance_' + str(m))[0]
    
    added_edges = [float(added_edges[i])/float(prev_g_edges[i]) for i in range(len(prev_g_edges))]

    visualize.plot_bins(added_edges, True, True, 'Change', 'Density', 'sample_' + str(m))

    X1, Y1, X2, Y2, xmin, alpha = fit_powerlaw.fit_data(added_edges)
    p, gof = fit_powerlaw.calc_gof(added_edges, xmin)
    
    print m, xmin, alpha, p, gof, performance
    
    return p, gof, performance


#####################################################################################
### main
#####################################################################################

if __name__ == '__main__':
    execute()

    print 'Done.'
