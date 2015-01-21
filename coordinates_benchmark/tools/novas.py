# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Conversions using the Python-wrapped high-precision C NOVAS library.

http://aa.usno.navy.mil/software/novas/novas_py/novaspy_intro.php
https://github.com/brandon-rhodes/python-novas
https://pypi.python.org/pypi/novas/

"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np
from astropy.table import Table
from novas import compat as novas

T0 = 2451545.00000000

SUPPORTED_SYSTEMS = 'icrs fk5 ecliptic'.split()


def transform_celestial(coords, systems):
    rav = coords['lon'] / 15.0
    decv = coords['lat']
    plist = [novas.radec2vector(ra, dec, 1.0) for ra, dec in zip(rav, decv)]

    if systems['in'] == 'icrs':
        pass
    elif systems['in'] == 'fk5':
        plist = [novas.frame_tie(position, -1) for position in plist]
    elif systems['in'] == 'ecliptic':
        plist = [novas.ecl2equ_vec(T0, position, 2) for position in plist]

    if systems['out'] == 'icrs':
        pass
    elif systems['out'] == 'fk5':
        plist = [novas.frame_tie(position, 0) for position in plist]
    elif systems['out'] == 'ecliptic':
        plist = [novas.equ2ecl_vec(T0, position, 2) for position in plist]

    ra, dec = np.array([novas.vector2radec(position) for position in plist]).T

    out = Table()
    out['lon'] = ra * 15.0
    out['lat'] = dec

    return out
