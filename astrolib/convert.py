"""
Coordinate conversions with the astrolib coords package.
astrolib coords is a Python wrapper around the TPM C library [2].

I couldn't find a repository for TPM, but there is another
Python wrapper for it called pytpm which has TPM bundled
and is on github, so you can look at the code there.

[1] http://www.scipy.org/AstroLibCoordsHome
[2] http://www.sal.wisc.edu/~jwp/astro/tpm/tpm.html
[3] https://github.com/phn/pytpm/tree/master/src/tpm
"""
import numpy as np
from coords import Position 

SUPPORTED_SYSTEMS = 'fk5 fk4 galactic ecliptic'.split()

def convert(coords, systems):
    
    if not set(systems.values()).issubset(SUPPORTED_SYSTEMS):
        return None

    lons = np.zeros_like(coords['lon'])
    lats = np.zeros_like(coords['lat'])

    for ii, (lon, lat) in enumerate(zip(coords['lon'], coords['lat'])):

        # Create coordinate in input system
        if systems['in'] == 'fk5':
            coord = Position((lon, lat))
        elif systems['in'] == 'fk4':
            coord = Position((lon, lat), system='celestial', equinox='B1950')
        elif systems['in'] == 'galactic':
            coord = Position((lon, lat), system='galactic')
        elif systems['in'] == 'ecliptic':
            coord = Position((lon, lat), system='ecliptic')
        else:
            raise ValueError()
        
        # Convert to appropriate output system
        if systems['out'] == 'fk5':
            lon, lat = coord.j2000()
        elif systems['out'] == 'fk4':
            lon, lat = coord.b1950()
        elif systems['out'] == 'galactic':
            lon, lat = coord.galactic()
        elif systems['out'] == 'ecliptic':
            lon, lat = coord.ecliptic()
        else:
            raise ValueError()

        lons[ii], lats[ii] = lon, lat

    return dict(lon=lons, lat=lats)