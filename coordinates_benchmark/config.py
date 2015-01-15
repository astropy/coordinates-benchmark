# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Configuration parameters.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import itertools

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
