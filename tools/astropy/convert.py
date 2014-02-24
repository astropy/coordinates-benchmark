"""
Coordinate conversions with the astropy Python package.

https://github.com/astropy/astropy
http://www.astropy.org
"""
import numpy as np
from astropy import coordinates as coord
from astropy.time import Time
from astropy import units as u

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

    lons = np.zeros_like(coords['lon'])
    lats = np.zeros_like(coords['lat'])

    in_coord = skyin(coords['lon'], coords['lat'], unit=(u.degree, u.degree),
                     obstime=Time('J2000', scale='utc'))

    out_coord = in_coord.transform_to(skyout)

    lons, lats = out_coord.lonangle.degree, out_coord.latangle.degree

    lons = lons % 360.

    return dict(lon=lons, lat=lats)
