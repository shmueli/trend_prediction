import math
import random
import pylab
import visualize

def draw_powerlaw(alpha, cutoff, a, b):

    x = cutoff
    while x>=cutoff:
        y = random.random()
        x = math.pow(1.-y, -1./(alpha-1.))

    x = a + x/(cutoff-1.)*(b-a)
    
    return x
                              

if __name__ == '__main__':
    data = []
    for i in range(1000):
        x = draw_powerlaw(2.0, 100, 0, 1)
        data.append(x)
    
    print data
    print min(data), max(data)
     
    pylab.hist(data)
    pylab.show()
       
    visualize.plot_bins(data, True, True, '', 'Density', 'aaa')
    
    print 'Done.'