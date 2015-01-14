# Licensed under a 3-clause BSD style license - see LICENSE.rst
import os
import shutil
import tempfile
import subprocess
import logging
import click


@click.command()
def deploy():
    """Deploy HTML output to Github pages."""
    tmpdir = tempfile.mkdtemp()
    shutil.copytree('output', os.path.join(tmpdir, 'output'))

    cmd = 'git checkout gh-pages'
    logging.info('EXEC: {}'.format(cmd))
    subprocess.call(cmd, shell=True)

    try:
        for root, dirnames, filenames in os.walk(os.path.join(tmpdir, 'output')):
            for filename in filenames:
                if filename.endswith('.png'):  # for now
                    continue
                filename = os.path.relpath(os.path.join(root, filename), os.path.join(tmpdir, 'output'))
                shutil.copy(os.path.join(tmpdir, 'output', filename), filename)
                cmd = 'git add ' + filename
                logging.info('EXEC: {}'.format(cmd))
                subprocess.call(cmd, shell=True)

        cmd = 'git commit -m "Latest build"'
        logging.info('EXEC: {}'.format(cmd))
        subprocess.call(cmd, shell=True)

    finally:
        cmd = 'git checkout master'
        logging.info('EXEC: {}'.format(cmd))
        subprocess.call(cmd, shell=True)
