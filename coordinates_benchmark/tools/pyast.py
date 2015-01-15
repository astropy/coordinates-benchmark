# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Coordinate conversions with the pyast Python package.

https://github.com/timj/starlink-pyast
http://dsberry.github.com/starlink/pyast.html
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np
import starlink.Ast as Ast
from astropy.time import Time


SUPPORTED_SYSTEMS = 'fk5 fk4 icrs galactic ecliptic'.split()


def get_frame(system):
    """Convert generic system specification tags to pyast.SkyFrame"""
    # Create a Frame to describe J2000 FK5 coordinates, and another that
    #  will be used in turn to describe each of the output coordinate systems.
    #  Assume that the epoch of observation is J2000.0. The default values for
    #  the reference equinox will be used (J2000.0 for FK5 and ecliptic, and
    #  B1950.0 for FK4).
    d = dict()
    d['fk5'] = 'FK5'
    d['fk4'] = 'FK4'
    d['galactic'] = 'Galactic'
    d['ecliptic'] = 'Ecliptic'
    d['icrs'] = 'ICRS'
    return Ast.SkyFrame('System=%s,Format(1)=hms.5,Format(2)=dms.5,Epoch=2000.0' % d[system])


def convert(coords, systems):
    """Convert an array of in_coords from in_system to out_system"""

    if not set(systems.values()).issubset(SUPPORTED_SYSTEMS):
        return None

    in_frame, out_frame = get_frame(systems['in']), get_frame(systems['out'])
    frameset = in_frame.convert(out_frame)
    lon, lat = np.radians(coords['lon']), np.radians(coords['lat'])
    coords = frameset.tran([lon, lat])
    coords = np.degrees(coords.T)
    return dict(lon=coords[:, 0], lat=coords[:, 1])



def altaz_radec_transform():
    # TODO: rewrite
    raise NotImplementedError
    # Read in initial coordinates and the observers.
    # For now just process one observer and 10 positions to compare against pyast
    data_j2000 = np.loadtxt('../../input/initial_coords.txt')[:3]
    observers = np.recfromcsv('../../input/observers.txt')[:2]

    # We'll store the results here
    results = np.zeros(data_j2000.shape[0] * observers.shape[0], dtype=[('az', 'float64'), ('alt', 'float64')])

    for ii, (lon, lat, altitude, time, time_mjd, time_tdb) in enumerate(observers):
        for jj, (ra, dec) in enumerate(data_j2000):

            fk5_frame = Ast.SkyFrame('System=FK5,Format(1)=hms.5,Format(2)=dms.5,Epoch=2000.0')
            # TODO: Need to set fk5_frame.Epoch in tdb scale?
            out_frame = Ast.SkyFrame('System=AZEL,Format(1)=hms.5,Format(2)=dms.5')

            # Set observation location and time
            # http://www.starlink.rl.ac.uk/docs/sun211.htx/node612.html#System
            out_frame.ObsLon = lon
            out_frame.ObsLat = lat
            out_frame.ObsAlt = altitude
            # http://www.starlink.rl.ac.uk/docs/sun211.htx/node489.html#Epoch
            epoch = Time(time, scale='utc').tdb.mjd
            out_frame.Epoch = epoch
            # http://www.starlink.rl.ac.uk/docs/sun211.htx/node486.html
            # http://en.wikipedia.org/wiki/DUT1
            # TODO: Set DUT1 correctly. But how to compute it?
            out_frame.Dut1 = 0

            # Compute alt / az
            fk5_to_out = fk5_frame.convert( out_frame )
            az, alt = np.degrees(fk5_to_out.tran([[ra], [dec]]))

            # Store in results array
            kk = ii * data_j2000.shape[0] + jj
            results[kk]['az'] = az
            results[kk]['alt'] = alt

    np.savetxt('coords_fk5_to_horizontal.txt', results, fmt="%20.15f")
