#!/usr/bin/env python3

import cube
import solve
import same_color_solve_1d
import same_color_solve_2d
import dics
import pandas as pd
import sys

data = pd.read_csv( sys.argv[ 1 ], sep = "\t", index_col = 0, header = 0 )
cubes = []

for line in range( data.shape[ 0 ] ):
    cubes.append( cube.cube( line + 1, data.iloc[ line, range( 6 ) ], data.iloc[ line, range( 6, 12 ) ] ) )

#if ( len( sys.argv ) == 4 ):
#    solve.solve_1d( cubes, dics.colors[ sys.argv[ 2 ] ], int( sys.argv[ 3 ] ) )
#elif ( len( sys.argv ) == 5 ):
#    solve.solve_2d( cubes, dics.colors[ sys.argv[ 2 ] ], int( sys.argv[ 3 ] ), int( sys.argv[ 4 ] ) )

if ( len( sys.argv ) == 3 ):
    same_color_solve_1d.solve_1d( cubes, int( sys.argv[ 2 ] ) )

if ( len( sys.argv ) == 4 ):
    same_color_solve_2d.solve_2d( cubes, int( sys.argv[ 2 ] ), int( sys.argv[ 3 ] ) )
