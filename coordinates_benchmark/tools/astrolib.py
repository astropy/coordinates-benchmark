# Licensed under a 3-clause BSD style license - see LICENSE.rst
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
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np
from astropy.table import Table
from astrolib.coords import Position

SUPPORTED_SYSTEMS = 'fk5 fk4 galactic ecliptic'.split()


def transform_celestial(coords, systems):
    out = Table()
    out['lon'] = np.zeros(len(coords), dtype='float64')
    out['lat'] = np.zeros(len(coords), dtype='float64')

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

        out['lon'][ii] = lon
        out['lat'][ii] = lat

    return out
