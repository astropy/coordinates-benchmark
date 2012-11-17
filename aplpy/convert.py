import numpy as np

from aplpy.wcs_util import fk52gal, j2000tob1950

# Read in initial coordinates as J2000 coordinates
data_j2000 = np.loadtxt('../initial_coords.txt')
ra_j2000, dec_j2000 = data_j2000[:,0], data_j2000[:,1]

glon, glat = fk52gal(ra_j2000, dec_j2000)
np.savetxt('coords_galactic.txt', zip(glon, glat), fmt="%20.15f")

ra_fk4, dec_fk4 = j2000tob1950(ra_j2000, dec_j2000)
np.savetxt('coords_b1950.txt', zip(ra_fk4, dec_fk4), fmt="%20.15f")
