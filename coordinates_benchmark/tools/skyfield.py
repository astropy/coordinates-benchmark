# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Coordinate conversions with the Skyfield Python package.

https://github.com/skyfielders/python-skyfield
https://rhodesmill.org/skyfield/
"""
from __future__ import absolute_import, division, print_function

from skyfield.units import Angle
from skyfield.api import Star, wgs84, load
from skyfield.data import iers
from astropy.time import Time
from astropy.table import Table


EPHEMERIS = 'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de430.bsp'


def _convert_radec_to_altaz(ra, dec, lon, lat, height, time):
    """Convert a single position.

    This is done for easy code sharing with other tools.
    Skyfield does support arrays of positions.
    """

    radec = Star(ra=Angle(degrees=ra), dec=Angle(degrees=dec))

    earth = load(EPHEMERIS)['earth']
    location = earth + wgs84.latlon(longitude_degrees=lon,
                                    latitude_degrees=lat,
                                    elevation_m=height * 1000.0)

    ts = load.timescale(builtin=False)
    with load.open('finals2000A.all') as f:
        finals_data = iers.parse_x_y_dut1_from_finals_all(f)
    iers.install_polar_motion_table(ts, finals_data)
    obstime = ts.from_astropy(Time(time, scale='utc'))

    alt, az, _ = location.at(obstime).observe(radec).apparent().altaz(pressure_mbar=0)

    return dict(az=az.degrees, alt=alt.degrees)


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
