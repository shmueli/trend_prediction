import pylab as pl
import numpy as np

size = 256, 16
dpi = 72.0
figsize= size[0] / float(dpi), size[1] / float(dpi)
fig = pl.figure(figsize=figsize, dpi=dpi)
fig.patch.set_alpha(0)
pl.axes([0, 0, 1, 1])

pl.plot(np.arange(4), np.ones(4), color="blue", linewidth=8,
        solid_capstyle='butt')

pl.plot(5 + np.arange(4), np.ones(4), color="blue", linewidth=8,
        solid_capstyle='round')

pl.plot(10 + np.arange(4), np.ones(4), color="blue", linewidth=8,
        solid_capstyle='projecting')

pl.xlim(0, 14)
pl.xticks(())
pl.yticks(())

pl.show()