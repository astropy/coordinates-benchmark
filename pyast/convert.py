#!/usr/bin/env python
import starlink.Ast as Ast

#  Create lists holding values read from the first two columns of the
#  "coords.txt" file (should be the FK5 J2000 RA and Dec values). Convert
#  from degrees to radians.
ra_j2000_fk5 = []
dec_j2000_fk5 =  []
fd = open( 'coords.txt', 'r' )
for row in fd:
   if not '#' in row:
      values = row.strip().split(',')
      ra_j2000_fk5.append( float(values[0])*Ast.DD2R )
      dec_j2000_fk5.append( float(values[1])*Ast.DD2R )
fd.close()

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


#  Write the table of converted values (in degrees) to text file "pyast.txt"
fd = open( 'pyast.txt', 'w' )
fd.write("# ra_fk5  dec_fk5 ra_fk4 dec_fk4 elon elat glon glat ra dec\n")
for (ra_fk5,dec_fk5,ra_fk4,dec_fk4,elon,elat,glon,glat,ra,dec) in zip(
                                          ra_j2000_fk5, dec_j2000_fk5,
                                          vals['FK4'][0], vals['FK4'][1],
                                          vals['Ecliptic'][0], vals['Ecliptic'][1],
                                          vals['Galactic'][0], vals['Galactic'][1],
                                          vals['ICRS'][0], vals['ICRS'][1]):

   ra_fk5 *= Ast.DR2D
   dec_fk5 *= Ast.DR2D
   ra_fk4 *= Ast.DR2D
   dec_fk4 *= Ast.DR2D
   elon *= Ast.DR2D
   elat *= Ast.DR2D
   glon *= Ast.DR2D
   glat *= Ast.DR2D
   ra *= Ast.DR2D
   dec *= Ast.DR2D
   fd.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\n".format(ra_fk5, dec_fk5,
                                ra_fk4, dec_fk4, elon, elat, glon, glat, ra, dec ))
fd.close()


