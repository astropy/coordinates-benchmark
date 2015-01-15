Tools
=====

The following Python packages for astronomy coordinate calculations are compared:

* `astropy.coordinates <http://astropy.readthedocs.org/en/latest/coordinates/>`_: Uses `erfa <https://github.com/liberfa/erfa>`_ for some computations, but re-implements many things using Python / numpy.
* `astrolib.coords <http://www.scipy.org/AstroLibCoordsHome>`_: A `Swig <http://www.swig.org>`_ wrapper for the `TPM <http://www.sal.wisc.edu/~jwp/astro/tpm/tpm.html>`_ C library with a high-level `Position` class. Unmaintained. We are using the last version `coords-0.37` from 2009.
* `kapteyn.celestial <http://www.astro.rug.nl/software/kapteyn/celestial.html>`_: Part of the `Kapteyn <http://www.astro.rug.nl/software/kapteyn/>`_ package.
* NOVAS (`PyPI <http://pypi.python.org/pypi/novas/>`_, `Official <http://www.usno.navy.mil/USNO/astronomical-applications/software-products/novas/novas-python>`_): A `ctypes <http://docs.python.org/library/ctypes.html>`_ wrapper for the NOVAS C library from the United States Naval observatory.
* `pyast <http://dsberry.github.com/starlink/pyast.html>`_: A Python interface to the `Starlink AST <http://starlink.jach.hawaii.edu/starlink/AST>`_ C library.
* `palpy <https://github.com/Starlink/palpy>`_: A Python interface to the `Starlink PAL <https://github.com/Starlink/pal>`_ C library which is a reimplementation of SLALIB using SOFA/ERFA.
* `pyephem <http://rhodesmill.org/pyephem/>`_: A Python astrometry package based on the `xephem <http://www.clearskyinstitute.com/xephem/>`_ coordinate routines, which are interfaced as C extensions. Currently a re-write using Cython is underway in the `version4` branch on github.
* `pyslalib <https://github.com/scottransom/pyslalib>`_: `f2py <http://www.scipy.org/F2py>`_ and `numpy <http://numpy.scipy.org/>`_ wrappers of the fortran version of the astro library `SLALIB <http://www.starlink.rl.ac.uk/docs/sun67.htx/sun67.html>`_
* `pysofa <http://pypi.python.org/pypi/pysofa>`_ is a `ctypes <http://docs.python.org/library/ctypes.html>`_ wrapper for the `SOFA <http://www.iausofa.org>`_ `C library <http://www.iausofa.org/current_C.html>`_. It does use numpy for 3x3 matrices, but it does not support input numpy arrays of coordinates for it's functions.
* `pytpm <http://phn.github.com/pytpm/>`_: A `Cython <http://cython.org>`_ interface to the `TPM <http://www.sal.wisc.edu/~jwp/astro/tpm/tpm.html>`_ C library with a high-level `convert.convertv6` function interface. Unmaintained. We are using the version from github master.
* `idl euler <http://idlastro.gsfc.nasa.gov/ftp/pro/astro/euler.pro>`_: Part of the `IDL Astronomy User's Library <http://idlastro.gsfc.nasa.gov>`_.

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
astrolib.coords   BSD           ???           No    No
kapteyn.celestial BSD           ---           Yes   No
novas             Public Domain Public Domain No    Yes
palpy             GPL           GPL           Some  Yes
pyast             LGPL          LGPL          Yes   Yes
pyephem           LGPL          LGPL          No    Yes
pyslalib          GPL           GPL           No    Yes
pysofa            MIT           SOFA          No    Yes
pytpm             BSD           ???           No    Yes
idl               Public Domain Commercial    ???   ???
================= ============= ============= ===== ======

Notes:

* The `SOFA License <http://www.iausofa.org/tandc.html>`_ is considered non-free (see discussion `here <https://groups.google.com/forum/?fromgroups=#!topic/astropy-dev/QVpMZFlsQUo>`_).

Please report any inaccuracies, especially concerning the license status.

Methods
-------

TODO: Give details on the methods used, e.g. for Earth obliquity, precession, nutation, time, ...
Probably best to first collect this info in a bullet list and then try to summarize it in a table.
