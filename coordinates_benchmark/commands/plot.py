"""Make plots to be included in the html page."""
import os
import logging
import numpy as np
import click
from .. import utils


def make_plot(tool1, tool2, systems,
              vmin=-3, vmax=1):
    """Make a comparison plot for celestial conversion"""
    import matplotlib.pyplot as plt

    try:
        table = utils.celestial_separation_table(tool1, tool2, systems)
    except IOError as exc:
        logging.debug(str(exc))
        return

    # Clip diff values to plotting range, otherwise values
    # below the min will not show up in the plot (probably white)
    with np.errstate(divide='ignore'):
        diff = np.clip(np.log10(table['separation']), vmin, vmax)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='aitoff')
    s = ax.scatter(np.radians(table['lon']), np.radians(table['lat']),
                   s=10, c=diff, vmin=vmin, vmax=vmax, lw=0, cmap=plt.cm.RdYlGn_r)
    ax.grid()
    axc = fig.add_axes([0.925, 0.25, 0.025, 0.5])
    cb = fig.colorbar(s, cax=axc)
    axc.set_yticklabels('')
    cb.set_ticks([-3, -2, -1, 0, 1])
    cb.set_label('Difference in arcsec')
    axc.set_yticklabels(["0.001", "0.01", "0.1", "1", "10"])

    fmt = '{} vs {} for conversion {} -> {}'
    title = fmt.format(tool1, tool2, systems['in'], systems['out'])
    ax.set_title(title, y=1.1)

    filename = utils.plot_filename(tool1, tool2, systems)
    logging.info('Writing {}'.format(filename))
    fig.savefig(filename, bbox_inches='tight')

    plt.close(fig)


@click.command(name='plots')
@click.option('--tools', default='all',
              help='Which tools to benchmark.')
def plots_command(tools):
    """Create plots to illustrate results"""
    tools = utils.select_tools(tools)

    # Make sure the output folder for plots exists
    if not os.path.exists('output'):
        os.mkdir('output')
    if not os.path.exists('output/plots'):
        os.mkdir('output/plots')

    for tool in tools:
        logging.info('Making plots for tool {tool}'.format(tool=tool))
        other_tools = [_[1] for _ in utils.TOOL_PAIRS if _[0] == tool]
        for tool2 in other_tools:
            for systems in utils.CELESTIAL_CONVERSIONS:
                make_plot(tool, tool2, systems)
