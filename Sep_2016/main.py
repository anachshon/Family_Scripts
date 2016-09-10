#!/usr/bin/env python

import os, sys, shutil
import my_image
import calc_dist
import circ_cover

calc = calc_dist.calc()
im = circ_cover.circ_cover( sys.argv[ 1 ] )
for i in range( 100 ):
    [ cen, rad ] = im.find_best()
    print( str( rad ) + '   ' + str( cen ) )
    im.save( sys.argv[2] + '/' + str( i ).zfill( 10 ) + '.tif' )
    print(i)
im.show()
calc.save()
