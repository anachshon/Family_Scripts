#!/usr/bin/env python3

import cube
import dics
import copy

#
#   1D
#

def solve_1d( cubes, length ):

    nof_cubes = len( cubes )
    nof_soln = 0

    colors = 6 * [ -1 ]

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

        nonlocal colors

        for n in range( nof_cubes ):
            if ( not used[ n ] ):
                if ( len( solution ) == 0 ):
                    for y in range( 1, 7 ):
                        for x in dics.valid_vals[ y ]:
                            cur_cube = copy.deepcopy( cubes[ n ] )
                            cur_cube.set_y( y )
                            cur_cube.set_x( x )
                            colors[ dics.f.up ] = cur_cube.get_up()[ 0 ]
                            colors[ dics.f.down ] = cur_cube.get_down()[ 0 ]
                            colors[ dics.f.back ] = cur_cube.get_back()[ 0 ]
                            colors[ dics.f.front ] = cur_cube.get_front()[ 0 ]
                            new_solution = copy.deepcopy( solution )
                            new_used = copy.deepcopy( used )
                            new_solution.append( cur_cube )
                            new_used[ n ] = True
                            if ( len( new_solution ) == length ):
                                write_soln( new_solution )
                            else:
                                aux_solve( new_solution, new_used )
                else:
                    cur_cube = copy.deepcopy( cubes[ n ] )
                    y = cur_cube.has_color( colors[ dics.f.up ] )
                    if ( not y ):
                        continue
                    else:
                        cur_cube.set_y( y )
                        found = False
                        for x in dics.valid_vals[ y ]:
                            cur_cube.set_x( x )
                            if (
                                    cur_cube.get_down()[ 0 ] == colors[ dics.f.down ] and
                                    cur_cube.get_front()[ 0 ] == colors[ dics.f.front ] and
                                    cur_cube.get_back()[ 0 ] == colors[ dics.f.back ]
                                ):
                                found = True
                                break
                        if ( not found ):
                            continue
                        else:
                            prev_cube = solution[ -1 ]
                            if ( not prev_cube.match_right( cur_cube ) ):
                                continue
                            else:
                                new_solution = copy.deepcopy( solution )
                                new_used = copy.deepcopy( used )
                                new_solution.append( cur_cube )
                                new_used[ n ] = True
                                if ( len( new_solution ) == length ):
                                    write_soln( new_solution )
                                else:
                                    aux_solve( new_solution, new_used )

    aux_solve( [], nof_cubes * [ False ] )
