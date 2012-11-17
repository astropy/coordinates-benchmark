import numpy as np

from astropy import coordinates as coord

# Read in initial coordinates as J2000 coordinates
data_j2000 = np.loadtxt('../initial_coords.txt')

f = {}
f['galactic'] = open('coords_galactic.txt', 'wb')
f['b1950'] = open('coords_b1950.txt', 'wb')

for i in range(len(data_j2000)):

    ra_j2000, dec_j2000 = data_j2000[i,0], data_j2000[i,1]
    fk5 = coord.FK5Coordinates(ra_j2000, dec_j2000, unit='degree')

    # Convert to Galactic coordinates
    galactic = fk5.galactic
    l, b = galactic.l, galactic.b
    f['galactic'].write("%20.15f %20.15f\n" % (l.degrees, b.degrees))

    # Convert to B1950
    fk4 = fk5.fk4
    ra_b1950, dec_b1950 = fk4.ra, fk4.dec
    f['b1950'].write("%20.15f %20.15f\n" % (ra_b1950.degrees,
                                            dec_b1950.degrees))

    # Convert to ecliptic
    # Not implemented yet

for system in f:
    f[system].close()