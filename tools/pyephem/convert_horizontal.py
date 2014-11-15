"""Convert FK5 J2000 to / from horizontal coordinate system"""
import numpy as np
import ephem

# Read in initial coordinates and the observers.
# For now just process one observer and 10 positions to compare against pyast
data_j2000 = np.loadtxt('../../input/initial_coords.txt')[:3]
observers = np.recfromcsv('../../input/observers.txt')[:2]

# We'll store the results here
results = np.zeros(data_j2000.shape[0] * observers.shape[0], dtype=[('az', 'float64'), ('alt', 'float64')])

for ii, (lon, lat, altitude, time, time_mjd, time_tdb) in enumerate(observers):
    for jj, (ra, dec) in enumerate(data_j2000):
        # We need to create a "Body" in pyephem, which represents the coordinate
        # http://stackoverflow.com/questions/11169523/how-to-compute-alt-az-for-given-galactic-coordinate-glon-glat-with-pyephem
        body = ephem.FixedBody()
        body._ra = np.radians(ra)
        body._dec = np.radians(dec)
        #body._epoch = 'eq.epoch'

        # Set observer parameters
        obs =  ephem.Observer()
        obs.lon = np.radians(lon)
        obs.lat = np.radians(lat)
        obs.elevation = altitude
        obs.epoch = '2000'
        obs.date = time
        # Turn refraction off by setting pressure to zero
        obs.pressure = 0

        # Compute alt / az of the body for that observer
        body.compute(obs)
        az, alt = np.degrees([body.az, body.alt])

        # Store in results array
        kk = ii * data_j2000.shape[0] + jj
        results[kk]['az'] = az
        results[kk]['alt'] = alt

np.savetxt('coords_fk5_to_horizontal.txt', results, fmt="%20.15f")
