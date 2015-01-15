"""Make plots to be included in the html page."""
import os
import logging
import numpy as np
import click
from .. import utils
from ..utils import _vicenty_dist_arcsec


def make_plot(self, tool1, tool2, system1, system2,
              vmin=-3, vmax=1):
    """Make a comparison plot for celestial conversion"""
    import matplotlib.pyplot as plt

    try:

        filename1 = utils.celestial_filename(tool1, system1, system2)
        # For plotting we need longitudes in the symmetric range -180 to +180
        coords1 = self._read_coords(filename1, symmetric=True)
        filename2 = utils.celestial_filename(tool2, system1, system2)
        coords2 = self._read_coords(filename2, symmetric=True)
        diff = _vicenty_dist_arcsec(coords1['lon'], coords1['lat'],
                                    coords2['lon'], coords2['lat'])
    except IOError:
        return

    # Clip diff values to plotting range, otherwise values
    # below the min will not show up in the plot (probably white)
    diff = np.clip(np.log10(diff), vmin, vmax)

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection='aitoff')
    s = ax.scatter(np.radians(coords1['lon']), np.radians(coords1['lat']),
                   s=10, c=diff, vmin=vmin, vmax=vmax, lw=0, cmap=plt.cm.RdYlGn_r)
    ax.grid()
    axc = fig.add_axes([0.925, 0.25, 0.025, 0.5])
    cb = fig.colorbar(s, cax=axc)
    axc.set_yticklabels('')
    cb.set_ticks([-3, -2, -1, 0, 1])
    cb.set_label('Difference in arcsec')
    axc.set_yticklabels(["0.001", "0.01", "0.1", "1", "10"])
    ax.set_title("{tool1} vs {tool2} for conversion {system1} -> {system2}".format(**locals()), y=1.1)
    filename = utils.plot_filename(tool1, tool2, system1, system2)
    logging.info('Writing %s' % filename)
    fig.savefig(os.path.join('output', filename), bbox_inches='tight')
    plt.close(fig)


@click.command(name='plots')
def plots_command(tools):
    """Create plots to illustrate results"""
    if not os.path.exists('output'):
        os.mkdir('output')
    if not os.path.exists('output/plots'):
        os.mkdir('output/plots')

    for tool in tools:
        logging.info('Making plots for tool {tool}'.format(tool=tool))
        other_tools = [_[1] for _ in utils.TOOL_PAIRS if _[0] == tool]
        for tool2 in other_tools:
            for systems in utils.CELESTIAL_CONVERSIONS:
                make_plot(tool, tool2, systems['in'], systems['out'])
