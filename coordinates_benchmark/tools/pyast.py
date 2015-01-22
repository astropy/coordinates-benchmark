# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Coordinate conversions with the pyast Python package.

https://github.com/timj/starlink-pyast
http://dsberry.github.com/starlink/pyast.html
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np
from astropy.table import Table
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


def transform_celestial(coords, systems):
    in_frame, out_frame = get_frame(systems['in']), get_frame(systems['out'])
    frameset = in_frame.convert(out_frame)
    lon, lat = np.radians(coords['lon']), np.radians(coords['lat'])
    coords = frameset.tran([lon, lat])
    coords = np.degrees(coords.T)

    out = Table()
    out['lon'] = coords[:, 0]
    out['lat'] = coords[:, 1]
    return out

def _convert_radec_to_altaz(ra, dec, lon, lat, height, time):

    # Convert supplied UTC date string to a UTC MJD.
    utc_frame = Ast.TimeFrame( 'TimeScale=UTC' )
    (nc, utc_epoch) = utc_frame.unformat( 1, time )

    # Convert the UTC MJD to a TDB epoch (i.e. a decimal year).
    tdb_frame = Ast.TimeFrame( 'System=JEPOCH,TimeScale=TDB' )
    mapping = utc_frame.convert(tdb_frame)
    tdb_epoch = mapping.tran(utc_epoch)

    # Create a Frame describing FK5 coords. Note we need to prefix the
    # epoch with "J" to indicate that it is a Julian epoch. This is
    # because values less than 1984.0 are interpreted as Besselian by
    # default.
    fk5_frame = Ast.SkyFrame('System=FK5,Epoch=J{0}'.format(tdb_epoch[0][0]))

    # Create a Frame describing AZEL (aka altaz) coords.
    azel_frame = Ast.SkyFrame('System=AZEL,Epoch=J{0}'.format(tdb_epoch[0][0]))
    azel_frame.ObsLon = lon
    azel_frame.ObsLat = lat
    azel_frame.ObsAlt = height*1000.0

    # Get the mapping from fk5 to azel.
    mapping = fk5_frame.convert(azel_frame)

    # Use it to transform the supplied (ra,dec) values to (az,el) values.
    coords = mapping.tran([ [np.radians(ra)], [np.radians(dec)] ])
    az = np.degrees( coords[0][0] )
    el = np.degrees( coords[1][0] )
    return dict( az=az, alt=el )

def convert_horizontal(positions, observers):

    results = []
    for observer in observers:
        for position in positions:

            ra = position['lon']
            dec = position['lat']
            lon = observer['lon']
            lat = observer['lat']
            height = observer['height']
            time = observer['time']
            altaz = _convert_radec_to_altaz(ra, dec, lon, lat, height, time)
            results.append(altaz)

    out = Table(results)
    return out
