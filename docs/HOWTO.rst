HOWTO
=====

* First install the coordinate packages you'd like to benchmark.
* The top-level `./run_benchmark.py` script is used to run the benchmark.
* `./run_benchmark.py -h` to show help.
* `./run_benchmark.py --tasks celestial --tools all` to run the celestial coordinate conversion benchmark for all tools. This generates `*.txt` files in the tool sub-folders.
* The `idl` celestial conversions have to be run via `cd idl; idl convert.pro`
* `./run_benchmark.py --tasks plots --tools all` to produce plots in the `plots` sub-folder (needs the `<tool>/*.txt files`)
* `./run_benchmark.py --tasks summary` to create the `summary.txt` and `summary.html` tables (needs the `<tool>/*.txt files`)
