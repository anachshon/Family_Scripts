#!/usr/bin/env python3

import cube
import dics
import pandas as pd
import sys
import copy

data = pd.read_csv( sys.argv[ 1 ], sep = "\t", index_col = 0, header = 0 )
cubes = []

for line in range( data.shape[ 0 ] ):
    cubes.append( cube.cube( line + 1, data.iloc[ line, range( 6 ) ], data.iloc[ line, range( 6, 12 ) ] ) )

solns = pd.read_csv( sys.argv[ 2 ], sep = "\t", header = None )

nof_solns = solns.shape[ 0 ]
soln_size = int( ( solns.shape[ 1 ] - 2 ) / 4 )

num = int( sys.argv[ 3 ] ) - 1

for n in range( soln_size ):

    m = solns.iloc[ num, 2 + n * 4 + 1 ]
    y_color = solns.iloc[ num, 2 + 4 * n + 2 ]
    x_color = solns.iloc[ num, 2 + 4 * n + 3 ]

    cur_cube = copy.deepcopy( cubes[ m - 1 ] )
    y = cur_cube.has_color( dics.colors[ y_color ] )
    cur_cube.set_y( y )
    found = False
    for x in dics.valid_vals[ y ]:
        cur_cube.set_x( x )
        if ( cur_cube.get_right()[ 0 ] == dics.colors[ x_color ] ):
            found = True
            break
    if ( not  found ):
        print( "*** ERROR ***" )
        exit()
    print( m, y_color, x_color, y, x )
    print( cur_cube.get_right(), cur_cube.get_back(), cur_cube.get_left(), cur_cube.get_front(), cur_cube.get_up(), cur_cube.get_down() )
