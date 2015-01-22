Astropy Coordinates Benchmark
=============================

Here we compare Astropy coordinate transformation results against other Python coordinate packages.

For now we only compare precision, in the future we also want to compare speed.

Latest Results
--------------

The latest results can be viewed at http://www.astropy.org/coordinates-benchmark/summary.html

[![Build Status](https://travis-ci.org/astropy/coordinates-benchmark.svg?branch=master)](https://travis-ci.org/astropy/coordinates-benchmark)

The benchmarks
--------------

The coordinate systems used in the benchmarks are:

* ``fk4``: FK4 system (with e-terms), equinox B1950 and observation epoch J2000
* ``fk5``: FK5 system, equinox J2000
* ``icrs``: ICRS system
* ``galactic``: Galactic coordinate system
* ``ecliptic``: Ecliptic coordinate system, observation epoch J2000
* ``altaz``: Horizontal coordinate system


Links
-----

Repository: https://github.com/astropy/coordinates-benchmark

Mailing list discussions:
* https://groups.google.com/forum/?fromgroups#!topic/astropy-dev/tbcpMQ1rOcY
* https://groups.google.com/forum/?fromgroups#!topic/astropy-dev/-ulzSY9qJKk
* https://groups.google.com/forum/?fromgroups#!searchin/astropy-dev/benchmark

Documentation is in the `docs` folder:
* `Specification.rst <https://github.com/astropy/coordinates-benchmark/blob/master/docs/Specification.rst>`_
* `Notes.rst <https://github.com/astropy/coordinates-benchmark/blob/master/docs/Notes.rst>`_
* `Tools.rst <https://github.com/astropy/coordinates-benchmark/blob/master/docs/Tools.rst>`_
* `HOWTO.rst <https://github.com/astropy/coordinates-benchmark/blob/master/docs/HOWTO.rst>`_

History
-------

- 2012-11-20: Fixed ``kapteyn`` transforms to explicitly specify the epoch of observation for
  the B1950 conversion, and the equinox for the ecliptic conversion

- 2012-11-21: Explicitly precess astropy.coordinates fk4 result to B1950

- 2015-01-14: Add first AltAz system benchmark

- 2015-01-15: Re-structure ``coordinates-benchmark``
  (see `GH #42 <https://github.com/astropy/coordinates-benchmark/pull/42>`_)
