"""
Coordinate conversions with the pyslalib Python package.

https://github.com/scottransom/pyslalib
"""
import numpy as np
from pyslalib import slalib as S

# Read in initial coordinates as J2000 coordinates
data_j2000 = np.radians(np.loadtxt('../initial_coords.txt'))
ra_j2000_fk5, dec_j2000_fk5 = data_j2000[:,0], data_j2000[:,1]

vals = {}
for system in 'FK4', 'Ecliptic', 'Galactic', 'ICRS':
   vals[system] = [np.zeros_like(ra_j2000_fk5), np.zeros_like(dec_j2000_fk5)]

for ii, (raj, decj) in enumerate(zip(ra_j2000_fk5, dec_j2000_fk5)):

   # FK5 -> FK4 at BEPOCH 2000.0 assuming no proper motion or parallax
   r1950, d1950, dr1950, dd1950 = S.sla_fk54z (raj, decj, 2000.0)
   vals['FK4'][0][ii],vals['FK4'][1][ii] = r1950, d1950

   # FK5 -> Ecliptic at TDB (MJD) 51544.0 (i.e. J2000)
   dl, db = S.sla_eqecl(raj, decj, 51544.0)
   vals['Ecliptic'][0][ii],vals['Ecliptic'][1][ii] = dl, db

   # FK5 -> Galactic
   dl, db = S.sla_eqgal(raj, decj)
   vals['Galactic'][0][ii],vals['Galactic'][1][ii] = dl, db

   # FK5 -> Hipparcos (i.e. ICRF, which is as close as SLALIB
   # gets to ICRS) at epoch 2000.0 and with no proper motion
   rh, dh = S.sla_fk5hz(raj, decj, 2000.0)
   vals['ICRS'][0][ii],vals['ICRS'][1][ii] = rh, dh


glon = vals['Galactic'][0]
glat = vals['Galactic'][1]
np.savetxt('coords_galactic.txt', zip(np.degrees(glon), 
                                       np.degrees(glat)), fmt="%20.15f")

ra_fk4 = vals['FK4'][0]
dec_fk4 = vals['FK4'][1]
np.savetxt('coords_b1950.txt', zip(np.degrees(ra_fk4),
                                    np.degrees(dec_fk4)), fmt="%20.15f")

elon = vals['Ecliptic'][0]
elat = vals['Ecliptic'][1]
np.savetxt('coords_ecliptic.txt', zip(np.degrees(elon),
                                       np.degrees(elat)), fmt="%20.15f")

ra_fk5 = vals['ICRS'][0]
dec_fk5 = vals['ICRS'][1]
np.savetxt('coords_j2000.txt', zip(np.degrees(ra_fk5),
                                    np.degrees(dec_fk5)), fmt="%20.15f")
