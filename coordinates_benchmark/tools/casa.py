# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Coordinate conversions with the CASA measures tool.

https://casadocs.readthedocs.io/en/stable/api/tt/casatools.measures.html
https://casa.nrao.edu/
"""
from __future__ import absolute_import, division, print_function

import numpy as np
from astropy.table import Table
import casatools

SUPPORTED_SYSTEMS = 'fk5 fk4 icrs galactic ecliptic'.split()

# Map benchmark system names to CASA measures reference codes
_SYSTEM_MAP = {
    'fk5': 'J2000',
    'fk4': 'B1950',
    'icrs': 'ICRS',
    'galactic': 'GALACTIC',
    'ecliptic': 'ECLIPTIC',
}

# MJD of J2000.0 epoch, used as the reference epoch for ecliptic conversions
_MJD_J2000 = 51544.0


def _get_measures():
    """Return an initialised CASA measures tool."""
    mt = casatools.measures()
    # Set J2000 epoch as the default frame; this is required for ecliptic
    # conversions which use the mean ecliptic of date.
    mt.doframe(mt.epoch('UTC', '{0}d'.format(_MJD_J2000)))
    return mt


def transform_celestial(coords, systems):
    in_ref = _SYSTEM_MAP[systems['in']]
    out_ref = _SYSTEM_MAP[systems['out']]

    mt = _get_measures()

    lons_out = np.zeros(len(coords), dtype='float64')
    lats_out = np.zeros(len(coords), dtype='float64')

    for ii, (lon, lat) in enumerate(zip(coords['lon'], coords['lat'])):
        d_in = mt.direction(in_ref, '{0}deg'.format(lon), '{0}deg'.format(lat))
        d_out = mt.measure(d_in, out_ref)
        lons_out[ii] = np.degrees(d_out['m0']['value'])
        lats_out[ii] = np.degrees(d_out['m1']['value'])

    out = Table()
    out['lon'] = lons_out
    out['lat'] = lats_out
    return out


def _convert_radec_to_altaz(ra, dec, lon, lat, height, time):
    """Convert a single ICRS/J2000 position to horizontal (Az/Alt) coordinates.

    Parameters
    ----------
    ra, dec : float
        Right ascension and declination in degrees (FK5 J2000).
    lon, lat : float
        Observer geographic longitude and latitude in degrees.
    height : float
        Observer height above the WGS84 ellipsoid in kilometres.
    time : str
        UTC date string, e.g. ``'2000-01-01'``.
    """
    mt = casatools.measures()

    # Set observer position (height converted from km to m)
    obs_pos = mt.position('WGS84',
                          '{0}deg'.format(lon),
                          '{0}deg'.format(lat),
                          '{0}km'.format(height))
    mt.doframe(obs_pos)

    # Set observation epoch from UTC date string
    #   Note: CASA requires a time, so we append midnight. When comparing to
    #   other tools, make sure they are using the same time.
    mt.doframe(mt.epoch('UTC', '{0}/00:00:00'.format(time)))

    d = mt.direction('J2000', '{0}deg'.format(ra), '{0}deg'.format(dec))
    d_azel = mt.measure(d, 'AZELGEO')

    az = np.degrees(d_azel['m0']['value'])
    alt = np.degrees(d_azel['m1']['value'])
    return dict(az=az, alt=alt)


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
