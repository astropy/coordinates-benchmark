"""Convert FK5 J2000 to / from horizontal coordinate system"""
import numpy as np
import starlink.Ast as Ast
from astropy.time import Time

# Read in initial coordinates and the observers.
# For now just process one observer and 10 positions to compare against pyast
data_j2000 = np.loadtxt('../../input/initial_coords.txt')[:3]
observers = np.recfromcsv('../../input/observers.txt')[:2]

# We'll store the results here
results = np.zeros(data_j2000.shape[0] * observers.shape[0], dtype=[('az', 'float64'), ('alt', 'float64')])

for ii, (lon, lat, altitude, time, time_mjd, time_tdb) in enumerate(observers):
    for jj, (ra, dec) in enumerate(data_j2000):

        fk5_frame = Ast.SkyFrame('System=FK5,Format(1)=hms.5,Format(2)=dms.5,Epoch=2000.0')
        # TODO: Need to set fk5_frame.Epoch in tdb scale?
        out_frame = Ast.SkyFrame('System=AZEL,Format(1)=hms.5,Format(2)=dms.5')

        # Set observation location and time
        # http://www.starlink.rl.ac.uk/docs/sun211.htx/node612.html#System
        out_frame.ObsLon = lon
        out_frame.ObsLat = lat
        out_frame.ObsAlt = altitude
        # http://www.starlink.rl.ac.uk/docs/sun211.htx/node489.html#Epoch
        epoch = Time(time, scale='utc').tdb.mjd
        out_frame.Epoch = epoch
        # http://www.starlink.rl.ac.uk/docs/sun211.htx/node486.html
        # http://en.wikipedia.org/wiki/DUT1
        # TODO: Set DUT1 correctly. But how to compute it?
        out_frame.Dut1 = 0

        # Compute alt / az
        fk5_to_out = fk5_frame.convert( out_frame )
        #import IPython; IPython.embed(); 1/0
        alt, az = np.degrees(fk5_to_out.tran([[ra], [dec]]))

        # Store in results array
        kk = ii * data_j2000.shape[0] + jj
        results[kk]['az'] = az
        results[kk]['alt'] = alt

np.savetxt('coords_fk5_to_horizontal.txt', results, fmt="%20.15f")
