"""
Coordinate conversions with the pyast Python package.

https://github.com/timj/starlink-pyast
http://dsberry.github.com/starlink/pyast.html
"""
import numpy as np
import starlink.Ast as Ast

SUPPORTED_SYSTEMS = 'fk5 fk4 icrs galactic ecliptic'.split()

def get_frame(system):
    """Convert generic system specification tags to pyast.SkyFrame"""
    #  Create a Frame to describe J2000 FK5 coordinates, and another that
    #  will be used in turn to describe each of the output coordinate systems.
    #  Assume that the epoch of observation is J2000.0. The default values for
    #  the reference equinox will be used (J2000.0 for FK5 and ecliptic, and
    #  B1950.0 for FK4).
    d = dict()
    d['fk5'] = 'FK5'
    d['fk4'] = 'FK4'
    d['galactic'] = 'Galactic'
    d['ecliptic'] = 'Ecliptic'
    d['icrs'] = 'ICRS'
    return Ast.SkyFrame('System=%s,Format(1)=hms.5,Format(2)=dms.5,Epoch=2000.0' % d[system])

def convert(coords, systems):
    """Convert an array of in_coords from in_system to out_system"""

    if not set(systems.values()).issubset(SUPPORTED_SYSTEMS):
        return None

    in_frame, out_frame = get_frame(systems['in']), get_frame(systems['out'])
    frameset = in_frame.convert(out_frame)
    lon, lat = np.radians(coords['lon']), np.radians(coords['lat'])
    coords = frameset.tran([lon, lat])
    coords = np.degrees(coords.T)
    return dict(lon=coords[:,0], lat=coords[:,1])
