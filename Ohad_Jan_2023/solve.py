#!/usr/bin/env python3

import numpy as np
import cube
import dics
import copy

def solve_1d( cubes, color, length ):

    nof_cubes = len( cubes )
    nof_soln = 0

    def write_soln( solution ):

        nonlocal nof_soln

        nof_soln += 1
        line = [ nof_soln, ' : ' ]
        for n in range( len( solution ) ):
            line.append( '(' + str( n + 1 ) + ')' )
            cur_cube = solution[ n ]
            line += [
                       cur_cube.get_index(),
                       dics.colors_inv[ cur_cube.cols[ cur_cube.get_y() - 1 ] ],
                       dics.colors_inv[ cur_cube.cols[ cur_cube.get_x() - 1 ] ]
                    ]
        print( '\t'.join( [ str( x ) for x in line ] ) )

    def aux_solve( solution, used ):

#        new_solution = copy.deepcopy( solution )
#        new_used = copy.deepcopy( used )
        for n in range( nof_cubes ):
            if ( not used[ n ] and cubes[ n ].has_color( color ) ):
                cur_cube = copy.deepcopy( cubes[ n ] )
                cur_cube.set_y( cur_cube.has_color( color ) )
                for x in dics.valid_vals[ cur_cube.get_y() ]:
                    cur_cube.set_x( x )
                    if ( len( solution ) == 0 ):
                        #
                        #   on the first one nothing to check
                        #
                        new_solution = copy.deepcopy( solution )
                        new_used = copy.deepcopy( used )
                        new_solution.append( cur_cube )
                        new_used[ n ] = True
                        if ( len( new_solution ) == length ):
                            write_soln( new_solution )
                        else:
                            aux_solve( new_solution, new_used )
                    else:
                        #
                        #   we should check that the new (cur) one match the previou ones
                        #
                        prev_cube = solution[ -1 ]
                        if ( prev_cube.match_right( cur_cube ) ):
                            new_solution = copy.deepcopy( solution )
                            new_solution.append( cur_cube )
                            new_used = copy.deepcopy( used )
                            new_used[ n ] = True
                            if ( len( new_solution ) == length ):
                                write_soln( new_solution )
                            else:
                                aux_solve( new_solution, new_used )
                        else:
                            continue
#                else:
#                    for x in dics.valid_vals[ cur_cube.get_y() ]:
#                        cur_cube.set_x( x )
#                        aux_solve( new_solution, new_used )

    aux_solve( [], nof_cubes * [ False ] )
