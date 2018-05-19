#!/usr/bin/env python

import math
import MyAudio
import MyGL
import MyGeom


myaudio = MyAudio.MyAudio()
mygl = MyGL.MyGL()
mygeom = MyGeom.MyGeom( 80, 40, 1.3, 2.5 )

while( 1 ):

    data = myaudio.read()
    if ( len( data ) > 0 ):
    #    mygeom.scale_cur( math.atan( 100 * data[ 0 ] ) / math.pi + 1 )
        mygeom.scale_cur_z( data )

    mygl.start_frame()
    mygl.draw_mesh( mygeom.get_verts(), mygeom.get_norms() )
    #mygl.draw_cube()
    mygl.end_frame()

    cmd = mygl.handle_events()
    if ( cmd == 'esc' ):
        myaudio.__del__()
        exit()
