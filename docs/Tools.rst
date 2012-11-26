Tools
=====

The following Python packages for astronomy coordinate calculations are compared:

* `astropy <http://www.astropy.org>`_: A new Python coordinate package being developed. The reason for this benchmark. See https://github.com/astropy/astropy/pull/471 .
* `astrolib.coords <http://www.scipy.org/AstroLibCoordsHome>`_: A `Swig <http://www.swig.org>`_ wrapper for the `TPM <http://www.sal.wisc.edu/~jwp/astro/tpm/tpm.html>`_ C library with a high-level `Position` class. Unmaintained. We are using the last version `coords-0.37` from 2009.
* `kapteyn.celestial <http://www.astro.rug.nl/software/kapteyn/celestial.html>`_: Part of the `Kapteyn <http://www.astro.rug.nl/software/kapteyn/>`_ package.
* `pyast <http://dsberry.github.com/starlink/pyast.html>`_: A Python interface to the `Starlink AST <http://starlink.jach.hawaii.edu/starlink/AST>`_ C library.
* `pyephem <http://rhodesmill.org/pyephem/>`_: A Python astrometry package based on the `xephem <http://www.clearskyinstitute.com/xephem/>`_ coordinate routines, which are interfaced as C extensions. Currently a re-write using Cython is underway in the `version4` branch on github.
* `pyslalib <https://github.com/scottransom/pyslalib>`_: `f2py <http://www.scipy.org/F2py>`_ and `numpy <http://numpy.scipy.org/>`_ wrappers of the fortran version of the astro library `SLALIB <http://www.starlink.rl.ac.uk/docs/sun67.htx/sun67.html>`_
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
pyast             GPL           GPL           Yes   Yes
pyephem           ???           ???           No    Yes
pyslalib          GPL           GPL           No    Yes
pytpm             BSD           ???           No    Yes
idl               Public Domain Commercial    ???   ???
================= ============= ============= ===== ======

Please report any inaccuracies, especially concerning the license status.

Methods
-------

TODO: Give details on the methods used, e.g. for Earth obliquity, precession, nutation, time, ...
Probably best to first collect this info in a bullet list and then try to summarize it in a table.
