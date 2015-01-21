"""Make a html page summarising the results."""
import logging
import os
import itertools
import numpy as np
import click
from .. import utils


def _accuracy_color(mean):
    """Accuracy color for a given mean difference in arcsec"""
    if mean > 1.:
        color='red'
    elif mean > 0.01:
        color='orange'
    else:
        color='green'
    return color


def write_html_header(fh):
    fh.write("<html>\n")
    fh.write("   <head>\n")
    fh.write("      <link href='style.css' rel='stylesheet' type='text/css'\n")
    fh.write("   </head>\n")
    fh.write("   <body>\n")
    fh.write("      <p align='center'>Summary of differences in arcseconds</p>\n")
    fh.write("      <p align='center'>Green means < 10 milli-arcsec, orange < 1 arcsec and red > 1 arcsec</p>\n")


def write_html_footer(fh):
    fh.write("   </body>\n")
    fh.write("</html>\n")


def write_html_table_header(fh, systems):
    fh.write("<a name='{in}_{out}'></a><a class='anchor' href='#{in}_{out}'><h2>{in} to {out}</h2></a>".format(**systems))
    fh.write("<table align='center'>\n")
    fh.write("  <tr>\n")
    fh.write("    <th width=80>Tool 1</th>\n")
    fh.write("    <th width=80>Tool 2</th>\n")
    fh.write("    <th width=80>System 1</th>\n")
    fh.write("    <th width=80>System 2</th>\n")
    fh.write("    <th width=80>Median</th>\n")
    fh.write("    <th width=80>Mean</th>\n")
    fh.write("    <th width=80>Max</th>\n")
    fh.write("    <th width=80>Std. Dev.</th>\n")
    fh.write("    <th width=80>Plot</th>\n")
    fh.write("  </tr>\n")


def _compare_celestial(tool1, tool2, systems, f_txt, f_html):

    try:
        table = utils.celestial_separation_table(tool1, tool2, systems)
    except IOError as exc:
        logging.debug(str(exc))
        return

    # Compute stats
    diff = table['separation']
    median = np.median(diff)
    mean = np.mean(diff)
    max = np.max(diff)
    std = np.std(diff)

    # Print out stats
    system1, system2 = systems['in'], systems['out']
    fmt = ('{tool1:10s} {tool2:10s} {system1:10s} {system2:10s} '
           '{median:12.6f} {mean:12.6f} {max:12.6f} {std:12.6f}')
    f_txt.write(fmt.format(**locals()) + "\n")

    # Write out to HTML
    color = _accuracy_color(mean)
    plot_filename = utils.plot_filename(tool1, tool2, systems)

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


def write_tool_comparison_table(fh, tool):
    other_tools = sorted(t for t in utils.TOOLS if t != tool)

    fh.write('<a name="{0}"></a><a class="anchor" href="#{0}"><h2>{0}</h2></a>\n'.format(tool))
    fh.write('<table align="center">\n')
    fh.write('<tr><th width="80">\n')
    for t in other_tools:
        fh.write('<th width="80">{}\n'.format(t))
    pairs = itertools.permutations(utils.CELESTIAL_SYSTEMS, 2)
    for systems in pairs:
        systems = {'in': systems[0], 'out': systems[1]}
        try:
            c = utils.celestial_results(tool, systems)
        except IOError:
            continue

        fh.write('<tr><th>{} &#8594; {}\n'.format(systems['in'], systems['out']))
        for t in other_tools:
            try:
                d = utils.celestial_results(t, systems)
            except IOError:
                fh.write('<td> &mdash;\n')
                continue
            diff = utils.our_angular_separation(c['lon'], c['lat'], d['lon'], d['lat'])
            mean = np.mean(diff)
            color = _accuracy_color(mean)
            fmt = '<td class="{}">{:.6f}<br>{:.6f}<br>{:.6f}<br>{:.6f}'
            fh.write(fmt.format(color, np.median(diff), mean,
                                np.max(diff), np.std(diff)))

        fh.write('<th align="left">Median<br>Mean<br>Max<br>Std.Dev.\n')
    fh.write('</tr>\n')
    fh.write('</table>\n')


def summary(txt_filename='summary.txt',
            html_filename='summary.html',
            html_matrix_filename='summary_matrix.html'):
    """Write txt and html summary"""
    f_txt = open(os.path.join('output', txt_filename), 'w')
    f_html = open(os.path.join('output', html_filename), 'w')

    fmt = ('{tool1:10s} {tool2:10s} {system1:10s} {system2:10s} '
           '{median:>12s} {mean:>12s} {max:>12s} {std:>12s}')

    labels = dict(tool1="Tool 1", tool2="Tool 2", system1='System 1', system2='System 2',
                  median='Median', mean='Mean', max='Max', std='Std.Dev.')

    f_txt.write(fmt.format(**labels) + "\n")
    f_txt.write('-' * 94 + "\n")

    write_html_header(f_html)

    f_html.write('<p align="center"><a href="summary_matrix.html"><b>See also matrix view</b></a></p>')

    for systems in utils.CELESTIAL_CONVERSIONS:
        logging.info('Summarizing celestial conversions: %s -> %s' % (systems['in'], systems['out']))

        write_html_table_header(f_html, systems)

        for tool1, tool2 in utils.TOOL_PAIRS:
            _compare_celestial(tool1, tool2, systems, f_txt, f_html)

        f_html.write("   </table>\n")

    write_html_footer(f_html)

    f_html.close()
    f_txt.close()

    logging.info('Writing output/%s' % txt_filename)
    logging.info('Writing output/%s' % html_filename)

    # Write comparison matrix

    f_matrix_html = open(os.path.join('output', html_matrix_filename), 'w')

    write_html_header(f_matrix_html)

    f_matrix_html.write('<p align="center"><a href="summary.html"><b>See also list view</b></a></p>')

    for tool in utils.TOOLS:
        write_tool_comparison_table(f_matrix_html, tool)

    write_html_footer(f_matrix_html)

    f_matrix_html.close()

    logging.info('Writing output/%s' % html_matrix_filename)


def copy_static():
    """Copy static files to the output folder"""
    import shutil
    repo_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
    www_dir = os.path.join(repo_dir, 'coordinates_benchmark', 'www')
    output_dir = os.path.join(repo_dir, 'output')
    filenames = ['style.css']
    for filename in filenames:
        shutil.copy(os.path.join(www_dir, filename),
                    os.path.join(output_dir, filename))


@click.command()
def summary_celestial():
    """For now: summary and HTML page."""
    # """Summarize all results into a few stats"""
    summary()
    copy_static()
