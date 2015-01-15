# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Coordinate conversions with the pytpm Python package.

https://github.com/phn/pytpm
http://phn.github.com/pytpm
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np
from astropy.table import Table
import pytpm
from pytpm import tpm

SUPPORTED_SYSTEMS = 'fk5 fk4 galactic ecliptic'.split()


def get_state(system):
    # The table of TPM states is here
    # http://phn.github.com/pytpm/conversions.html#function-convert-convertv6

    # We set the epoch and equinox to get consistent results with
    # astrolib.coords.Position, see Position._set_tpmstate there.
    d = dict()
    d['fk5'] = dict(state=tpm.TPM_S06, epoch=tpm.J2000, equinox=tpm.J2000)
    d['fk4'] = dict(state=tpm.TPM_S05, epoch=tpm.B1950, equinox=tpm.B1950)
    d['galactic'] = dict(state=tpm.TPM_S04, epoch=tpm.J2000, equinox=tpm.byear2jd(1958))
    d['ecliptic'] = dict(state=tpm.TPM_S03, epoch=tpm.J2000, equinox=tpm.jyear2jd(1984))
    # d['icrs'] = TPM_S06
    return d[system]


def transform_celestial(coords, systems):

    if not set(systems.values()).issubset(SUPPORTED_SYSTEMS):
        return None

    # Convert coords to a list of tpm.V6C objects called in_coords
    lon, lat = np.radians(coords['lon']), np.radians(coords['lat'])
    dummy = np.zeros_like(lon)
    in_coords = pytpm.convert.cat2v6(lon, lat, dummy, dummy, dummy, dummy)

    # Do the coordinate transformation
    in_state, out_state = get_state(systems['in']), get_state(systems['out'])
    out_coords = pytpm.convert.convertv6(in_coords, s1=in_state['state'], s2=out_state['state'],
                                         equinox=in_state['equinox']) # epoch=in_state['epoch'],

    # Maybe we have to precess here fore some systems?
    # http://phn.github.com/pytpm/functions.html#pytpm.convert.precessv6

    #import IPython; IPython.embed(); 1/0

    # Convert list of tpm.V6C objects out_coords first
    # to a list of dicts, then to lon, lat numpy arrays
    out_coords = pytpm.convert.v62cat(out_coords) # , C=tpm.CB
    lon = np.array([_['alpha'] for _ in out_coords])
    lat = np.array([_['delta'] for _ in out_coords])
    lon, lat = np.degrees(lon), np.degrees(lat)

    out = Table()
    out['lon'] = lon
    out['lat'] = lat

    return out
