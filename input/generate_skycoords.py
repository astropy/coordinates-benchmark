"""Generate skycoords.txt file.

Columns:
- lon      : longitude in deg
- lat      : latitude in deg
"""
import numpy as np
np.random.seed(12345)

# Number of samples
N = 1000

# Sample uniformly on the unit sphere
lon = np.random.uniform(0., 360., N)
lat = np.degrees(np.arcsin(np.random.uniform(-1., 1., N)))

# Save to file
np.savetxt('initial_coords.txt', zip(lon, lat), fmt="%20.15f")