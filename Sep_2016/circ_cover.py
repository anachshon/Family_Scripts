#!/usr/bin/env python

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import calc_dist
import my_image
import math

air_color = 255
diag_factor = math.sqrt( 2 )

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
                    dx = 0
                    while ( i + dx < self.nx and self.matrix[ i + dx, j ] == air_color ):
                        dx += 1
                    point_max_dist = min( point_max_dist, dx )
                    if ( point_max_dist > global_max_dist ):
                        dx = 0
                        while ( i - dx >= 0 and self.matrix[ i - dx, j ] == air_color ):
                            dx += 1
                        point_max_dist = min( point_max_dist, dx )
                        if ( point_max_dist > global_max_dist ):
                            dy = 0
                            while ( j + dy < self.ny and self.matrix[ i, j +  dy ] == air_color ):
                                dy += 1
                            point_max_dist = min( point_max_dist, dy )
                            if ( point_max_dist > global_max_dist ):
                                dy = 0
                                while ( i - dy >= 0 and self.matrix[ i, j - dy ] == air_color ):
                                    dy += 1
                                point_max_dist = min( point_max_dist, dy )

                                if ( point_max_dist > global_max_dist ):
                                    cen = ( i, j )
                                    global_max_dist = point_max_dist

        add_circ( self, cen , global_max_dist )
        return( [ cen, global_max_dist ])

def add_circ(self, tup1, rad ):

        i0 = max( 0, tup1[ 0 ] - rad - 1)
        i1 = min( tup1[ 0 ] + rad + 1 , self.nx )
        j0 = min( 0, tup1[ 1 ] - rad - 1 )
        j1 = max( tup1[ 1 ] + rad + 1, self.ny )
        for i in range(i0, i1):
            for j in range(j0, j1):
                tup2 = (i, j)
                if (self.calc.dist(tup1, tup2) < rad):
                    if ( self.matrix[i, j] == air_color):
                        self.matrix[i, j] = 128
                    else:
                        self.matrix[i, j] = 64

