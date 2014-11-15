import os
import shutil
import tempfile
import subprocess

tmpdir = tempfile.mkdtemp()
shutil.copytree('output', os.path.join(tmpdir, 'output'))

subprocess.call('git checkout gh-pages', shell=True)

try:

    for root, dirnames, filenames in os.walk(os.path.join(tmpdir, 'output')):
        for filename in filenames:
            print(root, filename)
            filename = os.path.relpath(os.path.join(root, filename), os.path.join(tmpdir, 'output'))
            shutil.copy(os.path.join(tmpdir, 'output', filename), filename)
            subprocess.call('git add ' + filename, shell=True)

    subprocess.call('git commit -m "Latest build"', shell=True)

finally:
    subprocess.call('git checkout deployer', shell=True)
