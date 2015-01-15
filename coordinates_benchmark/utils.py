# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Utility functions / classes.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np


# TODO: replace by function from astropy.coordinates
def _vicenty_dist_arcsec(lon1, lat1, lon2, lat2):
    """Compute distance on the sky. Input and output in arcsec"""

    lon1 = np.radians(lon1)
    lat1 = np.radians(lat1)
    lon2 = np.radians(lon2)
    lat2 = np.radians(lat2)

    sdlon = np.sin(lon2 - lon1)
    cdlon = np.cos(lon2 - lon1)

    num1 = np.cos(lat2) * sdlon
    num2 = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * cdlon
    denominator = np.sin(lat1) * np.sin(lat2) + np.cos(lat1) * np.cos(lat2) * cdlon

    dist_in_radians = np.arctan2((num1 ** 2 + num2 ** 2) ** 0.5, denominator)
    deg_to_arcsec = 3600.
    return deg_to_arcsec * np.degrees(dist_in_radians)
