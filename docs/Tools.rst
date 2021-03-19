Tools
=====

Overview
--------

The following Python packages for astronomy coordinate calculations are compared.

astropy.coordinates
+++++++++++++++++++

`astropy.coordinates <http://astropy.readthedocs.org/en/latest/coordinates/>`_:
Uses `erfa <https://github.com/liberfa/erfa>`_ for some computations, but re-implements many things using Python / numpy.

kapteyn.celestial
+++++++++++++++++

`kapteyn.celestial <http://www.astro.rug.nl/software/kapteyn/celestial.html>`_:
Part of the `Kapteyn <http://www.astro.rug.nl/software/kapteyn/>`_ package.

NOVAS
+++++

The Naval Observatory Vector Astrometry Software
(`NOVAS <http://aa.usno.navy.mil/software/novas/novas_info.php>`__)
version 3.1 exists as a FORTRAN, C and Python edition.

We use the Python edition, which is a `ctypes <http://docs.python.org/library/ctypes.html>`_ wrapper for the C version.
It can be obtained from three locations ... the versions should be identical:

* Official tarball: http://www.usno.navy.mil/USNO/astronomical-applications/software-products/novas/novas-python
* Unofficial, but convenient: http://pypi.python.org/pypi/novas/
* Unofficial, but convenient: https://github.com/brandon-rhodes/python-novas

PyAST
+++++

`pyast <http://dsberry.github.com/starlink/pyast.html>`_:
A Python interface to the `Starlink AST <http://starlink.jach.hawaii.edu/starlink/AST>`_ C library.

PalPy
+++++

`palpy <https://github.com/Starlink/palpy>`_ is a Python interface to the
`Starlink PAL <https://github.com/Starlink/pal>`_ C library which is a reimplementation of SLALIB using SOFA/ERFA.

PyEphem
+++++++

`pyephem <http://rhodesmill.org/pyephem/>`_ is a Python astrometry package based on the
`xephem <http://www.clearskyinstitute.com/xephem/>`_ coordinate routines,
which are interfaced as C extensions. Currently a re-write using Cython is underway in the `version4` branch on github.

PySlalib
++++++++

`pyslalib <https://github.com/scottransom/pyslalib>`_

`f2py <http://www.scipy.org/F2py>`_ and `numpy <http://numpy.scipy.org/>`_
wrappers of the fortran version of the astro library `SLALIB <http://www.starlink.rl.ac.uk/docs/sun67.htx/sun67.html>`_

PyTPM
+++++

`pytpm <http://phn.github.com/pytpm/>`_ is `Cython <http://cython.org>`_ interface to the
`TPM <http://www.sal.wisc.edu/~jwp/astro/tpm/tpm.html>`_ C library with a high-level
``convert.convertv6`` function interface. Unmaintained.

We are using the version from github main.

Note that ``pytpm`` is unmaintained and is known to give incorrect results in this case:
https://github.com/phn/pytpm/issues/2

Licenses and Features
---------------------

* Package -- Package name
* License -- License of the Python package
* Lib License -- License of the underlying C or Fortran coordinates library (if applicable)
* Array -- Works with arrays of coordinates?
* Alt/Az -- Can compute horizontal coordinates for a given observer? 

================= ============= ============= ===== ======
Package           License       Lib License   Array Alt/Az
================= ============= ============= ===== ======
astropy           BSD           ---           No    No
kapteyn.celestial BSD           ---           Yes   No
novas             Public Domain Public Domain No    Yes
palpy             GPL           GPL           Some  Yes
pyast             LGPL          LGPL          Yes   Yes
pyephem           LGPL          LGPL          No    Yes
pyslalib          GPL           GPL           No    Yes
pysofa            MIT           SOFA          No    Yes
pytpm             BSD           ???           No    Yes
================= ============= ============= ===== ======

Notes:

* The `SOFA License <http://www.iausofa.org/tandc.html>`_ is considered non-free (see discussion `here <https://groups.google.com/forum/?fromgroups=#!topic/astropy-dev/QVpMZFlsQUo>`_).

Please report any inaccuracies, especially concerning the license status.

The following packages have been removed from the ``coordinates-benchmark``:

Other tools that are currently not included
+++++++++++++++++++++++++++++++++++++++++++

PySOFA
++++++

`pysofa <http://pypi.python.org/pypi/pysofa>`_ is a `ctypes <http://docs.python.org/library/ctypes.html>`_
wrapper for the `SOFA <http://www.iausofa.org>`_ `C library <http://www.iausofa.org/current_C.html>`_.
It does use numpy for 3x3 matrices, but it does not support input numpy arrays of coordinates for it's functions.
It was never added to the ``coordinates-benchmark`` and given that Astropy and some others use SOFA/ERFA
and PySOFA is unmaintained it doesn't seem useful to add it.

astrolib.coords
+++++++++++++++

`astrolib.coords <http://www.scipy.org/AstroLibCoordsHome>`_:
A `Swig <http://www.swig.org>`_ wrapper for the `TPM <http://www.sal.wisc.edu/~jwp/astro/tpm/tpm.html>`_ C library
with a high-level `Position` class. Unmaintained. We are using the last version `coords-0.37` from 2009.

We removed it because we ran into a small issue https://github.com/astropy/coordinates-benchmark/issues/44
and didn't feel it's worth tracking it down given that we have enough other packages in the benchmark to compare against.

Skyfield
++++++++

* http://rhodesmill.org/skyfield/
* https://github.com/brandon-rhodes/python-skyfield

Note that Skyfield now can do AltAz to RaDec transforms:
https://github.com/brandon-rhodes/python-skyfield/issues/13#issuecomment-72392700


Methods
-------

TODO: Give details on the methods used, e.g. for Earth obliquity, precession, nutation, time, ...
Probably best to first collect this info in a bullet list and then try to summarize it in a table.

Useful references:

* `SOFA C-version Documentation <http://www.iausofa.org/sofa_ast_c.pdf>`__ (see Figure 1)
* `TPM Specification <http://www.sal.wisc.edu/~jwp/astro/tpm/tpm.pdf>`__ and `TPM diagram <http://www.sal.wisc.edu/~jwp/astro/tpm/tpm-states.pdf>`__
* `NOVAS User Guide <http://aa.usno.navy.mil/software/novas/novas_c/NOVAS_C3.1_Guide.pdf>`__
