import numpy as np

import ephem

# Read in initial coordinates as J2000 coordinates
data_j2000 = np.loadtxt('../initial_coords.txt')

f = {}
f['galactic'] = open('coords_galactic.txt', 'wb')
f['b1950'] = open('coords_b1950.txt', 'wb')
f['ecliptic'] = open('coords_ecliptic.txt', 'wb')

for i in range(len(data_j2000)):

    ra_j2000, dec_j2000 = np.radians((data_j2000[i,0], data_j2000[i,1]))

    j2000 = ephem.Equatorial(ra_j2000, dec_j2000)

    # Convert to Galactic coordinates
    galactic = ephem.Galactic(j2000)
    l, b = np.degrees((galactic.lon, galactic.lat))
    f['galactic'].write("%20.15f %20.15f\n" % (l, b))

    # Convert to B1950
    b1950 = ephem.Equatorial(j2000, epoch=ephem.B1950)
    ra_b1950, dec_b1950 = np.degrees((b1950.ra, b1950.dec))
    f['b1950'].write("%20.15f %20.15f\n" % (ra_b1950, dec_b1950))

    # Convert to ecliptic
    ecliptic = ephem.Ecliptic(j2000)
    elon, elat = np.degrees((ecliptic.lon, ecliptic.lat))
    f['ecliptic'].write("%20.15f %20.15f\n" % (elon, elat))

for system in f:
    f[system].close()
