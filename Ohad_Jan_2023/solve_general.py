#!/usr/bin/env python3

import sys
import dics
import copy
import random
import numpy as np
import pandas as pd
import time

def solve( cubes, pairs_file ):

    def read_inp():
        pairs = pd.read_csv( pairs_file, sep = "\t", header = 0 )
        shape_cubes = set( list( pairs.Cube_1 ) + list( pairs.Cube_2 ) )
        nof_shape_cubes = len( shape_cubes )
        magnets = {}
        for cube in shape_cubes:
            magnets[ cube - 1 ] = []
        for n in range( pairs.shape[ 0 ] ):
            C1 = pairs.Cube_1[ n ] - 1
            F1 = pairs.Face_1[ n ]
            C2 = pairs.Cube_2[ n ] - 1
            F2 = pairs.Face_2[ n ]
            if ( C1 < C2 ):
                magnets[ C2 ].append( ( C1, F1 ) )
            else:
                magnets[ C1 ].append( ( C2, F2 ) )

        col_define = np.zeros( ( nof_shape_cubes, dics.f.nof ), dtype = bool )
        col_define.fill( True )
        for cube in shape_cubes:
            for entry in magnets[ cube - 1 ]:
                C = entry[ 0 ]
                F = entry[ 1 ]
                col_define[ C, dics.f_inv[ F ] ] = False
        col_check = np.zeros( ( nof_shape_cubes, dics.f.nof ), dtype = bool )
        col_check.fill( False )
        for f in range( dics.f.nof ):
            change = False
            for c in range( nof_shape_cubes ):
                if ( change ):
                    col_define[ c, f ] = False
                    col_check[ c, f ] = True
                else:
                    if( col_define[ c, f ] == True ):
                        change = True
        for C1 in magnets:
            for entry in magnets[ C1 ]:
                C2 = entry[ 0 ]
                F2 = dics.f_inv[ entry[ 1 ] ]
                col_check[ C2, F2 ] = False
                col_check[ C1, dics.pairs[ F2 + 1 ] - 1 ] = False

        return( col_define, col_check, magnets )

    def write_soln( solution ):

        nonlocal nof_soln

        nof_soln += 1
        line = [ str( nof_soln ) + ' : ', ','.join( [ dics.colors_inv[ c ] for c in colors ] ) ]
        for n in range( len( solution ) ):
            line.append( '(' + str( n + 1 ) + ')' )
            cur_cube = solution[ n ]
            line += [
                       cur_cube.get_index(),
                       dics.colors_inv[ cur_cube.cols[ cur_cube.get_y() - 1 ] ],
                       dics.colors_inv[ cur_cube.cols[ cur_cube.get_x() - 1 ] ]
                    ]
        print( '\t'.join( [ str( x ) for x in line ] ) )
        exit()

    def aux_solve( solution, used ):

        random.seed( time.time() )
        nonlocal colors
        nonlocal nof_calls

        nof_calls += 1
        if ( nof_calls > 10000 ):
            exit()

        for n in random.sample( list( range( nof_cubes ) ), nof_cubes ):
            if ( not used[ n ] ):
                n_cur_cube = len( solution )
                if ( n_cur_cube == 0 ):
                    #
                    #   This is the first cube in the solution
                    #
                    cur_cube = copy.deepcopy( cubes[ n ] )
                    for y in range( 1, 7 ):
                        cur_cube.set_y( y )
                        for x in dics.valid_vals[ y ]:
                            cur_cube.set_x( x )
                            colors = 6 * [ -1 ]
                            for f in range( dics.f.nof ):
                                if ( define[ n_cur_cube, f ] ):
                                    colors[ f ] = cur_cube.get( f )[ 0 ]
                            new_solution = copy.deepcopy( solution )
                            new_used = copy.deepcopy( used )
                            new_solution.append( cur_cube )
                            new_used[ n ] = True
                            aux_solve( new_solution, new_used )
                else:
                    cur_cube = copy.deepcopy( cubes[ n ] )
                    #   does the candidate cube had at all the right colors
                    has_all_colors = True
                    for f in range( dics.f.nof ):
                        if ( check[ n_cur_cube, f ] and not cur_cube.has_color( colors[ f ] ) ):
                            has_all_colors = False
                            break
                    if ( has_all_colors ):
                        for y in range( 1, 7 ):
                            cur_cube.set_y( y )
                            for x in dics.valid_vals[ y ]:
                                cur_cube.set_x( x )
                                #   does the colors match the necessary defined colors
                                match_prev_colors = True
                                for f in range( dics.f.nof ):
                                    if ( check[ n_cur_cube, f ] and cur_cube.get( f )[ 0 ] != colors[ f ] ):
                                        match_prev_colors = False
                                        break
                                if ( match_prev_colors ):
                                    #   does the magnets match
                                    match_prev_magnets = True
                                    for entry in mags[ n_cur_cube ]:
                                        C_prev = solution[ entry[ 0 ] ]
                                        F_prev = dics.f_inv[ entry[ 1 ] ]
                                        if ( not C_prev.match_mag( F_prev, cur_cube ) ):
                                            match_prev_magnets = False
                                            break
                                    if( match_prev_magnets ):
                                        #   update colors if necesary
                                        for f in range( dics.f.nof ):
                                            if ( define[ n_cur_cube, f ] ):
                                                colors[ f ] = cur_cube.get( f )[ 0 ]
                                        new_solution = copy.deepcopy( solution )
                                        new_used = copy.deepcopy( used )
                                        new_solution.append( cur_cube )
                                        new_used[ n ] = True
                                        if ( len( new_solution ) == nof_shape_cubes ):
                                            write_soln( new_solution )
                                        else:
                                            aux_solve( new_solution, new_used )

    nof_cubes = len( cubes )
    nof_soln = 0
    nof_calls = 0

    define, check, mags = read_inp()
    nof_shape_cubes = define.shape[ 0 ]

    if ( '-d' in sys.argv ):
        print()
        print( '*** define ***' )
        print( define )
        print()
        print( '*** check ***' )
        print( check )
        print()
        print( '*** magnets ***' )
        for key in mags:
            print( key, mags[ key ] )
        print()
        exit()

    colors = 6 * [ -1 ]
#    print( define )
    aux_solve( [], nof_cubes * [ False ] )
