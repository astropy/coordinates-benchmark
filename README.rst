Astropy Coordinates Benchmark
=============================

Here we compare Astropy coordinate transformation results against other Python coordinate packages.

For now we only compare precision, in the future we also want to compare speed.

- View latest results: http://www.astropy.org/coordinates-benchmark/summary.html
- ``astropy.coordinates`` docs: http://astropy.readthedocs.org/en/latest/coordinates/index.html
- Repository: https://github.com/astropy/coordinates-benchmark


.. image:: https://github.com/astropy/coordinates-benchmark/workflows/Run%20benchmarks/badge.svg
    :target: https://github.com/astropy/coordinates-benchmark/actions?query=workflow%3A%22Run+benchmarks%22
    :alt: Benchmarks Status

Documentation is in the `docs <https://github.com/astropy/coordinates-benchmark/blob/master/docs/>`__ folder:

- `Specification.rst <https://github.com/astropy/coordinates-benchmark/blob/master/docs/Specification.rst>`_
- `Notes.rst <https://github.com/astropy/coordinates-benchmark/blob/master/docs/Notes.rst>`_
- `Tools.rst <https://github.com/astropy/coordinates-benchmark/blob/master/docs/Tools.rst>`_
- `HOWTO.rst <https://github.com/astropy/coordinates-benchmark/blob/master/docs/HOWTO.rst>`_

Automatic deploying
-------------------

The automatic deploying to ``gh-pages`` was set up by first generating an ssh key with::

    ssh-keygen -t rsa -b 4096 -C "astropy.team@gmail.com" -f github_deploy_key -N ''

The ``github_deploy_key.pub`` public key was added as a deploy key in this
repository (with write access). The ``travis`` command was then used to encrypt
the private key::

    travis encrypt-file github_deploy_key

The ``github_deploy_key.enc`` file was added to the repository, and the
following lines were added to ``.travis.yml`` (the first line should be whatever
is output by the ``travis encrypt-file`` command)::

    openssl aes-256-cbc -K $encrypted_ae4bff0a7007_key -iv $encrypted_ae4bff0a7007_iv -in github_deploy_key.enc -out ~/.ssh/publish-key -d
    chmod u=rw,og= ~/.ssh/publish-key
    echo "Host github.com" >> ~/.ssh/config
    echo "  IdentityFile ~/.ssh/publish-key" >> ~/.ssh/config
