#!/usr/bin/env python

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import calc_dist

class my_image:

    def __init__( self, file_name ):

        self.image = Image.open( file_name )

        matrix = np.asarray( self.image )

        ( self.ny, self.nx ) = self.image.size

        self.calc = calc_dist.calc( "" )

        print( self.image.info )
        print( self.image.mode )

        self.matrix = np.ndarray((self.nx, self.ny), dtype=np.uint8)
        for i in range(0, self.nx, 1):
            for j in range(0, self.ny, 1):
                self.matrix[ i, j ]  = matrix[ i, j ]

    def show( self ):

        self.image = Image.fromarray( self.matrix, 'L' )
        plt.imshow( self.image, cmap = 'Greys_r' )
        plt.show()

    def save( self, file_name ):

        self.image = Image.fromarray( self.matrix, 'L' )
        self.image.save( file_name, 'tiff' )