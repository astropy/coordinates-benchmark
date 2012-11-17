import os

import numpy as np
from matplotlib import pyplot as plt
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

if not os.path.exists('plots'):
    os.mkdir('plots')

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

    # Plot initial

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection='aitoff')
    s = ax.scatter(np.radians(ra_j2000), np.radians(dec_j2000), s=5, c=np.log10(diff), vmin=-3., vmax=1., lw=0)
    ax.grid()
    axc = fig.add_axes([0.925, 0.25, 0.025, 0.5])
    cb = fig.colorbar(s, cax=axc)
    axc.set_yticklabels('')
    cb.set_ticks([-3, -2, -1, 0, 1])
    cb.set_label('Difference in arcsec')
    axc.set_yticklabels(["0.001", "0.01", "0.1", "1", "10"])
    ax.set_title("{tool_1} vs {tool_2} for system={system}".format(tool_1=tool_1, tool_2=tool_2, system=system), y=1.1)
    fig.savefig('plots/{tool_1}_vs_{tool_2}_for_{system}.png'.format(tool_1=tool_1, tool_2=tool_2, system=system), bbox_inches='tight')


TOOLS = ['astropy', 'pyast', 'idl', 'aplpy']
for tool_1 in TOOLS:
    for tool_2 in TOOLS:
        if tool_1 == tool_2:
            continue
        for system in ['galactic', 'b1950', 'j2000', 'ecliptic']:
            make_comparison(tool_1, tool_2, system)
