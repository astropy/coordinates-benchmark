# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Conversions using the Python-wrapped high-precision C NOVAS library.

http://aa.usno.navy.mil/software/novas/novas_py/novaspy_intro.php
https://github.com/brandon-rhodes/python-novas
https://pypi.python.org/pypi/novas/

"""
import numpy as np
from novas import compat as novas

T0 = 2451545.00000000


def convert(coords, systems):
    rav = coords['lon'] / 15.0
    decv = coords['lat']
    plist = [novas.radec2vector(ra, dec, 1.0) for ra, dec in zip(rav, decv)]

    if systems['in'] == 'icrs':
        pass
    elif systems['in'] == 'fk5':
        plist = [novas.frame_tie(position, -1) for position in plist]
    elif systems['in'] == 'ecliptic':
        plist = [novas.ecl2equ_vec(T0, position, 2) for position in plist]
    else:
        return None

    if systems['out'] == 'icrs':
        pass
    elif systems['out'] == 'fk5':
        plist = [novas.frame_tie(position, 0) for position in plist]
    elif systems['out'] == 'ecliptic':
        plist = [novas.equ2ecl_vec(T0, position, 2) for position in plist]
    else:
        return None

    ra, dec = np.array([novas.vector2radec(position) for position in plist]).T
    return dict(lon=ra * 15.0, lat=dec)
