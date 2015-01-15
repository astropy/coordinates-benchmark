# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Create lists of sky coordinates."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import logging
import numpy as np
import click
from astropy.table import Table
from ..config import FLOAT_FORMAT_INPUT, TABLE_FORMAT


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
    table = Table()
    table['lon'] = np.random.uniform(0., 360., N)
    table['lat'] = np.degrees(np.arcsin(np.random.uniform(-1., 1., N)))

    for col in ['lon', 'lat']:
        table[col].format = FLOAT_FORMAT_INPUT

    return table


@click.command(name='make_skycoord_table')
def make_skycoord_table_command():
    """Generate table of random sky coordinates."""
    table = make_skycoord_table()

    filename = 'input/skycoords.txt'
    logging.info('Writing {}'.format(filename))
    table.write(filename, format=TABLE_FORMAT)
