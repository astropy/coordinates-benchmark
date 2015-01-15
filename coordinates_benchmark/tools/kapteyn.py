# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Coordinate conversions with the kapteyn Python package.

kapteyn.celestial is very feature-complete and has great docs.
Check this out:

http://www.astro.rug.nl/software/kapteyn/celestial.html
http://www.astro.rug.nl/software/kapteyn/celestial.html#celestial.sky2sky
http://www.astro.rug.nl/software/kapteyn/celestial.html#celestial.skyparser

http://www.astro.rug.nl/software/kapteyn/celestialbackground.html
http://www.astro.rug.nl/software/kapteyn/celestialbackground.html#composing-other-transformations
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np
from astropy.table import Table
from kapteyn import celestial

SUPPORTED_SYSTEMS = 'fk5 fk4 icrs galactic ecliptic'.split()


def system_spec(system):
    """Convert generic system specification tags to Kapteyn specific specification strings."""
    d = dict()
    d['fk5'] = 'fk5'
    d['fk4'] = 'fk4,J2000_OBS'
    d['icrs'] = 'icrs'
    d['galactic'] = 'galactic'
    d['ecliptic'] = 'ecliptic,J2000'
    return str(d[system])


def transform_celestial(coords, systems):
    """Convert an array of in_coords from in_system to out_system"""
    # Use kapteyn package specific specifiers for in- and out-systems
    skyin, skyout = system_spec(systems['in']), system_spec(systems['out'])

    coords = celestial.sky2sky(skyin, skyout, coords['lon'], coords['lat'])
    coords = np.array(coords)

    out = Table()
    out['lon'] = coords[:, 0]
    out['lat'] = coords[:, 1]

    return out
