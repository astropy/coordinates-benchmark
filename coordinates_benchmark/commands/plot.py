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

    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(1, 1, 1, projection='aitoff')
    s = ax.scatter(np.radians(table['lon']), np.radians(table['lat']),
                   s=10, c=diff, vmin=vmin, vmax=vmax, lw=0, cmap=plt.cm.RdYlGn_r)
    ax.grid()
    axc = fig.add_axes([0.2, 0.1, 0.6, 0.03])
    cb = fig.colorbar(s, cax=axc, orientation='horizontal')
    cb.set_ticks([-3, -2, -1, 0, 1])
    cb.set_label('Difference in arcsec')

    fmt = '{} vs {} for conversion {} -> {}'
    title = fmt.format(tool1, tool2, systems['in'], systems['out'])
    ax.set_title(title, y=1.1)

    filename = utils.plot_filename(tool1, tool2, systems)
    logging.info('Writing {}'.format(filename))

    # We don't use bbox_inches='tight' here to make sure that the image size
    # is the same for different versions of matplotlib, freetype, and different
    # platforms (otherwise the image comparison when deploying fails).
    fig.savefig(filename)

    plt.close(fig)


@click.command(name='plots')
@click.option('--tools', default='all',
              help='Which tools to benchmark.')
def plots_command(tools):
    """Create plots to illustrate results"""
    utils.make_output_dir('plots')
    tools = utils.select_tools(tools)

    for tool in tools:
        logging.info('Making plots for tool {tool}'.format(tool=tool))
        other_tools = [_[1] for _ in utils.TOOL_PAIRS if _[0] == tool]
        for tool2 in other_tools:
            for systems in utils.CELESTIAL_CONVERSIONS:
                make_plot(tool, tool2, systems)
