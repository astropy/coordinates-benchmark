Coordinates Benchmark
=====================

Here we compare astropy coordinate conversion results against other Python packages.

For now we only compare precision, in the future we also want to compare speed.

Setting up an environment to run the benchmarks
-----------------------------------------------

If you want to set up a virtual environment to run the benchmarks, you can do:

    virtualenv env
    source env/bin/activate
    pip install numpy Cython
    pip install -r pip-requirements.txt

Running
-------

To run the benchmarks:

    python run_benchmark.py --tasks celestial

To generate the summary:

    python run_benchmark.py --tasks summary

To generate the plots:

    python run_benchmark.py --tasks plots

Latest Results
--------------

The latest results can be viewed at http://www.astropy.org/coordinates-benchmark/summary.html

Links
-----

Repository: https://github.com/astropy/coordinates-benchmark
Results summary: http://mpia.de/~robitaille/astropy/coordinates/summary.html

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
