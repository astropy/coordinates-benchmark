import numpy as np

import coords

# Read in initial coordinates as J2000 coordinates
data_j2000 = np.loadtxt('../initial_coords.txt')

f = {}
f['galactic'] = open('coords_galactic.txt', 'wb')
f['b1950'] = open('coords_b1950.txt', 'wb')
f['ecliptic'] = open('coords_ecliptic.txt', 'wb')

for i in range(len(data_j2000)):

    ra_j2000, dec_j2000 = data_j2000[i,0], data_j2000[i,1]
    j2000 = coords.Position((ra_j2000, dec_j2000))

    # Convert to Galactic coordinates
    l, b = j2000.galactic()
    f['galactic'].write("%20.15f %20.15f\n" % (l, b))

    # Convert to B1950
    ra_b1950, dec_b1950 = j2000.b1950()
    f['b1950'].write("%20.15f %20.15f\n" % (ra_b1950, dec_b1950))

    # Convert to ecliptic
    elon, elat = j2000.ecliptic()
    f['ecliptic'].write("%20.15f %20.15f\n" % (elon, elat))

for system in f:
    f[system].close()
