import numpy
import powerlaw
# import plfit
# import plplot
# import plfit2
from pl import plpva


def fit_data(Y, discrete=False, pdf=True, original_data=False, xmin=None):
    stats = (xmin==None)
        
    Y = [y for y in Y if y>0]

    fit = powerlaw.Fit(Y, discrete=discrete, xmin=xmin)
    alpha = fit.alpha
    xmin = fit.xmin

    if pdf:
        ORG_X1, ORG_Y1 = fit.pdf(original_data=original_data)
        X1 = [(ORG_X1[i]+ORG_X1[i+1])/2.0 for i in range(len(ORG_Y1)) if ORG_Y1[i]>0]
        Y1 = [ORG_Y1[i] for i in range(len(ORG_Y1)) if ORG_Y1[i]>0]
    else:
        X1, Y1 = fit.ccdf(original_data=original_data)

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
    '''
    X2 = sorted(numpy.unique(X1))
    if pdf:
        Y2 = pl.pdf(data=X2)
    else:
        Y2 = pl.ccdf(data=X2)
    X2 = X2[-len(Y2):]
    '''
    X2 = [x for x in X1 if x>=xmin]
    if pdf:
        Y2 = pl.pdf(data=X2)
    else:
        Y2 = pl.ccdf(data=X2)

    
    '''
    if stats:
        [p, gof] = calc_gof(Y, xmin)
        print 'xmin:', xmin, 'alpha:', alpha, 'p:', p
    '''
    
    '''
    if stats:
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


    return X1, Y1, X2, Y2, xmin, alpha


def calc_gof(Y, xmin):
    Y = [y for y in Y if y>0]

    [p, gof] = plpva.plpva(Y, xmin, 'reps', 100, 'silent')
    return p, gof

