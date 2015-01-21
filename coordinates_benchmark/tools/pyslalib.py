# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Coordinate conversions with the pyslalib Python package.

https://github.com/scottransom/pyslalib
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np
from astropy.table import Table
from pyslalib import slalib

SUPPORTED_SYSTEMS = 'fk5 fk4 icrs galactic ecliptic'.split()


def transform_celestial(coords, systems):
    lons, lats = np.radians(coords['lon']), np.radians(coords['lat'])

    out = Table()
    out['lon'] = np.zeros(len(coords), dtype='float64')
    out['lat'] = np.zeros(len(coords), dtype='float64')

    for ii, (lon, lat) in enumerate(zip(lons, lats)):

        # First convert to FK5 J2000 in all cases
        if systems['in'] == 'fk4':
            lon, lat = slalib.sla_fk45z(lon, lat, 2000.0012775136652)
        elif systems['in'] == 'icrs':
            lon, lat = slalib.sla_hfk5z(lon, lat, 2000)[:2]
        elif systems['in'] == 'galactic':
            lon, lat = slalib.sla_galeq(lon, lat)
        elif systems['in'] == 'ecliptic':
            lon, lat = slalib.sla_ecleq(lon, lat, 51544)

        # Now convert from FK5 J2000 to out system    
        if systems['out'] == 'fk4':
            # FK5 -> FK4 at BEPOCH 2000 assuming no proper motion or parallax
            lon, lat = slalib.sla_fk54z(lon, lat, 2000.0012775136652)[:2]
        elif systems['out'] == 'icrs':
            # FK5 -> Hipparcos (i.e. ICRF, which is as close as SLALIB
            # gets to ICRS) at epoch 2000 and with no proper motion
            lon, lat = slalib.sla_fk5hz(lon, lat, 2000)
        elif systems['out'] == 'galactic':
            # FK5 -> Galactic
            lon, lat = slalib.sla_eqgal(lon, lat)
        elif systems['out'] == 'ecliptic':
            # FK5 -> Ecliptic at TDB (MJD) 51544 (i.e. J2000)
            lon, lat = slalib.sla_eqecl(lon, lat, 51544)

        out[ii]['lon'] = np.degrees(lon)
        out[ii]['lat'] = np.degrees(lat)

    return out
