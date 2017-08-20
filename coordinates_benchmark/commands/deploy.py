# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function

import os
import shutil
import tempfile
import subprocess
import filecmp

import click
from matplotlib.testing.compare import compare_images
from matplotlib.testing.exceptions import ImageComparisonFailure

def run(cmd):
    print("EXEC: {0}".format(cmd))
    retcode = subprocess.call(cmd, shell=True)
    assert retcode == 0


def copy_mkdir(original, destination):
    directory = os.path.dirname(destination)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    shutil.copy2(original, destination)


@click.command()
@click.option('--repo', default='astropy/coordinates-benchmark', help='Github repo slug')
def deploy(repo):
    """Deploy HTML output to Github pages."""

    tmp_dir = tempfile.mkdtemp()
    start_dir = os.path.abspath('.')
    output_dir = os.path.abspath('output')

    try:
        os.chdir(tmp_dir)
        run('git init')
        run('git remote add upstream git@github.com:{0}'.format(repo))
        run('git fetch upstream')
        run('git reset --hard upstream/gh-pages')

        # We check the files one by one because we want to minimize changes and
        # make sure we only upload plots that have really changed (otherwise
        # PNG files look externally different every time they are generated even
        # if the real content hasn't changed)

        changed = False

        for root, _, filenames in os.walk(output_dir):
            for filename in filenames:
                original_file = os.path.join(root, filename)
                new_file = os.path.relpath(original_file, output_dir)
                if os.path.exists(new_file):
                    if filename.endswith('.png'):
                        try:
                            result = compare_images(original_file, new_file, tol=0)
                        except ImageComparisonFailure:
                            result = 'failed'
                        if result is not None:
                            copy_mkdir(original_file, new_file)
                            changed = True
                    else:
                        if not filecmp.cmp(original_file, new_file, shallow=False):
                            copy_mkdir(original_file, new_file)
                            changed = True
                else:
                    copy_mkdir(original_file, new_file)
                    changed = True

        if changed:
            run('git add -A .')
            run('git commit --allow-empty -m "Latest build"')
            run('git push -q upstream HEAD:gh-pages')

    finally:
        os.chdir(start_dir)
