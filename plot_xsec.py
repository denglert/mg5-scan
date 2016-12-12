#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

#################################################

# - Our input datafile
dataFile = 'xsec_sqrt_s.dat'

print('Opening file {}.'.format(dataFile) )

# - Load data into a python
data = np.genfromtxt( dataFile, delimiter='\t', skip_header=0, skip_footer=0, names=['sqrt_s', 'xsec', 'xsec_unc'])
print(data)

# - Create figure object
fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True)
fig = plt.figure()


# - Plot with errorbars
plt.errorbar(data['sqrt_s'], data['xsec'], yerr=data['xsec_unc'], fmt='--o' )
#plt.scatter(data['sqrt_s'], data['xsec'])

# - Labels
plt.xlabel('$\sqrt{s}$ [GeV]')
plt.ylabel('$\sigma$ [pb]')

# - Save figure
plt.savefig('./xsec.pdf')
