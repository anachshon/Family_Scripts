#!/usr/bin/env python3
import os

import cube
import solve
import same_color_solve_1d
import same_color_solve_2d
import solve_general
import dics
import pandas as pd
import sys
import runpy

data = pd.read_csv( sys.argv[ 1 ], sep = "\t", index_col = 0, header = 0 )
cubes = []

for line in range( data.shape[ 0 ] ):
    cubes.append( cube.cube( line + 1, data.iloc[ line, range( 6 ) ], data.iloc[ line, range( 6, 12 ) ] ) )

match sys.argv[ 2 ]:
    case '1d':
        same_color_solve_1d.solve_1d( cubes, int(sys.argv[ 3 ] ) )
    case '2d':
        same_color_solve_2d.solve_2d( cubes, int( sys.argv[ 3 ] ), int( sys.argv[ 4 ] ) )
    case 'gen':
        solve_general.solve( cubes, sys.argv[ 3 ] )
    case other:
        print( 'The second argument should be either 1d, 2d, or gen' )
        exit()
