"""Print summary table for sky distance distributions
for different tools / systems."""
import os

import numpy as np
from astropy.coordinates.angle_utilities import vicenty_dist

def vicenty_dist_deg(lon1, lat1, lon2, lat2):

    lon1 = np.radians(lon1)
    lat1 = np.radians(lat1)
    lon2 = np.radians(lon2)
    lat2 = np.radians(lat2)

    sdlon = np.sin(lon2 - lon1)
    cdlon = np.cos(lon2 - lon1)

    num1 = np.cos(lat2) * sdlon
    num2 = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * cdlon
    denominator = np.sin(lat1) * np.sin(lat2) + np.cos(lat1) * np.cos(lat2) * cdlon

    return np.degrees(np.arctan2((num1 ** 2 + num2 ** 2) ** 0.5, denominator))

initial = np.loadtxt('initial_coords.txt')
ra_j2000, dec_j2000 = initial[:,0], initial[:,1]
ra_j2000[ra_j2000 > 180.] -= 360.

def make_comparison(tool_1, tool_2, system):

    try:

        coords = np.loadtxt('{tool}/coords_{system}.txt'.format(tool=tool_1,
                                                                system=system))
        lon1, lat1 = coords[:,0], coords[:,1]
        lon1[lon1 > 180.] -= 360.

        coords = np.loadtxt('{tool}/coords_{system}.txt'.format(tool=tool_2,
                                                                system=system))
        lon2, lat2 = coords[:,0], coords[:,1]
        lon2[lon2 > 280.] -= 360.

    except IOError:

        return

    diff = vicenty_dist_deg(lon1, lat1, lon2, lat2) * 3600.

    median = np.median(diff)
    mean = np.mean(diff)
    max = np.max(diff)
    std = np.std(diff)
    fmt = ('{tool_1:10s} {tool_2:10s} {system:10s} '
           '{median:12.6f} {mean:12.6f} {max:12.6f} {std:12.6f}')
    print(fmt.format(**locals()))

    fmt3 = '{median:12s} {mean:12s} {max:12s} {std:12s}'

fmt = ('{tool_1:10s} {tool_2:10s} {system:10s} '
       '{median:12s} {mean:12s} {max:12s} {std:12s}')
labels = dict(tool_1="Tool 1", tool_2="Tool 2", system='System',
              median='Median', mean='Mean', max='Max', std='Std.Dev.')
print('')
print('Summary of differences in arcseconds.')
print('')
print(fmt.format(**labels))
print('-' * 84)

TOOLS = ['astropy', 'pyast', 'idl', 'aplpy']
for tool_1 in TOOLS:
    for tool_2 in TOOLS:
        if tool_1 == tool_2:
            continue
        for system in ['galactic', 'b1950', 'j2000', 'ecliptic']:
            make_comparison(tool_1, tool_2, system)
