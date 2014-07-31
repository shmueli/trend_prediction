'''
Created on May 9, 2014

@author: Erez
'''

def plot_data_with_error_bars(data, top, repeats, with_replace, ylabel, suffix):
    output_filename = constants.CHARTS_FOLDER_NAME + constants.DATASET + '_' + suffix

    pylab.figure(figsize=(15, 10))
    
    pylab.rcParams.update({'font.size': 30})


    pylab.plot(top, aggregate_repeats(data, top, repeats, False, 0), linewidth=2, color="red", marker='o', markersize=15, markeredgecolor="red", markerfacecolor="white")
    pylab.plot(top, aggregate_repeats(data, top, repeats, False, 1), linewidth=2, color="blue", marker='o', markersize=15, markeredgecolor="black", markerfacecolor="white")
    pylab.plot(top, aggregate_repeats(data, top, repeats, False, -1), linewidth=2, color="green", marker='o', markersize=15, markeredgecolor="blue", markerfacecolor="white")
    
    if with_replace:
        pylab.errorbar(top, aggregate_repeats(data, top, repeats, True, -1), yerr=[20 for x in data], linewidth=2, color="green", marker='o', markersize=15, markeredgecolor="green", markerfacecolor="white")

    pylab.xscale('log', basex=10)

    pylab.xlabel('X')
    pylab.ylabel(ylabel)

    pylab.legend(['Crowd', 'Network - 1', 'Network - Inf', 'Network - Inf - Replace'], loc='upper left')
    
    pylab.tight_layout()

    pylab.savefig(output_filename + '.pdf')




if __name__ == '__main__':
    pass