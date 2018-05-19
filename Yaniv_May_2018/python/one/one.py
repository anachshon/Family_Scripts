#!/usr/bin/env python

import math
import MyAudio
import MyGL
import MyGeom


myaudio = MyAudio.MyAudio()
mygl = MyGL.MyGL()
mygeom = MyGeom.MyGeom( 256, 64, 1.3, 2.5 )

fact = 1.0
delta = 1.0
delta_prev = 0.0

while( 1 ):

    data = myaudio.read()
    if ( len( data ) > 0 ):
    #    mygeom.scale_cur( math.atan( 100 * data[ 0 ] ) / math.pi + 1 )
        mygeom.scale_cur_z( data, fact )

    mygl.start_frame( delta )
    mygl.draw_mesh( mygeom.get_verts(), mygeom.get_norms() )
    #mygl.draw_cube()
    mygl.end_frame()

    cmd = mygl.handle_events()
    if ( cmd == 'esc' ):
        myaudio.__del__()
        exit()
    elif ( cmd == 'up' ):
        fact *= 2
    elif( cmd == 'down' ):
        fact /= 2
    elif ( cmd == 'sapce' ):
        tmp = delta
        delta = delta_prev
        delta_prev = tmp
    elif ( cmd == 'right' ):
        delta *= 2
    elif ( cmd == 'left' ):
        delta /= 2
    elif ( cmd == 'reset' ):
        mygeom.reset()