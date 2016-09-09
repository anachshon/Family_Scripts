#!/usr/bin/env python

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import calc_dist
import my_image

class circ_cover( my_image.my_image ):

#    def __init__(self, file_name ):
#        my_image.my_image.__init__( self, file_name )

    def find_best(self):

        cen = ( -1, -1 )
        max_dist = 0
        for i in range( self.nx ):
            for j in range( self.ny ):
                if ( self.matrix[ i, j ] == 0 ):
                    dx = 0
                    while ( i + dx < self.nx and self.matrix[ i + dx, j ] == 0  ):
                        dx += 1
                    if ( dx > max_dist )
                        max_dist = dx
                        cen = ( i, j )
                        dx = 0
                        while (i - dx >= 0 and self.matrix[i + dx, j] == 0):
                            dx += 1
                        if (dx > max_dist)
                            max_dist = dx
                            cen = (i, j)

def add_circ(self, tup1, rad ):

        i0 = max( 0, tup1[ 0 ] - rad - 1)
        i1 = min( tup1[ 0 ] + rad + 1 , self.nx )
        j0 = min( 0, tup1[ 1 ] - rad - 1 )
        j1 = max( tup1[ 1 ] + rad + 1, self.ny )
        for i in range(i0, i1):
            for j in range(j0, j1):
                tup2 = (i, j)
                if (self.calc.dist(tup1, tup2) < rad):
                    self.matrix[i, j] = 128

