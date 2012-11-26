Coordinates Benchmark
=====================

Here we compare astropy coordinate conversion results against other Python packages.

For now we only compare precision, in the future we also want to compare speed.

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
