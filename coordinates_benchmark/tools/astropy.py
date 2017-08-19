# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Coordinate conversions with the Astropy Python package.

https://github.com/astropy/astropy
http://www.astropy.org
"""
from __future__ import absolute_import, division, print_function

from astropy.table import Table
from astropy.coordinates import Angle, EarthLocation, AltAz, SkyCoord
from astropy import coordinates as coord
from astropy.time import Time
from astropy import units as u

SUPPORTED_SYSTEMS = 'fk5 fk4 icrs galactic ecliptic'.split()


def get_system(system):
    """Convert generic system specification tags to astropy specific class."""
    d = dict()
    d['fk5'] = coord.FK5
    d['fk4'] = coord.FK4
    d['icrs'] = coord.ICRS
    d['galactic'] = coord.Galactic
    d['ecliptic'] = coord.BarycentricTrueEcliptic
    return d[system]


def transform_celestial(coords, systems):
    skyin, skyout = get_system(systems['in']), get_system(systems['out'])

    in_kwargs = {}
    if skyin is coord.FK4:
        in_kwargs['obstime'] = Time('J2000', scale='utc')

    out_kwargs = {}
    if skyout is coord.FK4:
        out_kwargs['obstime'] = Time('J2000', scale='utc')

    in_coord = skyin(coords['lon'] * u.deg, coords['lat'] * u.deg, **in_kwargs)

    out_coord = in_coord.transform_to(skyout(**out_kwargs))

    out = Table()
    out['lon'] = out_coord.spherical.lon.degree
    out['lat'] = out_coord.spherical.lat.degree

    return out


def _convert_radec_to_altaz(ra, dec, lon, lat, height, time):
    """Convert a single position.

    This is done for easy code sharing with other tools.
    Astropy does support arrays of positions.
    """
    radec = SkyCoord(ra, dec, unit='deg')

    location = EarthLocation(lon=Angle(lon, 'deg'),
                             lat=Angle(lat, 'deg'),
                             height=height * u.km)


    # Pressure = 0 is the default
    obstime = Time(time, scale='utc')
    # temperature = 0 * u.deg_C
    # pressure = 0 * u.bar
    # relative_humidity = ?
    # obswl = ?
    altaz_frame = AltAz(obstime=obstime, location=location)
    #                temperature=temperature, pressure=pressure)

    altaz = radec.transform_to(altaz_frame)
    az = altaz.az.deg
    alt = altaz.alt.deg

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
