# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Create lists of observers."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import logging
import itertools
import numpy as np
from astropy.time import Time
from astropy.table import Table
from ..config import FLOAT_FORMAT, TABLE_FORMAT
import click


def make_observer_table(n_samples=5):
    """Generate table of observers.

    TODO: use real observatory positions instead.

    A small list of observers (lon, lat, altitude, time in various formats).

    This list will be used as input for the horizontal coordinate conversion tests.

    Columns:
    - lon      : longitude in deg
    - lat      : latitude in deg
    - altitude : altitude in km
    - time     : UTC time string
    - time_mjd : time in MJD scale
    - time_tdb : time in TDB scale
    """
    np.random.seed(12345)

    # Sample uniformly on the unit sphere
    lon = np.random.uniform(0., 360., n_samples)
    lat = np.degrees(np.arcsin(np.random.uniform(-1., 1., n_samples)))

    # Sample of heights (distances from the Earth's center) in km
    height = np.array([6e3, 10e3], dtype='float64')

    # Sample of UTC times
    time = ['1970-01-01', '1980-01-01', '1990-01-01', '2000-01-01', '2010-01-01']

    # Some coordinate packages need time input on another scale
    # We use astropy.time to do the conversion and store several times in the ascii file.
    time_mjd = Time(time, scale='utc').mjd
    time_mjd = time_mjd.astype('int') # these are actually ints, I checked.
    time_tdb = Time(time, scale='utc').tdb.value

    # For each longitude, create an observer at each height and time
    # This is a cartesian product:
    # http://docs.python.org/2/library/itertools.html#itertools.product
    table = list(itertools.product(zip(lon, lat), height, zip(time, time_mjd, time_tdb)))
    table = [(_[0][0], _[0][1], _[1], _[2][0], _[2][1], _[2][2]) for _ in table]
    cols = 'lon lat height time time_mjd time_tdb'.split()

    table = Table(rows=table, names=cols)
    for cols in ['lon', 'lat', 'height']:
        table[cols].format = FLOAT_FORMAT

    return table


@click.command(name='make_observer_table')
def make_observer_table_command():
    """Generate table of observers."""
    table = make_observer_table()
    filename = 'input/observers.txt'
    logging.info('Writing {}'.format(filename))
    table.write(filename, format=TABLE_FORMAT)
