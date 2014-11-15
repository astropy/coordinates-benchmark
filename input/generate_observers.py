"""Generate a small list of observers (lon, lat, altitude, time in various formats).

This list will be used as input for the horizontal coordinate conversion tests.

Columns:
lon : longitude in deg
lat : latitude in deg
altitude : altitude in km
time : UTC time string
time_mjd : time in MJD scale
time_tdb : time in TDB scale
"""
import itertools
import numpy as np
import pandas as pd
from astropy.time import Time

np.random.seed(12345)

# Number of samples
N = 100

# Sample uniformly on the unit sphere
lon = np.random.uniform(0., 360., N)
lat = np.degrees(np.arcsin(np.random.uniform(-1., 1., N)))

# Sample of altitudes (distances from the Earth's center) in km
altitude = np.array([6e3, 10e3], dtype='int')

# Sample of UTC times
time = ['1970-01-01', '1980-01-01', '1990-01-01', '2000-01-01', '2010-01-01']

# Some coordinate packages need time input on another scale
# We use astropy.time to do the conversion and store several times in the ascii file.
time_mjd = Time(time, scale='utc').mjd
time_mjd = time_mjd.astype('int') # these are actually ints, I checked.
time_tdb = Time(time, scale='utc').tdb.vals

# For each longitude, create an observer at ech altitude and time
# This is a cartesian product: http://docs.python.org/2/library/itertools.html#itertools.product
table = list(itertools.product(zip(lon, lat), altitude, zip(time, time_mjd, time_tdb)))
table = [(_[0][0], _[0][1], _[1], _[2][0], _[2][1], _[2][2]) for _ in table]
columns = 'lon lat altitude time time_mjd time_tdb'.split()

table = pd.DataFrame(table, columns=columns)
table.to_csv('observers.txt', float_format='%.15f', index=False)
