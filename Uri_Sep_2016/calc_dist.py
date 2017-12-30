#!/usr/bin/env python

import os, sys, shutil
import numpy as np
import math

dic = {}
default_name = "./sqrt.npy"

class calc:

    def __init__( self, file_name = default_name ):

        global dic

        if ( os.path.exists( file_name ) and os.path.isfile( file_name ) ):
            dic = np.load( file_name ).item()

    def save( self, file_name = default_name ):
        np.save( file_name, dic )

    def dist( self, tup1, tup2 ):

        diff_1 = abs( tup1[ 0 ] - tup2[ 0 ] )
        diff_2 = abs( tup1[ 1 ] - tup2[ 1 ] )

        if ( diff_1 > diff_2 ):

            tmp = diff_1
            diff_1 = diff_2
            diff_2 = tmp

        tup = ( diff_1, diff_2 )
        if ( diff_1 + diff_2 < 200 ):
            if ( not tup in dic.keys() ):
                if ( tup[ 0 ] == 0 ):
                    dic[ tup ] = tup[ 1 ]
                else:
                    dic[ tup ] = math.sqrt( tup[ 0 ] * tup[ 0 ] + tup[ 1 ] * tup[ 1 ] )

            return( dic[ tup ] )
        else:
            return( 400 )