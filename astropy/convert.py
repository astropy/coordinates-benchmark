"""
Coordinate conversions with the astropy Python package.

https://github.com/astropy/astropy
http://www.astropy.org
"""
import numpy as np
from astropy import coordinates as coord
from astropy.time import Time

SUPPORTED_SYSTEMS = 'fk5 fk4 icrs galactic'.split()

def get_system(system):
    """Convert generic system specification tags to astropy specific class."""
    d = dict()
    d['fk5'] = coord.FK5Coordinates
    d['fk4'] = coord.FK4Coordinates
    d['icrs'] = coord.ICRSCoordinates
    d['galactic'] = coord.GalacticCoordinates
    return d[system]

def convert(coords, systems):

    if not set(systems.values()).issubset(SUPPORTED_SYSTEMS):
        return None

    skyin, skyout = get_system(systems['in']), get_system(systems['out'])

    lons = np.zeros_like(coords['lon'])
    lats = np.zeros_like(coords['lat'])

    for ii, (lon, lat) in enumerate(zip(coords['lon'], coords['lat'])):
        in_coord = skyin(lon, lat, unit='deg')
    
        #if (systems['in'] == 'fk5' and systems['out'] == 'fk4'):
        if systems['in'] == 'fk4':
            in_coord.precess_to(Time('B1950', scale='utc'))
    
        out_coord = in_coord.transform_to(skyout)
    
        if systems['out'] == 'fk4':
            out_coord.precess_to(Time('B1950', scale='utc'))
        
        lon, lat = out_coord.longangle.degrees, out_coord.latangle.degrees
        # Wrap longitude to range 0 to 360
        lon = np.where(lon < 0, lon + 360, lon) 

        lons[ii], lats[ii] = lon, lat

    return dict(lon=lons, lat=lats)
