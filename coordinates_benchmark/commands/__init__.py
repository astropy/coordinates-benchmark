# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Command line tool (uses sub-commands).
"""
# TODO: set up logging with click and add verbosity option
import logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

import click

# All commands are implemented as `click` sub-commands
# on the `cli` click command group.
@click.group()
def cli():
    """Astropy coordinate benchmarks utility."""
    pass

from .deploy import deploy
cli.add_command(deploy)

from .generate_skycoords import make_skycoord_table_command
cli.add_command(make_skycoord_table_command)

from .generate_observers import make_observer_table_command
cli.add_command(make_observer_table_command)

from .run_benchmark import benchmark_celestial
cli.add_command(benchmark_celestial)

from .run_benchmark import benchmark_horizontal
cli.add_command(benchmark_horizontal)

from .run_benchmark import benchmark_all
cli.add_command(benchmark_all)

from .run_benchmark import summary
cli.add_command(summary)

from .run_benchmark import plots
cli.add_command(plots)
