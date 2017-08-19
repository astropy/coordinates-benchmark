# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function

import os
import sys
import shutil
import tempfile
import subprocess
import click


def run(cmd, verbose=False):
    if verbose:
        print("EXEC: {0}".format(cmd))
        retcode = subprocess.call(cmd, shell=True)
    else:
        retcode = subprocess.call(cmd, shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    assert retcode == 0


@click.command()
@click.option('--token', help='Github token')
@click.option('--verbose', is_flag=True, help='Whether to display the git commands and their output')
def deploy(token, verbose):
    """Deploy HTML output to Github pages."""

    if not token:
        print("Github token not set")
        sys.exit(1)

    tmpdir = tempfile.mkdtemp()
    tmpout = os.path.join(tmpdir, 'output')
    shutil.copytree('output', tmpout)
    start_dir = os.path.abspath('.')

    try:
        os.chdir(tmpout)
        run('git init', verbose=verbose)
        run('git remote add upstream "https://{0}@github.com/astrofrog/coordinates-benchmark.git"'.format(token), verbose=verbose)
        run('git fetch upstream', verbose=verbose)
        run('git reset upstream/gh-pages', verbose=verbose)
        run('git add -A .', verbose=verbose)
        run('git commit -m "Latest build"', verbose=verbose)
        run('git push -q upstream HEAD:gh-pages', verbose=verbose)
    finally:
        os.chdir(start_dir)
