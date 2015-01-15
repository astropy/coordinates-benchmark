# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Run the coordinates benchmark"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import os
import time
import itertools
import imp
import logging
import numpy as np
import click
from .. import utils
from ..utils import _vicenty_dist_arcsec
from ..config import CELESTIAL_CONVERSIONS, CELESTIAL_SYSTEMS
from ..config import TOOLS, TOOL_PAIRS
from ..config import select_tools
from ..config import FLOAT_FORMAT_OUTPUT, TABLE_FORMAT


class CoordinatesBenchmark():
    """Summarize all available benchmark results in a txt and html file"""

    def run_celestial_conversions(self, tool, report_speed):
        """Run celestial conversion benchmark for one given tool"""
        try:
            tool_module = imp.load_source('dummy', 'tools/%s/convert.py' % tool)
        except (IOError, ImportError):
            logging.warning("Benchmarks for {0} cannot be run because tools/{0}/convert.py "
                            "could not be imported.".format(tool))
            return
        logging.info('Running celestial conversions using %s' % tool)
        coords = self._read_coords('input/initial_coords.txt')

        for systems in CELESTIAL_CONVERSIONS:
            timestamp = time.time()
            out_coords = tool_module.convert(coords, systems)
            duration = time.time() - timestamp
            if out_coords == None:
                logging.info('Skipping %s -> %s. Not supported.' %
                             (systems['in'], systems['out']))
                continue
            #if report_speed:
            #    f_speed.write('%15s %10s %10s %10.6f\n' %
            #                  (tool, systems['in'], systems['out'], duration))
            filename = 'tools/%s/%s_to_%s.txt' % (tool, systems['in'], systems['out'])
            self._write_coords(filename, out_coords)

    @staticmethod
    def _accuracy_color(mean):
        """Accuracy color for a given mean difference in arcsec"""
        if mean > 1.:
            color='red'
        elif mean > 0.01:
            color='orange'
        else:
            color='green'
        return color

    def make_plot(self, tool1, tool2, system1, system2,
                  vmin=-3, vmax=1):
        """Make a comparison plot for celestial conversion"""
        import matplotlib.pyplot as plt

        try:
            filename1 = CoordinatesBenchmark._celestial_filename(tool1, system1, system2)
            # For plotting we need longitudes in the symmetric range -180 to +180
            coords1 = self._read_coords(filename1, symmetric=True)
            filename2 = CoordinatesBenchmark._celestial_filename(tool2, system1, system2)
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
        filename = CoordinatesBenchmark._plot_filename(tool1, tool2, system1, system2)
        logging.info('Writing %s' % filename)
        fig.savefig(os.path.join('output', filename), bbox_inches='tight')
        plt.close(fig)

    @staticmethod
    def _plot_filename(tool1, tool2, system1, system2):
        return 'plots/{tool1}_vs_{tool2}_for_{system1}_to_{system2}.png'.format(**locals())

    @staticmethod
    def _celestial_filename(tool, in_system, out_system):
        return 'tools/%s/%s_to_%s.txt' % (tool, in_system, out_system)

    def summary(self, txt_filename='summary.txt', html_filename='summary.html', html_matrix_filename='summary_matrix.html'):
        """Write txt and html summary"""
        f_txt = open(os.path.join('output', txt_filename), 'w')
        f_html = open(os.path.join('output', html_filename), 'w')

        fmt = ('{tool1:10s} {tool2:10s} {system1:10s} {system2:10s} '
               '{median:>12s} {mean:>12s} {max:>12s} {std:>12s}')

        labels = dict(tool1="Tool 1", tool2="Tool 2", system1='System 1', system2='System 2',
                      median='Median', mean='Mean', max='Max', std='Std.Dev.')

        f_txt.write(fmt.format(**labels) + "\n")
        f_txt.write('-' * 94 + "\n")

        self._html_header(f_html)

        f_html.write('<p align="center"><a href="summary_matrix.html"><b>See also matrix view</b></a></p>')

        for systems in CELESTIAL_CONVERSIONS:
            logging.info('Summarizing celestial conversions: %s -> %s' % (systems['in'], systems['out']))

            f_html.write("<a name='{in}_{out}'></a><a class='anchor' href='#{in}_{out}'><h2>{in} to {out}</h2></a>".format(**systems))
            f_html.write("<table align='center'>\n")
            f_html.write("  <tr>\n")
            f_html.write("    <th width=80>Tool 1</th>\n")
            f_html.write("    <th width=80>Tool 2</th>\n")
            f_html.write("    <th width=80>System 1</th>\n")
            f_html.write("    <th width=80>System 2</th>\n")
            f_html.write("    <th width=80>Median</th>\n")
            f_html.write("    <th width=80>Mean</th>\n")
            f_html.write("    <th width=80>Max</th>\n")
            f_html.write("    <th width=80>Std. Dev.</th>\n")
            f_html.write("    <th width=80>Plot</th>\n")
            f_html.write("  </tr>\n")

            for tool1, tool2 in TOOL_PAIRS:
                self._compare_celestial(tool1, tool2, systems['in'],
                                        systems['out'], f_txt, f_html)

            f_html.write("   </table>\n")

        self._html_footer(f_html)

        f_html.close()
        f_txt.close()

        logging.info('Writing output/%s' % txt_filename)
        logging.info('Writing output/%s' % html_filename)

        # Write comparison matrix

        f_matrix_html = open(os.path.join('output', html_matrix_filename), 'w')

        self._html_header(f_matrix_html)

        f_matrix_html.write('<p align="center"><a href="summary.html"><b>See also list view</b></a></p>')

        for tool in TOOLS:
            for line in self.tool_comparison_table(tool):
                f_matrix_html.write(line)

        self._html_footer(f_matrix_html)

        f_matrix_html.close()

        logging.info('Writing output/%s' % html_matrix_filename)

    def _html_header(self, file_handle):
        file_handle.write("<html>\n")
        file_handle.write("   <head>\n")
        file_handle.write("      <link href='style.css' rel='stylesheet' type='text/css'\n")
        file_handle.write("   </head>\n")
        file_handle.write("   <body>\n")
        file_handle.write("      <p align='center'>Summary of differences in arcseconds</p>\n")
        file_handle.write("      <p align='center'>Green means < 10 milli-arcsec, orange < 1 arcsec and red > 1 arcsec</p>\n")

    def _html_footer(self, file_handle):
        file_handle.write("   </body>\n")
        file_handle.write("</html>\n")

    def _compare_celestial(self, tool1, tool2, system1, system2, f_txt, f_html):
        try:
            filename1 = CoordinatesBenchmark._celestial_filename(tool1, system1, system2)
            # For plotting we need longitudes in the symmetric range -180 to +180
            coords1 = self._read_coords(filename1, symmetric=True)
            filename2 = CoordinatesBenchmark._celestial_filename(tool2, system1, system2)
            coords2 = self._read_coords(filename2, symmetric=True)
            diff = _vicenty_dist_arcsec(coords1['lon'], coords1['lat'],
                                        coords2['lon'], coords2['lat'])
        except IOError:
            return

        # Compute stats
        median = np.median(diff)
        mean = np.mean(diff)
        max = np.max(diff)
        std = np.std(diff)

        # Print out stats
        fmt = ('{tool1:10s} {tool2:10s} {system1:10s} {system2:10s} '
               '{median:12.6f} {mean:12.6f} {max:12.6f} {std:12.6f}')
        f_txt.write(fmt.format(**locals()) + "\n")

        # Write out to HTML
        color = CoordinatesBenchmark._accuracy_color(mean)
        plot_filename = CoordinatesBenchmark._plot_filename(tool1, tool2, system1, system2)

        f_html.write("  <tr>\n")
        f_html.write("    <td align='center'>{tool1:10s}</td>\n".format(tool1=tool1))
        f_html.write("    <td align='center'>{tool2:10s}</td>\n".format(tool2=tool2))
        f_html.write("    <td align='center'>{system1:10s}</td>\n".format(system1=system1))
        f_html.write("    <td align='center'>{system2:10s}</td>\n".format(system2=system2))
        f_html.write("    <td align='right' class='{color}'>{median:12.6f}</td>\n".format(color=color, median=median))
        f_html.write("    <td align='right' class='{color}'>{mean:12.6f}</td>\n".format(color=color, mean=mean))
        f_html.write("    <td align='right' class='{color}'>{max:12.6f}</td>\n".format(color=color, max=max))
        f_html.write("    <td align='right' class='{color}'>{std:12.6f}</td>\n".format(color=color, std=std))
        f_html.write("    <td align='center'><a href='{plot_filename}'>Plot</a></td>\n".format(plot_filename=plot_filename))
        f_html.write("  </tr>\n")

    def tool_comparison_table(self, tool):
        other_tools = sorted(t for t in TOOLS if t != tool)

        yield '<a name="{0}"></a><a class="anchor" href="#{0}"><h2>{0}</h2></a>'.format(tool)
        yield '<table align="center">'
        yield '<tr><th width="80">'
        for t in other_tools:
            yield '<th width="80">{}'.format(t)
        pairs = itertools.permutations(CELESTIAL_SYSTEMS, 2)
        for in_system, out_system in pairs:
            filename = self._celestial_filename(tool, in_system, out_system)
            try:
                c = self._read_coords(filename)
            except IOError:
                continue
            yield '<tr><th>{} &#8594; {}'.format(in_system, out_system)
            for t in other_tools:
                filename = self._celestial_filename(t, in_system, out_system)
                try:
                    d = self._read_coords(filename)
                except IOError:
                    yield '<td> &mdash;'
                    continue
                diff = _vicenty_dist_arcsec(c['lon'], c['lat'],
                                            d['lon'], d['lat'])
                mean = np.mean(diff)
                color = CoordinatesBenchmark._accuracy_color(mean)
                fmt = '<td class="{}">{:.6f}<br>{:.6f}<br>{:.6f}<br>{:.6f}'
                yield fmt.format(color, np.median(diff), mean,
                                 np.max(diff), np.std(diff))

            yield '<th align="left">Median<br>Mean<br>Max<br>Std.Dev.'
        yield '</tr>'
        yield '</table>'


benchmark = CoordinatesBenchmark()


@click.command()
@click.option('--tools', default='all',
              help='Which tools to benchmark.')
def benchmark_celestial(tools):
    """Run celestial coordinate conversions."""
    # TODO: implement command line option for speed reporting
    report_speed = False

    for tool in tools:
        benchmark.run_celestial_conversions(tool, report_speed=report_speed)


@click.command()
@click.option('--tools', default='all',
              help='Which tools to benchmark.')
def benchmark_horizontal(tools):
    """Run horizontal coordinate conversions."""
    tools = select_tools(tools)

    positions = utils.get_positions()
    observers = utils.get_observers()

    for tool in tools:
        module = utils.get_test_module(tool)

        if not hasattr(module, 'convert_horizontal'):
            logging.warning('{} does not support `convert_horizontal`'.format(tool))
            continue

        logging.info('Running `convert_horizontal` for tool `{}`'.format(tool))
        results = module.convert_horizontal(positions, observers)

        for col in ['az', 'alt']:
            results[col].format = FLOAT_FORMAT_OUTPUT

        filename = 'output/tools/{}/coords_fk5_to_horizontal.txt'.format(tool)
        logging.info('Writing {}'.format(filename))
        results.write(filename, format=TABLE_FORMAT)



@click.command()
def benchmark_all(tools):
    """Run coordinate benchmarks."""
    benchmark_celestial(tools)
    benchmark_horizontal(tools)


@click.command()
def summary():
    """Summarize all results into a few stats"""
    benchmark.summary()


@click.command()
def plots(tools):
    """Create plots to illustrate results"""
    if not os.path.exists('output'):
        os.mkdir('output')
    if not os.path.exists('output/plots'):
        os.mkdir('output/plots')

    for tool in tools:
        logging.info('Making plots for tool {tool}'.format(tool=tool))
        other_tools = [_[1] for _ in TOOL_PAIRS if _[0] == tool]
        for tool2 in other_tools:
            for systems in CELESTIAL_CONVERSIONS:
                benchmark.make_plot(tool, tool2, systems['in'], systems['out'])
