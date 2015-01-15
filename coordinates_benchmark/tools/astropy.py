# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Coordinate conversions with the Astropy Python package.

https://github.com/astropy/astropy
http://www.astropy.org
"""
import logging
from astropy.table import Table
from astropy.coordinates import Angle, EarthLocation, AltAz, SkyCoord
from astropy import coordinates as coord
from astropy.time import Time
from astropy import units as u
from ..config import FLOAT_FORMAT, TABLE_FORMAT

SUPPORTED_SYSTEMS = 'fk5 fk4 icrs galactic'.split()


def get_system(system):
    """Convert generic system specification tags to astropy specific class."""
    d = dict()
    d['fk5'] = coord.FK5
    d['fk4'] = coord.FK4
    d['icrs'] = coord.ICRS
    d['galactic'] = coord.Galactic
    return d[system]


def convert(coords, systems):
    if not set(systems.values()).issubset(SUPPORTED_SYSTEMS):
        return None

    skyin, skyout = get_system(systems['in']), get_system(systems['out'])

    in_kwargs = {}
    if skyin is coord.FK4:
        in_kwargs['obstime'] = Time('J2000', scale='utc')

    out_kwargs = {}
    if skyout is coord.FK4:
        out_kwargs['obstime'] = Time('J2000', scale='utc')

    in_coord = skyin(coords['lon'] * u.deg, coords['lat'] * u.deg, **in_kwargs)

    out_coord = in_coord.transform_to(skyout(**out_kwargs))

    lons, lats = out_coord.spherical.lon.degree, out_coord.spherical.lat.degree

    lons = lons % 360.

    return dict(lon=lons, lat=lats)


def read_positions_observers():
    # Read in initial coordinates and the observers.
    # For now just process one observer and 10 positions to compare against pyast
    positions = Table.read('../../input/initial_coords.txt', format='ascii',
                           names=['lon', 'lat'])
    observers = Table.read('../../input/observers.txt', format='ascii')

    # Select subset for now
    positions = positions[:10]

    return positions, observers


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

    table = Table(results)
    return table


def main():
    positions, observers = read_positions_observers()

    results = convert_horizontal(positions, observers)

    for col in ['az', 'alt']:
        results[col].format = FLOAT_FORMAT

    filename = 'coords_fk5_to_horizontal.txt'
    logging.info('Writing {}'.format(filename))
    results.write(filename, format=TABLE_FORMAT)
