Coordinates Benchmark
=====================

Here we compare astropy coordinate conversion results against other Python packages.

For now we only compare precision, in the future we also want to compare speed.

[![Build Status](https://travis-ci.org/astropy/coordinates-benchmark.svg?branch=master)](https://travis-ci.org/astropy/coordinates-benchmark)

Setting up an environment to run the benchmarks
-----------------------------------------------

If you want to set up a virtual environment to run the benchmarks, you can do:

    virtualenv env
    source env/bin/activate
    pip install numpy Cython jinja2
    pip install -r pip-requirements.txt

Running
-------

To run the benchmarks:

    python run_benchmark.py --tasks celestial

To generate the summary:

    python run_benchmark.py --tasks summary

To generate the plots:

    python run_benchmark.py --tasks plots

Deploying
---------

To deploy the latest results to the web version:

    python deploy.py

and if there are no errors:

    git push upstream gh-pages

The benchmarks
--------------

The coordinate systems used in the benchmarks are:

* ``fk4``: FK4 system (with e-terms), equinox B1950 and observation epoch J2000
* ``fk5``: FK5 system, equinox J2000
* ``icrs``: ICRS system
* ``galactic``: Galactic coordinate system
* ``ecliptic``: Ecliptic coordinate system, observation epoch J2000

The main scripts to set up the benchmarks are in ``tools/<toolname>/convert.py``.

Latest Results
--------------

The latest results can be viewed at http://www.astropy.org/coordinates-benchmark/summary.html

Links
-----

Repository: https://github.com/astropy/coordinates-benchmark

Results summary: http://www.astropy.org/coordinates-benchmark/summary.html

Mailing list discussions:
* https://groups.google.com/forum/?fromgroups#!topic/astropy-dev/tbcpMQ1rOcY
* https://groups.google.com/forum/?fromgroups#!topic/astropy-dev/-ulzSY9qJKk
* https://groups.google.com/forum/?fromgroups#!searchin/astropy-dev/benchmark

Documentation is in the `docs` folder:
* Specification.rst
* Notes.rst
* Tools.rst
* HOWTO.rst

History
-------

- Fixed kapteyn transforms to explicitly specify the epoch of observation for
  the B1950 conversion, and the equinox for the ecliptic conversion

- Explicitly precess astropy.coordinates fk4 result to B1950
