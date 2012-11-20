"""
Coordinate conversions with the kapteyn Python package.

kapteyn.celestial is very feature-complete and has great docs.
Check this out:

http://www.astro.rug.nl/software/kapteyn/celestial.html
http://www.astro.rug.nl/software/kapteyn/celestial.html#celestial.sky2sky
http://www.astro.rug.nl/software/kapteyn/celestial.html#celestial.skyparser

http://www.astro.rug.nl/software/kapteyn/celestialbackground.html
http://www.astro.rug.nl/software/kapteyn/celestialbackground.html#composing-other-transformations
"""
import numpy as np
from kapteyn import celestial

# Read in initial coordinates as J2000 coordinates
initial_coords = np.loadtxt('../initial_coords.txt')

def transform_to(skyout, tag):
    """Convert the test input coordinates to a given output system and save to text file"""
    skyin = 'fk5'
    output = celestial.sky2sky(skyin, skyout, initial_coords[:,0], initial_coords[:,1])
    np.savetxt('coords_{tag}.txt'.format(tag=tag), output, fmt="%20.15f")

transform_to(skyout='galactic', tag='galactic')
transform_to(skyout='fk4,J2000_OBS', tag='b1950')
transform_to(skyout='ecliptic,J2000', tag='ecliptic')
