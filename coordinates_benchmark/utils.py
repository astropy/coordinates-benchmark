# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Configuration parameters and utility functions and classes.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np
import logging
import itertools
from importlib import import_module
from astropy.table import Table

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

TOOLS = sorted('astropy kapteyn novas pyast palpy pyephem pyslalib astrolib pytpm'.split())
TOOL_PAIRS = [_ for _ in itertools.product(TOOLS, TOOLS)
              if _[0] < _[1]]


def _import_name(name):
    if name == 'astrolib':
        return 'astrolib.coords'
    elif name == 'pyast':
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
    tools['version'] = 'N/A'

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


def celestial_separation_table(tool1, tool2, systems):
    c1 = celestial_results(tool1, systems, symmetric=True)
    c2 = celestial_results(tool2, systems, symmetric=True)
    separation = _vicenty_dist_arcsec(c1['lon'], c1['lat'],
                                      c2['lon'], c2['lat'])
    table = c1.copy()
    table['separation'] = separation

    return table


def horizontal_filename(tool):
    fmt = 'output/tools/{}/coords_fk5_to_horizontal.txt'
    return fmt.format(tool)


def plot_filename(tool1, tool2, systems):
    fmt = 'output/plots/{}_vs_{}_for_{}_to_{}.png'
    return fmt.format(tool1, tool2, systems['in'], systems['out'])
