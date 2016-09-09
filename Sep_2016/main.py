#!/usr/bin/env python

import os, sys, shutil
import my_image
import calc_dist
import circ_cover

calc = calc_dist.calc()
im = circ_cover.circ_cover( sys.argv[ 1 ] )
#im.show()
im.add_circ( (10,10), 20)
im.add_circ( (100,100), 30)
im.add_circ( ( 200,220), 50)
im.show()
im.save( sys.argv[ 2 ] )
calc.save()
