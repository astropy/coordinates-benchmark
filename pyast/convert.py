#!/usr/bin/env python

import numpy as np
import starlink.Ast as Ast

# Read in initial coordinates as J2000 coordinates
data_j2000 = np.loadtxt('../initial_coords.txt')
ra_j2000_fk5, dec_j2000_fk5 = data_j2000[:,0], data_j2000[:,1]

#  Create a Frame to describe J2000 FK5 coordinates, and another that
#  will be used in turn to describe each of the output coordinate systems.
#  Assume that the epoch of observation is J2000.0. The default values for
#  the reference equinox will be used (J2000.0 for FK5 and ecliptic, and
#  B1950.0 for FK4).
fk5_frame = Ast.SkyFrame('System=FK5,Format(1)=hms.5,Format(2)=dms.5,Epoch=2000.0')
out_frame = Ast.SkyFrame('Format(1)=hms.5,Format(2)=dms.5,Epoch=2000.0')

#  Loop round each output coordinate system, modifying "out_frame" to
#  describe each one.
vals = {}
for system in 'FK4', 'Ecliptic', 'Galactic', 'ICRS':

   out_frame.System = system

   #  Get the transformation from FK5 J2000 to the current output system.
   fk5_to_out = fk5_frame.convert( out_frame )

   #  Transform the FK5 J2000 positions into the curent output system using
   #  the above transformation.
   vals[system] = fk5_to_out.tran( [ra_j2000_fk5,dec_j2000_fk5] )

glon = vals['Galactic'][0]
glat = vals['Galactic'][1]
np.savetxt('coords_galactic.txt', zip(np.degrees(glon), 
                                       np.degrees(glat)), fmt="%20.15f")

ra_fk4 = vals['FK4'][0]
dec_fk4 = vals['FK4'][1]
np.savetxt('coords_b1950.txt', zip(np.degrees(ra_fk4),
                                    np.degrees(dec_fk4)), fmt="%20.15f")

elon = vals['Ecliptic'][0]
elat = vals['Ecliptic'][1]
np.savetxt('coords_ecliptic.txt', zip(np.degrees(elon),
                                       np.degrees(elat)), fmt="%20.15f")

ra_fk5 = vals['ICRS'][0]
dec_fk5 = vals['ICRS'][1]
np.savetxt('coords_j2000.txt', zip(np.degrees(ra_fk5),
                                    np.degrees(dec_fk5)), fmt="%20.15f")


