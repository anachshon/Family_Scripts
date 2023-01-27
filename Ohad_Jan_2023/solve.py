#!/usr/bin/env python3

import cube
import dics
import copy

#
#   1D
#

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

    aux_solve( [], nof_cubes * [ False ] )

#
#   2D
#

def solve_2d( cubes, color, length_x, length_y ):

    nof_cubes = len( cubes )
    nof_soln = 0

    def write_soln( solution ):

        nonlocal nof_soln

        nof_soln += 1
        line = [ nof_soln, ' : ' ]
        for n in range( len( solution ) ):
            for m in range( len( solution[ n ] ) ):
                line.append( '(' + str( n + 1 ) + ',' + str( m + 1 ) + ')' )
                cur_cube = solution[ n ][ m ]
                line += [
                           cur_cube.get_index(),
                           dics.colors_inv[ cur_cube.cols[ cur_cube.get_y() - 1 ] ],
                           dics.colors_inv[ cur_cube.cols[ cur_cube.get_x() - 1 ] ]
                        ]
        print( '\t'.join( [ str( x ) for x in line ] ) )

    def aux_solve( solution, used ):

#        if ( len( solution ) > 0 ):
#            print( len( solution ), len( solution[ len( solution ) - 1 ] ) )
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
                        new_solution.append( [ cur_cube ] )
                        new_used[ n ] = True
                        if ( len( new_solution ) == length_y and len( new_solution[ length_y - 1 ] ) == length_x ):
                            write_soln( new_solution )
                        else:
                            aux_solve( new_solution, new_used )
                    else:
                        #
                        #   we should check that the new (cur) one match the previou ones
                        #
                        if ( len( solution ) == 1 and len( solution[ 0 ] ) < length_x ):
                            #
                            #   we are still in the first line
                            #
                            prev_cube = solution[ 0 ][ -1 ]
                            if ( prev_cube.match_right( cur_cube ) ):
                                new_solution = copy.deepcopy( solution )
                                new_solution[ 0 ].append( cur_cube )
                                new_used = copy.deepcopy( used )
                                new_used[ n ] = True
                                if ( len( new_solution ) == length_y and len( new_solution[ length_y - 1 ] ) == length_x ):
                                    write_soln( new_solution )
                                else:
                                    aux_solve( new_solution, new_used )
                        else:
                            #
                            #   we are in 2nd, 3rd, ... line we should check match also between the lines
                            #
                            nof_lines = len( solution )
                            if ( len( solution[ nof_lines - 1 ] ) == length_x  ):
                                #
                                #   we are opening a new line so we should check just with the previous line
                                #
                                prev_line_cube = solution[ nof_lines - 1 ][ 0 ]
                                if ( prev_line_cube.match_front( cur_cube ) ):
                                    new_solution = copy.deepcopy( solution )
                                    new_solution.append( [ cur_cube ] )
                                    new_used = copy.deepcopy( used )
                                    new_used[ n ] = True
                                    if ( len( new_solution ) == length_y and len( new_solution[ length_y - 1 ] ) == length_x ):
                                        write_soln( new_solution )
                                    else:
                                        aux_solve( new_solution, new_used )
                            else:
                                #
                                #   we are adding to the last line, so we should check both in the line and to the previous line
                                #
                                prev_cube = solution[ nof_lines - 1 ][ -1 ]
                                prev_line_cube = solution[ nof_lines - 2 ][ len( solution[ nof_lines - 1 ] ) ]
                                if ( prev_line_cube.match_front( cur_cube ) and prev_cube.match_right( cur_cube ) ):
                                    new_solution = copy.deepcopy( solution )
                                    new_solution[ nof_lines - 1 ].append( cur_cube )
                                    new_used = copy.deepcopy( used )
                                    new_used[ n ] = True
                                    if ( len( new_solution ) == length_y and len( new_solution[ length_y - 1 ] ) == length_x ):
                                        write_soln( new_solution )
                                    else:
                                        aux_solve( new_solution, new_used )
            else:
                continue

    aux_solve( [], nof_cubes * [ False ] )

