#!/usr/bin/env python3

import cube
import dics
import copy
import random
import numpy as np
import pandas as pd

def solve( cubes, pairs_file ):

    pairs = pd.read_csv( pairs_file, sep = "\t", header = 0 )
    shape_cubes = set( list( pairs.Cube_1 ) + list( pairs.Cube_2 ) )
    nof_shape_cubes = len( shape_cubes )
    magnets = {}
    for cube in shape_cubes:
        magnets[ cube ] = []
    for n in range( pairs.shape[ 0 ] ):
        C1 = pairs.Cube_1[ n ]
        F1 = pairs.Face_1[ n ]
        C2 = pairs.Cube_2[ n ]
        F2 = pairs.Face_2[ n ]
        if ( C1 < C2 ):
            magnets[ C2 ].append( ( F2, C1, F1 ) )
        else:
            magnets[ C1 ].append( ( F1, C2, F2 ) )

    col_define = np.zeros( ( nof_shape_cubes, dics.f.nof ), dtype = bool )
    col_define.fill( True )
    for cube in shape_cubes:
        for entry in magnets[ cube ]:
            C = entry[ 1 ] - 1
            F = entry[ 2 ]
            print( C, F )
            col_define[ C, dics.f_inv[ F ] ] = False
    col_check = np.zeros( ( nof_shape_cubes, dics.f.nof ), dtype = bool )
    col_check.fill( False )
    for f in range( dics.f.nof ):
        change = False
        for c in range( nof_shape_cubes ):
            if ( change ):
                col_define[c, f] = False
                col_check[c, f] = True
            else:
                if( col_define[ c, f ] == True ):
                    change = True

#   print( "pairs" )
#   print( pairs )
#   print( "magnets" )
#   print( magnets )
#   print( "define" )
#   print( col_define )
#   print( "check" )
#   print( col_check )
#   exit()

def solve_2d( cubes, length_x, length_y ):

    nof_cubes = len( cubes )
    nof_soln = 0

    colors = 6 * [ -1 ]

    def write_soln( solution ):

        nonlocal nof_soln

        nof_soln += 1
        line = [ str( nof_soln ) + ' : ', ','.join( [ dics.colors_inv[ c ] for c in colors ] ) ]
        for n in range( len( solution ) ):              #       y
            for m in range( len( solution[ n ] ) ):     #   x
                line.append( '(' + str( m + 1 ) + ',' + str( n + 1 ) + ')' )
                cur_cube = solution[ n ][ m ]
                line += [
                           cur_cube.get_index(),
                           dics.colors_inv[ cur_cube.cols[ cur_cube.get_y() - 1 ] ],
                           dics.colors_inv[ cur_cube.cols[ cur_cube.get_x() - 1 ] ]
                        ]
        print( '\t'.join( [ str( x ) for x in line ] ) )

    def aux_solve( solution, used ):

        nonlocal colors

        for n in random.sample( list( range( nof_cubes ) ), nof_cubes ):
            if ( not used[ n ] ):
                if ( len( solution ) == 0 ):
                    #
                    #   This is the first cube in the solution
                    #
                    for y in range( 1, 7 ):
                        for x in dics.valid_vals[ y ]:
                            cur_cube = copy.deepcopy( cubes[ n ] )
                            cur_cube.set_y( y )
                            cur_cube.set_x( x )
                            colors[ dics.f.up ] = cur_cube.get_up()[ 0 ]
                            colors[ dics.f.down ] = cur_cube.get_down()[ 0 ]
                            colors[ dics.f.back ] = cur_cube.get_back()[ 0 ]
                            colors[ dics.f.left ] = cur_cube.get_left()[ 0 ]
                            new_solution = copy.deepcopy( solution )
                            new_used = copy.deepcopy( used )
                            new_solution.append( [ cur_cube ] )
                            new_used[ n ] = True
                            aux_solve( new_solution, new_used )
                else:
                    cur_cube = copy.deepcopy( cubes[ n ] )
                    y = cur_cube.has_color( colors[ dics.f.up ] )
                    if ( not y ):
                        continue
                    else:
                        cur_cube.set_y( y )
                        if ( cur_cube.get_down()[ 0 ] != colors[ dics.f.down ] ):
                            continue
                        else:
                            if ( len( solution ) == 1 and len( solution[ 0 ] ) < length_x ):
                                #
                                #   we are in the first line, we should check back color and right match
                                #
                                match = False
                                for x in dics.valid_vals[ y ]:
                                    cur_cube.set_x( x )
                                    if ( cur_cube.get_back()[ 0 ] == colors[ dics.f.back ] ):
                                        match = True
                                        break
                                if ( not match ):
                                    continue
                                else:
                                    prev_cube = solution[ 0 ][ -1 ]
                                    if ( not prev_cube.match_right( cur_cube ) ):
                                        continue
                                    else:
                                        new_solution = copy.deepcopy( solution )
                                        new_used = copy.deepcopy( used )
                                        new_solution[ 0 ].append( cur_cube )
                                        new_used[ n ] = True
                                        if ( len( new_solution[ 0 ] ) == length_x ):
                                            colors[ dics.f.right ] = cur_cube.get_right()[ 0 ]
                                        aux_solve( new_solution, new_used )
                            else:
                                if ( len( solution[ len( solution ) - 1 ] ) == length_x ):
                                    #
                                    #   We are opening a new line
                                    #
                                    match = False
                                    for x in dics.valid_vals[ y ]:
                                        cur_cube.set_x( x )
                                        if ( cur_cube.get_left()[ 0 ] == colors[ dics.f.left ] ):
                                            match = True
                                            break
                                    if ( not match ):
                                        continue
                                    else:
                                        prev_line_cube = solution[ len( solution ) - 1 ][ 0 ]
                                        if ( not prev_line_cube.match_front( cur_cube ) ):
                                            continue
                                        else:
                                            new_solution = copy.deepcopy( solution )
                                            new_used = copy.deepcopy( used )
                                            new_solution.append( [ cur_cube ] )
                                            new_used[ n ] = True
                                            if ( len( new_solution ) == length_y ):
                                                colors[ dics.f.front ] = cur_cube.get_front()[ 0 ]
                                            aux_solve( new_solution, new_used )
                                else:
                                    for x in dics.valid_vals[ y ]:
                                        cur_cube.set_x( x )
                                        if ( len( solution ) == length_y and cur_cube.get_front()[ 0 ] != colors[ dics.f.front ] ):
                                            continue
                                        else:
                                            if ( len( solution[ len( solution ) - 1 ] ) == ( length_x - 1 ) and
                                                        cur_cube.get_right()[ 0 ] != colors[ dics.f.right ] ):
                                                continue
                                            else:
                                                prev_line_cube = solution[ len( solution ) - 2 ][ len( solution[ len( solution ) - 1 ] ) ]
                                                if ( not prev_line_cube.match_front( cur_cube ) ):
                                                    continue
                                                else:
                                                    prev_cube = solution[ len( solution ) - 1 ][ -1 ]
                                                    if ( not prev_cube.match_right( cur_cube ) ):
                                                        continue
                                                    else:
                                                        new_solution = copy.deepcopy( solution )
                                                        new_used = copy.deepcopy( used )
                                                        new_solution[ len( new_solution ) - 1 ].append( cur_cube )
                                                        new_used[ n ] = True
                                                        if ( len( new_solution ) == length_y and len( new_solution[ len( new_solution ) - 1 ] ) == length_x ):
                                                            write_soln( new_solution )
                                                        else:
                                                            aux_solve( new_solution, new_used )

    aux_solve( [], nof_cubes * [ False ] )
