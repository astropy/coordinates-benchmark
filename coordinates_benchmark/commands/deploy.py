# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function

import os
import sys
import shutil
import tempfile
import subprocess
import click


def run(cmd):
    print("EXEC: {0}".format(cmd))
    retcode = subprocess.call(cmd, shell=True)
    assert retcode == 0


@click.command()
@click.option('--repo', default='astropy/coordinates-benchmark', help='Github repo slug')
def deploy(repo):
    """Deploy HTML output to Github pages."""

    tmpdir = tempfile.mkdtemp()
    tmpout = os.path.join(tmpdir, 'output')
    shutil.copytree('output', tmpout)
    start_dir = os.path.abspath('.')

    try:
        os.chdir(tmpout)
        run('git init')
        run('git remote add upstream git@github.com:{0}'.format(repo))
        run('git fetch upstream')
        run('git reset upstream/gh-pages')
        run('git add -A .')
        run('git commit --allow-empty -m "Latest build"')
        run('git push -q upstream HEAD:gh-pages')
    finally:
        os.chdir(start_dir)
