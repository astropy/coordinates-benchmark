# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Configuration parameters.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import itertools
from importlib import import_module
from astropy.table import Table

TABLE_FORMAT = 'ascii.fixed_width_two_line'
FLOAT_FORMAT = '%20.15f'


# Make a list of celestial conversions to check
# We simply list all possible combinations here,
# systems not supported by certain tools are simply skipped later
CELESTIAL_SYSTEMS = 'fk5 fk4 icrs galactic ecliptic'.split()
CELESTIAL_CONVERSIONS = itertools.product(CELESTIAL_SYSTEMS, CELESTIAL_SYSTEMS)
CELESTIAL_CONVERSIONS = [dict(zip(['in', 'out'], _))
                         for _ in CELESTIAL_CONVERSIONS
                         if _[0] != _[1]]

TOOLS = 'astropy kapteyn novas pyast palpy pyephem pyslalib astrolib pytpm idl'.split()
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
            # module = import_module('coordinates_benchmark.tools.' + tool['name'])
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
