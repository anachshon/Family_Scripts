#!/usr/bin/env python

import math
import MyAudio
import MyGL
import MyGeom


myaudio = MyAudio.MyAudio()
mygl = MyGL.MyGL()
mygeom = MyGeom.MyGeom( 30, 60, 1.3, 2.5 )

while( 1 ):

    data = myaudio.read()
    if ( len( data ) > 0 ):
        mygeom.scale_cur( math.atan( 1000 * data[ 0 ] ) / math.pi + 1 )
    mygl.handle_events()
    mygl.start_frame()
    mygl.draw_mesh( mygeom.get_verts() )
    #mygl.draw_cube()
    mygl.end_frame()

