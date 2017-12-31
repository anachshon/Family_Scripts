#!/usr/bin/env python

import os, sys, shutil
import json
import datetime
import gzip

inp_file_name = sys.argv[ 1 ]
out_file_name = sys.argv[ 2 ]

#{u'latitudeE7': 321315952, u'altitude': 63, u'longitudeE7': 349514971, u'velocity': 4, u'timestampMs': u'1474264307000', u'heading': 218, u'accuracy': 13}

gkeys = { 'locs' : 'locations', 'long' : 'longitudeE7', 'lat' : 'latitudeE7', 'time' : 'timestampMs' }

inp_file = gzip.open( inp_file_name, 'r' )
data = json.load( inp_file )
inp_file.close()

out_file = gzip.open( out_file_name, 'w' )
out_file.write( '\time\tlong\tlat\n' )
for entry in data[ gkeys[ 'locs' ] ]:
    long = float( entry[ gkeys[ 'long' ] ] ) / 1e7
    lat = float( entry[ gkeys[ 'lat' ] ] ) / 1e7
    time = datetime.datetime.fromtimestamp( float( entry[ gkeys[ 'time' ] ] ) / 1e3 )

    out_file.write( time.strftime( "%a, %d %b %Y %H:%M:%S") + '\t' + str( long ) + '\t' + str( lat ) + '\n' )

    gdfkgdfk
out_file.close()

