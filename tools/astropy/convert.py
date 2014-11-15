"""
Coordinate conversions with the astropy Python package.

https://github.com/astropy/astropy
http://www.astropy.org
"""
import numpy as np
from astropy.coordinates import SkyCoord
#from astropy.time import Time
#from astropy import units as u

SUPPORTED_SYSTEMS = 'fk5 fk4 icrs galactic'.split()

def convert(coords, systems):

    if not set(systems.values()).issubset(SUPPORTED_SYSTEMS):
        return None

    frame_in = systems['in']
    pos_in = SkyCoord(coords['lon'], coords['lat'], unit='deg', frame=frame_in)

    frame_out = systems['out']
    pos_out = pos_in.transform_to(frame_out)

    lons = pos_out.data.lon.degree
    lats = pos_out.data.lat.degree

    return dict(lon=lons, lat=lats)
