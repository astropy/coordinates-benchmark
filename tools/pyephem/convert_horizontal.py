"""Convert ICRS to AltAz with PyEphem.
"""
import logging
logging.basicConfig(level=logging.INFO)
import numpy as np
import astropy.units as u
from astropy.table import Table
import ephem

TABLE_FORMAT = 'ascii.fixed_width_two_line'
FLOAT_FORMAT = '%20.15f'


def read_positions_observers():
    # Read in initial coordinates and the observers.
    # For now just process one observer and 10 positions to compare against pyast
    positions = Table.read('../../input/initial_coords.txt', format='ascii',
                           names=['lon', 'lat'])
    observers = Table.read('../../input/observers.txt', format='ascii')

    # Select subset for now
    positions = positions[:10]

    return positions, observers


def _convert_radec_to_altaz(ra, dec, lon, lat, height, time):
    """Convert a single position.

    (PyEphem doesn't support arrays of positions.)
    """
    # We need to create a "Body" in pyephem, which represents the coordinate
    # http://stackoverflow.com/questions/11169523/how-to-compute-alt-az-for-given-galactic-coordinate-glon-glat-with-pyephem
    body = ephem.FixedBody()
    body._ra = np.radians(ra)
    body._dec = np.radians(dec)
    #body._epoch = 'eq.epoch'

    # Set observer parameters
    obs = ephem.Observer()
    obs.lon = np.radians(lon)
    obs.lat = np.radians(lat)
    obs.elevation = (height * u.km).to(u.m).value
    obs.epoch = '2000'
    obs.date = time
    # Turn refraction off by setting pressure to zero
    obs.pressure = 0

    # Compute alt / az of the body for that observer
    body.compute(obs)
    az, alt = np.degrees([body.az, body.alt])

    return dict(az=az, alt=alt)


def convert_horizontal(positions, observers):

    results = []
    for observer in observers:
        for position in positions:

            ra = position['lon']
            dec = position['lat']
            lon = observer['lon']
            lat = observer['lat']
            height = observer['height']
            time = observer['time']
            altaz = _convert_radec_to_altaz(ra, dec, lon, lat, height, time)
            results.append(altaz)

    table = Table(results)
    return table


def main():
    positions, observers = read_positions_observers()

    results = convert_horizontal(positions, observers)

    for col in ['az', 'alt']:
        results[col].format = FLOAT_FORMAT

    filename = 'coords_fk5_to_horizontal.txt'
    logging.info('Writing {}'.format(filename))
    results.write(filename, format=TABLE_FORMAT)


if __name__ == '__main__':
    main()
