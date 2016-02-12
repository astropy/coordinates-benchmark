# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Configuration parameters and utility functions and classes.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import os
import logging
import itertools
from importlib import import_module
import numpy as np
from astropy.table import Table
from astropy.coordinates import Angle

TABLE_FORMAT = 'ascii.fixed_width_two_line'
FLOAT_FORMAT_OUTPUT = '%15.10f'   # For output tables
FLOAT_FORMAT_INPUT = '%20.15f'  # for input tables


# Make a list of celestial conversions to check
# We simply list all possible combinations here,
# systems not supported by certain tools are simply skipped later
CELESTIAL_SYSTEMS = sorted('fk5 fk4 icrs galactic ecliptic'.split())
CELESTIAL_CONVERSIONS = itertools.product(CELESTIAL_SYSTEMS, CELESTIAL_SYSTEMS)
CELESTIAL_CONVERSIONS = [dict(zip(['in', 'out'], _))
                         for _ in CELESTIAL_CONVERSIONS
                         if _[0] != _[1]]

TOOLS = sorted('astropy kapteyn novas pyast palpy pyephem pyslalib pytpm'.split())
TOOL_PAIRS = [_ for _ in itertools.product(TOOLS, TOOLS)
              if _[0] < _[1]]


def _import_name(name):
    if name == 'pyast':
        return 'starlink.Ast'
    elif name == 'pyephem':
        return 'ephem'
    else:
        return name


def _tool_check():
    tools = Table()
    tools['tool_name'] = TOOLS
    tools['import_name'] = [_import_name(_) for _ in TOOLS]
    tools['available'] = False
    # TODO: this is a temp workaround for this issue:
    # https://github.com/astropy/astropy/issues/3321
    tools['version'] = ['N/A' for _ in range(len(tools))]

    for tool in tools:
        try:
            module = import_module(tool['import_name'])
            tool['available'] = True
            try:
                version = module.__version__
                tool['version'] = version
            except AttributeError:
                pass
        except ImportError:
            pass

    return tools

# Table with tools are available and what their version is
TOOL_INFO = _tool_check()


def select_tools(tools, include_idl=False):
    """Select the sub-set of requested and available tools."""
    all = list(TOOL_INFO['tool_name'])

    if include_idl:
        all.add_row(['idl', True, 'N/A'])

    available = TOOL_INFO['tool_name'][TOOL_INFO['available']]

    requested = tools.split(',')

    if 'all' in requested:
        requested = all

    missing = set(requested).difference(available)
    if missing:
        logging.error('The following tools are not available: {}'.format(', '.join(missing)))
        exit(1)

    return sorted(requested)


def get_observers(use_subset=False):
    filename = 'input/observers.txt'
    logging.debug('Reading {}'.format(filename))

    table = Table.read(filename, format='ascii')

    if use_subset:
        table = table[:5]

    return table


def get_positions(symmetric=False, use_subset=False):
    filename = 'input/skycoords.txt'
    table = Table.read(filename, format='ascii',
                       names=['lon', 'lat'])

    if symmetric:
        lon = table['lon']
        table['lon'] = np.where(lon > 180, lon - 360, lon)

    if use_subset:
        table = table[:10]

    return table


def get_test_module(name):
    return import_module('coordinates_benchmark.tools.' + name)


def celestial_filename(tool, systems):
    fmt = 'output/tools/{}/{}_to_{}.txt'
    return fmt.format(tool, systems['in'], systems['out'])


def celestial_results(tool, systems, symmetric=False):
    filename = celestial_filename(tool, systems)
    table = Table.read(filename, format=TABLE_FORMAT)

    if symmetric:
        lon = table['lon']
        table['lon'] = np.where(lon > 180, lon - 360, lon)

    return table


# TODO: switch internally to radians and get rid of this helper function!
def angular_separation_deg_to_arcsec(lon1, lat1, lon2, lat2):
    from astropy.coordinates.angle_utilities import angular_separation
    from astropy.coordinates import Angle
    lon1 = np.radians(lon1)
    lat1 = np.radians(lat1)
    lon2 = np.radians(lon2)
    lat2 = np.radians(lat2)

    separation = angular_separation(lon1, lat1, lon2, lat2)

    return Angle(separation, 'radian').to('arcsec').value


def celestial_separation_table(tool1, tool2, systems):
    c1 = celestial_results(tool1, systems, symmetric=True)
    c2 = celestial_results(tool2, systems, symmetric=True)
    table = c1.copy()
    table['separation'] = angular_separation_deg_to_arcsec(c1['lon'], c1['lat'], c2['lon'], c2['lat'])

    return table


def horizontal_filename(tool):
    fmt = 'output/tools/{}/coords_fk5_to_horizontal.txt'
    return fmt.format(tool)


def plot_filename(tool1, tool2, systems, inc_root_dir=True):
    root_dir = ""
    if inc_root_dir:
        root_dir = "output/"
    fmt = root_dir + 'plots/{}_vs_{}_for_{}_to_{}.png'
    return fmt.format(tool1, tool2, systems['in'], systems['out'])


def make_output_dir(path):
    """Make a dir in `outputs` if it doesn't exist already."""
    path = os.path.join('output', path)
    if os.path.exists(path):
        logging.debug('Directory exists: {}'.format(path))
    else:
        logging.info('Making directory: {}'.format(path))
        os.makedirs(path)


def make_tool_output_dir(tool):
    path = os.path.join('tools', tool)
    make_output_dir(path)
