#!/usr/bin/env python

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import calc_dist
import my_image
import math

air_color = 255
diag_factor = math.sqrt( 2 )

dirs = [ (1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
facs = 4 * [1] + 4 * [diag_factor]
nof_dirs = 8

class circ_cover( my_image.my_image ):

#    def __init__(self, file_name ):
#        my_image.my_image.__init__( self, file_name )

    def find_best(self):

        cen = ( -1, -1 )
        global_max_dist = 0
        for i in range( self.nx ):
            for j in range( self.ny ):
                if ( self.matrix[ i, j ] == air_color ):
                    point_max_dist = 999999
                    dir = 0
                    while ( dir < nof_dirs and point_max_dist > global_max_dist ):
                        d = 0
                        si = i
                        sj = j
                        while ( si >= 0 and si < self.nx and sj >= 0 and sj < self.ny and self.matrix[ si, sj ] == air_color ):
                            si += dirs[ dir ][ 0 ]
                            sj += dirs[ dir ][ 1 ]
                            d += 1
                        point_max_dist = min( point_max_dist, int( d * facs[ dir ] ) )
                        dir += 1

                    if ( point_max_dist > global_max_dist ):
                        cen = ( i, j )
                        global_max_dist = point_max_dist

        self.add_circ( cen , global_max_dist )
        print(str(global_max_dist) + '   ' + str(cen))
        return( [ cen, global_max_dist ])


    def find_all(self, large_enough):
        cen = (-1, -1)
        global_max_dist = 0
        for i in range(self.nx):
            for j in range(self.ny):
                if (self.matrix[i, j] == air_color):
                    point_max_dist = 999999
                    dir = 0
                    while (dir < nof_dirs and point_max_dist > global_max_dist):
                        d = 0
                        si = i
                        sj = j
                        while (si >= 0 and si < self.nx and sj >= 0 and sj < self.ny and self.matrix[si, sj] == air_color):
                            si += dirs[dir][0]
                            sj += dirs[dir][1]
                            d += 1
                        point_max_dist = min(point_max_dist, int(d * facs[dir]))
                        dir += 1

                    if (point_max_dist == large_enough):
                        self.add_circ( (i, j), point_max_dist)
                        print(str(point_max_dist) + '   ' + str((i, j)))

    def add_circ(self, tup1, rad ):

        i0 = max( 0, tup1[ 0 ] - rad - 1)
        i1 = min( tup1[ 0 ] + rad + 1 , self.nx )
        j0 = max( 0, tup1[ 1 ] - rad - 1 )
        j1 = min( tup1[ 1 ] + rad + 1, self.ny )
        for i in range(i0, i1):
            for j in range(j0, j1):
                tup2 = (i, j)
                if (self.calc.dist(tup1, tup2) <= rad):
                    if ( self.matrix[i, j] == air_color):
                        self.matrix[i, j] = 128
                    else:
                        self.matrix[i, j] = 64

