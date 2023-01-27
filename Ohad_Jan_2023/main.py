#!/usr/bin/env python3

import cube
import solve
import dics
import pandas as pd
import sys

data = pd.read_csv( sys.argv[ 1 ], sep = "\t", index_col = 0, header = 0 )
cubes = []

for line in range( data.shape[ 0 ] ):
    cubes.append( cube.cube( line + 1, data.iloc[ line, range( 6 ) ], data.iloc[ line, range( 6, 12 ) ] ) )

if ( len( sys.argv ) == 4 ):
    solve.solve_1d( cubes, dics.colors[ sys.argv[ 2 ] ], int( sys.argv[ 3 ] ) )
elif ( len( sys.argv ) == 5 ):
    solve.solve_2d( cubes, dics.colors[ sys.argv[ 2 ] ], int( sys.argv[ 3 ] ), int( sys.argv[ 4 ] ) )
