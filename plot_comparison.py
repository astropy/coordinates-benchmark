import os

import numpy as np
from matplotlib import pyplot as plt

if not os.path.exists('plots'):
    os.mkdir('plots')

initial = np.loadtxt('initial_coords.txt')
ra_j2000, dec_j2000 = initial[:,0], initial[:,1]
ra_j2000[ra_j2000 > 180.] -= 360.

# Plot initial

fig = plt.figure()
ax = fig.add_subplot(1,1,1, projection='aitoff')
ax.scatter(np.radians(ra_j2000), np.radians(dec_j2000), s=2)
ax.grid()
fig.savefig('plots/initial.png')

def make_comparison(tool_1, tool_2, system):

    try:
        
        coords = np.loadtxt('{tool}/coords_{system}.txt'.format(tool=tool_1,
                                                            system=system), delimiter="," if tool_1 == 'idl' else None)
        lon1, lat1 = coords[:,0], coords[:,1]
        lon1[lon1 > 180.] -= 360.

        coords = np.loadtxt('{tool}/coords_{system}.txt'.format(tool=tool_2,
                                                            system=system), delimiter="," if tool_2 == 'idl' else None)
        lon2, lat2 = coords[:,0], coords[:,1]
        lon2[lon2 > 280.] -= 360.
    
    except IOError:
    
        return

    dlon = (lon1 - lon2) * np.cos(0.5 * (lat1 + lat2))
    dlat = (lat1 - lat2)
    diff = np.sqrt(dlon**2 + dlat**2) * 3600.
    
    md = diff.max()
    
    # Plot initial

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection='aitoff')
    s = ax.scatter(np.radians(ra_j2000), np.radians(dec_j2000), s=5, c=np.log10(diff), vmin=-2., vmax=2., lw=0)
    ax.grid()
    axc = fig.add_axes([0.925, 0.25, 0.025, 0.5])
    cb = fig.colorbar(s, cax=axc)
    axc.set_yticklabels('')
    cb.set_ticks([-2,-1,0,1,2])
    cb.set_label('Difference in arcsec')
    axc.set_yticklabels(["0.01", "0.1", "1", "10", "100"])
    ax.set_title("{tool_1} vs {tool_2} for system={system}".format(tool_1=tool_1, tool_2=tool_2, system=system), y=1.1)
    fig.savefig('plots/{tool_1}_vs_{tool_2}_for_{system}.png'.format(tool_1=tool_1, tool_2=tool_2, system=system), bbox_inches='tight')
    

TOOLS = ['astropy', 'pyast', 'idl']
for tool_1 in TOOLS:
    for tool_2 in TOOLS:
        if tool_1 == tool_2:
            continue
        for system in ['galactic', 'fk4', 'fk5', 'ecliptic']:
            make_comparison(tool_1, tool_2, system)
            