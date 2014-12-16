"""
Coordinate conversions with the pyephem Python package.

http://rhodesmill.org/pyephem/
https://github.com/brandon-rhodes/pyephem
"""
import numpy as np
import ephem

SUPPORTED_SYSTEMS = 'fk5 fk4 galactic ecliptic'.split()


def convert(coords, systems):
    if not set(systems.values()).issubset(SUPPORTED_SYSTEMS):
        return None

    lons, lats = np.radians(coords['lon']), np.radians(coords['lat'])

    for ii, (lon, lat) in enumerate(zip(lons, lats)):
        # Create coordinate in input system
        if systems['in'] == 'fk5':
            coord = ephem.Equatorial(lon, lat)
        elif systems['in'] == 'fk4':
            coord = ephem.Equatorial(lon, lat, epoch=ephem.B1950)
        elif systems['in'] == 'galactic':
            coord = ephem.Galactic(lon, lat)
        elif systems['in'] == 'ecliptic':
            coord = ephem.Ecliptic(lon, lat)
        else:
            raise ValueError()

        # Convert to appropriate output system
        # Retrieving output system coordinates is system specific
        # because the attribute names depend on the system
        if systems['out'] == 'fk5':
            coord = ephem.Equatorial(coord, epoch=ephem.J2000)
            lon, lat = coord.ra, coord.dec
        elif systems['out'] == 'fk4':
            coord = ephem.Equatorial(coord, epoch=ephem.B1950)
            lon, lat = coord.ra, coord.dec
        elif systems['out'] == 'galactic':
            coord = ephem.Galactic(coord)
            lon, lat = coord.lon, coord.lat
        elif systems['out'] == 'ecliptic':
            coord = ephem.Ecliptic(coord)
            lon, lat = coord.lon, coord.lat
        else:
            raise ValueError()

        lons[ii], lats[ii] = lon, lat

    return dict(lon=np.degrees(lons), lat=np.degrees(lats))
