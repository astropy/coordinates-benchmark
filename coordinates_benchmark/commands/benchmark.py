# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Run the coordinates benchmark"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import logging
import click
from .. import utils


@click.command()
@click.option('--tools', default='all',
              help='Which tools to benchmark.')
def benchmark_celestial(tools):
    """Run celestial coordinate conversions."""
    tools = utils.select_tools(tools)

    positions = utils.get_positions()

    for tool in tools:
        utils.make_tool_output_dir(tool)
        module = utils.get_test_module(tool)

        if not hasattr(module, 'transform_celestial'):
            logging.warning('{} does not support `transform_celestial`'.format(tool))
            continue

        logging.info('Running `transform_celestial` for tool `{}`'.format(tool))
        for systems in utils.CELESTIAL_CONVERSIONS:

            supported_systems = utils.CELESTIAL_SYSTEMS
            if hasattr(module, 'SUPPORTED_SYSTEMS'):
                supported_systems = module.SUPPORTED_SYSTEMS

            if not set(systems.values()).issubset(supported_systems):
                logging.debug('Skipping {}'.format(systems))
                continue

            results = module.transform_celestial(positions, systems)

            results['lon'] %= 360

            for col in ['lon', 'lat']:
                results[col].format = utils.FLOAT_FORMAT_OUTPUT

            filename = utils.celestial_filename(tool, systems)
            logging.info('Writing {}'.format(filename))
            results.write(filename, format=utils.TABLE_FORMAT)


@click.command()
@click.option('--tools', default='all',
              help='Which tools to benchmark.')
def benchmark_horizontal(tools):
    """Run horizontal coordinate conversions."""
    tools = utils.select_tools(tools)

    # TODO: for now we're running on a small subset for debugging
    positions = utils.get_positions(use_subset=True)
    observers = utils.get_observers(use_subset=True)

    for tool in tools:
        utils.make_tool_output_dir(tool)
        module = utils.get_test_module(tool)

        if not hasattr(module, 'convert_horizontal'):
            logging.warning('{} does not support `convert_horizontal`'.format(tool))
            continue

        logging.info('Running `convert_horizontal` for tool `{}`'.format(tool))
        results = module.convert_horizontal(positions, observers)
        results['az'] %= 360

        for col in ['az', 'alt']:
            results[col].format = utils.FLOAT_FORMAT_OUTPUT

        filename = utils.horizontal_filename(tool)
        logging.info('Writing {}'.format(filename))
        results.write(filename, format=utils.TABLE_FORMAT)


@click.command()
def benchmark_all():
    """Run coordinate benchmarks."""
    benchmark_celestial()
    benchmark_horizontal()
