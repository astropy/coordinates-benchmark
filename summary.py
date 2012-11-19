"""
Print summary table for sky distance distributions for different tools and
systems. This script can also produce plots of the differences as a function
of position on the sky, by running::

    python summary.py --plot

Disclaimer: this was written quickly and could be significantly improved...
            pull requests welcome! :-)
"""

import os
import sys

import numpy as np
from matplotlib import pyplot as plt
from astropy.coordinates.angle_utilities import vicenty_dist

plot = '--plot' in sys.argv[1:]
html = '--html' in sys.argv[1:]

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

def compare(tool_1, tool_2, system, plot=False):

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

    # Compute stats

    median = np.median(diff)
    mean = np.mean(diff)
    max = np.max(diff)
    std = np.std(diff)

    # Print out stats

    fmt = ('{tool_1:10s} {tool_2:10s} {system:10s} '
           '{median:12.6f} {mean:12.6f} {max:12.6f} {std:12.6f}')
    print(fmt.format(**locals()))
    f_txt.write(fmt.format(**locals()) + "\n")

    # Write out to HTML

    if mean > 1.:
        color='red'
    elif mean > 0.01:
        color='orange'
    else:
        color='green'

    f_html.write("  <tr>\n")
    f_html.write("    <td align='center'>{tool_1:10s}</td>\n".format(tool_1=tool_1))
    f_html.write("    <td align='center'>{tool_2:10s}</td>\n".format(tool_2=tool_2))
    f_html.write("    <td align='center'>{system:10s}</td>\n".format(system=system))
    f_html.write("    <td align='right' class='{color}'>{median:12.6f}</td>\n".format(color=color, median=median))
    f_html.write("    <td align='right' class='{color}'>{mean:12.6f}</td>\n".format(color=color, mean=mean))
    f_html.write("    <td align='right' class='{color}'>{max:12.6f}</td>\n".format(color=color, max=max))
    f_html.write("    <td align='right' class='{color}'>{std:12.6f}</td>\n".format(color=color, std=std))

    if plot:
        f_html.write("    <td align='center'><a href='plots/{tool_1}_vs_{tool_2}_for_{system}.png'>PNG</a></td>\n".format(tool_1=tool_1, tool_2=tool_2, system=system))

    f_html.write("  </tr>\n")

    # Make plot

    if plot:

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1, projection='aitoff')
        s = ax.scatter(np.radians(ra_j2000), np.radians(dec_j2000), s=5, c=np.log10(diff), vmin=-3., vmax=1., lw=0, cmap=plt.cm.RdYlGn_r)
        ax.grid()
        axc = fig.add_axes([0.925, 0.25, 0.025, 0.5])
        cb = fig.colorbar(s, cax=axc)
        axc.set_yticklabels('')
        cb.set_ticks([-3, -2, -1, 0, 1])
        cb.set_label('Difference in arcsec')
        axc.set_yticklabels(["0.001", "0.01", "0.1", "1", "10"])
        ax.set_title("{tool_1} vs {tool_2} for system={system}".format(tool_1=tool_1, tool_2=tool_2, system=system), y=1.1)
        fig.savefig('plots/{tool_1}_vs_{tool_2}_for_{system}.png'.format(tool_1=tool_1, tool_2=tool_2, system=system), bbox_inches='tight')

fmt = ('{tool_1:10s} {tool_2:10s} {system:10s} '
       '{median:12s} {mean:12s} {max:12s} {std:12s}')
labels = dict(tool_1="Tool 1", tool_2="Tool 2", system='System',
              median='Median', mean='Mean', max='Max', std='Std.Dev.')
print('')
print('Summary of differences in arcseconds.')
print('')
print(fmt.format(**labels))
print('-' * 84)

if not os.path.exists('plots'):
    os.mkdir('plots')

f_txt = open('summary.txt', 'wb')

f_txt.write(fmt.format(**labels) + "\n")
f_txt.write('-' * 84 + "\n")

f_html = open('summary.html', 'wb')

f_html.write("<html>\n")
f_html.write("   <head>\n")
f_html.write("      <link href='style.css' rel='stylesheet' type='text/css'\n")
f_html.write("   </head>\n")

f_html.write("   <body>\n")

f_html.write("<p align='center'>Differences are given in arcseconds</p>\n")

f_html.write("<table align='center'>\n")

f_html.write("  <tr>\n")
f_html.write("    <th width=80>Tool 1</th>\n")
f_html.write("    <th width=80>Tool 2</th>\n")
f_html.write("    <th width=80>System</th>\n")
f_html.write("    <th width=80>Median</th>\n")
f_html.write("    <th width=80>Mean</th>\n")
f_html.write("    <th width=80>Max</th>\n")
f_html.write("    <th width=80>Std. Dev.</th>\n")
if plot:
    f_html.write("    <th width=80>Plot</th>\n")
f_html.write("  </tr>\n")

TOOLS = ['astropy', 'pyast', 'idl', 'aplpy', 'tpm', 'kapteyn']
for tool_1 in TOOLS:
    for tool_2 in TOOLS:
        if tool_1 == tool_2:
            continue
        for system in ['galactic', 'b1950', 'j2000', 'ecliptic']:
            compare(tool_1, tool_2, system, plot)

f_html.write("   </body>\n")
f_html.write("</html>\n")
