Notes
=====

This is a somewhat random collection of notes that summarize
discussions in Github issues and mailing lists to understand
differences in results seen in the benchmarks.

Links
-----

Mailing list discussions:

* https://groups.google.com/forum/?fromgroups#!topic/astropy-dev/tbcpMQ1rOcY
* https://groups.google.com/forum/?fromgroups#!topic/astropy-dev/-ulzSY9qJKk
* https://groups.google.com/forum/?fromgroups#!searchin/astropy-dev/benchmark

Github issues with detailed discussion or results:

* https://github.com/astropy/coordinates-benchmark/issues/37
* ...

History
-------

- 2012-11-20: Fixed ``kapteyn`` transforms to explicitly specify the epoch of observation for
  the B1950 conversion, and the equinox for the ecliptic conversion

- 2012-11-21: Explicitly precess astropy.coordinates fk4 result to B1950

- 2015-01-14: Add first AltAz system benchmark

- 2015-01-15: Re-structure ``coordinates-benchmark``
  (see `GH #42 <https://github.com/astropy/coordinates-benchmark/pull/42>`_)

- 2020-08-20: Unify Python 2 and Python 3
  (see `GH #63 <https://github.com/astropy/coordinates-benchmark/pull/63>`_)

David Berry on differences in celestial coordinate transforms
-------------------------------------------------------------

::

    > 1) The differences between kapteyn and (idl,pyast,tpm) on the J2000 to
    > B1950 tests is reduced seriously if you specify the epoch of
    > observation explicitly in kapteyn/convert.py. That is, change
    >
    > transform_to(skyout='fk4', tag='b1950')
    >
    > to
    >
    > transform_to(skyout='fk4,J2000_OBS', tag='b1950')
    >
    > This reduces the median difference from 0.217 arc-sec, to 0.0044
    > arc-sec (this must mean that kapteyn is using a different default
    > epoch of observation to the other systems).
    >
    > 2) Improved agreement in J2000->ecliptic can be achieved by
    > specifying the equinox explicitly in kapteyn/convert.py. Change:
    >
    > transform_to(skyout='ecliptic', tag='ecliptic')
    >
    > to
    >
    > transform_to(skyout='ecliptic,J2000', tag='ecliptic')
    >
    > This causes kapteyn and IDL have zero difference. The kaptyn->pyast
    > median difference goes down from 0.04 to 0.036. The remaining
    > difference between kapteyn and pyast seems to be down to:
    >
    > a) DIfferent obliquity models. kaptyn uses the IAU 2000 model, and
    > pyast uses the IAU 2006 model.
    > b) Different precession models. kaptyn uses IAU 1976 and pyast uses IAU 2006.
    >
    > Reverting the models used by pyast gives zero difference between
    > kapteyn and pyast for the J2000->Ecliptic test
    
