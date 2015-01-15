# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Create lists of sky coordinates."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import logging
import numpy as np
import click
from ..config import FLOAT_FORMAT


def make_skycoord_table():
    """Generate table of random sky coordinates.

    TODO: change this to make an Astropy table.

    Columns:
    - lon      : longitude in deg
    - lat      : latitude in deg
    """
    np.random.seed(12345)

    # Number of samples
    N = 1000

    # Sample uniformly on the unit sphere
    lon = np.random.uniform(0., 360., N)
    lat = np.degrees(np.arcsin(np.random.uniform(-1., 1., N)))

    return lon, lat


@click.command(name='make_skycoord_table')
def make_skycoord_table_command():
    """Generate table of random sky coordinates."""
    lon, lat = make_skycoord_table()

    filename = 'input/initial_coords.txt'
    logging.info('Writing {}'.format(filename))
    np.savetxt(filename, zip(lon, lat), fmt=FLOAT_FORMAT)
