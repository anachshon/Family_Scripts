#!/usr/bin/env python

import math
import MyAudio
import MyGL
import MyGeom


myaudio = MyAudio.MyAudio()
mygl = MyGL.MyGL()
mygeom = MyGeom.MyGeom( 64, 64, 0.5, 2.5 )

fact = 1.0
delta = 1.0
delta_prev = 0.0

while( 1 ):

    data = myaudio.read()
    if ( len( data ) > 0 ):
    #    mygeom.scale_cur( data )
        mygeom.scale_cur_z( data, fact )

    mygl.start_frame( delta )
    mygl.draw_polys( mygeom.get_verts(), mygeom.get_norms() )
    mygl.draw_lines( mygeom.get_verts(), mygeom.get_norms() )
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
    elif ( cmd == 'save' ):
        mygeom.save()