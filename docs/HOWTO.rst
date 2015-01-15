Astropy coordinates benchmark HOWTO
===================================

Setting up an environment to run the benchmarks
-----------------------------------------------

If you want to set up a virtual environment to run the benchmarks, you can do:

    virtualenv env
    source env/bin/activate
    pip install numpy Cython jinja2
    pip install -r requirements.txt

Note: The ``kapteyn`` package doesn't support Python 3, so if you want to include
it in the benchmark, you have to use Python 2.

Running
-------

Go to the repository top-level folder (where the ``./make.py`` file is).
The ``./make.py`` command line tool gives you access to all functionality.

To print it's help message which lists all sub-commands run:

    ./make.py

To run the benchmarks (output goes in ``output/tools``):

    ./make.py benchmark_all

To generate a summary webpage (output goes in ``output``):

    ./make.py summary

To generate a ton of plots for the webpage (optional) (output goes in ``output/plots``):

    ./make.py plots

Checking
--------

The benchmark results are stored in this repository and have been obtained on one machine,
but it's easy for anyone to re-run (and should be re-run from time to time, especially
after changes in the ``astropy.coordinates`` code).

To check if benchmark or summary output matches results previously obtained,
use ``git diff output/tools`` and ``git diff output/summary.txt``.

TODO: describe how many decimal digits we store and why that
a) is enough precision (< milli-arcsec)
b) should be the same on any 64-bit computer


Deploying
---------

To deploy the latest results to Github pages:

    ./make.py deploy

and if there are no errors:

    git push upstream gh-pages
