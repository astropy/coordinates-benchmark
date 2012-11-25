#!/usr/bin/env python
"""Run the coordinates benchmark"""
import argparse
import time
import itertools
import imp
import logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
import numpy as np

# Make a list of celestial conversions to check
# We simply list all possible combinations here,
# systems not supported by certain tools are simply skipped later
CELESTIAL_SYTEMS = 'fk5 fk4 icrs galactic ecliptic'.split()
CELESTIAL_CONVERSIONS = itertools.product(CELESTIAL_SYTEMS, CELESTIAL_SYTEMS)
CELESTIAL_CONVERSIONS = [dict(zip(['in', 'out'], _))
                         for _ in CELESTIAL_CONVERSIONS
                         if _[0] != _[1]]

TOOLS = 'astropy kapteyn pyast pyephem pyslalib tpm'.split()

if __name__ == '__main__':
    
    # Command line argument parsing and argument checking

    parser = argparse.ArgumentParser(description='Run the coordinates benchmark')
    parser.add_argument('--celestial', action="store_true",
                        help='Run celestial coordinate conversions.')
    parser.add_argument('--horizontal', action="store_true",
                        help='Run horizontal coordinate conversions.')
    parser.add_argument('--tools', nargs='+', default='',
                        help='List tools to run. Available tools: %s' % ', '.join(TOOLS))
    args = parser.parse_args()
    
    if not (args.celestial or args.horizontal):
        parser.error('You must choose at least one task. '
                     'Available tasks: --celestial --horizontal')
    
    if not args.tools:
        parser.error('You must choose at least one tool. '
                     'Available tools: %s' % TOOLS)
    
    for tool in args.tools:
        if not tool in TOOLS:
            parser.error("Can't run tool: %s" % tool)
    
    # Execute the requested steps for the requested tools
    
    for tool in args.tools:
        
        tool_module = imp.load_source('dummy', '%s/convert.py' % tool)

        if args.celestial:
            logging.info('Running celestial conversions using %s' % tool)    
            coords = np.loadtxt('initial_coords.txt')
            coords = dict(lon=coords[:,0], lat=coords[:,1])
            for systems in CELESTIAL_CONVERSIONS:
                timestamp = time.time()
                out_coords = tool_module.convert(coords, systems)
                if out_coords == None:
                    logging.info('Skipping %s -> %s. Not supported.' %
                                 (systems['in'], systems['out']))
                    continue
                duration = time.time() - timestamp
                # TODO: print execution time to an ascii file (one for each tool)
                filename = '%s/%s_to_%s.txt' % (tool, systems['in'], systems['out'])
                logging.info('Writing %s' % filename)
                out_coords = np.transpose(np.vstack([out_coords['lon'], out_coords['lat']]))
                np.savetxt(filename, out_coords, fmt="%20.15f")

        if args.horizontal:
            raise NotImplementedError()
