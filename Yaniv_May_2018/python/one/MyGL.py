#!/usr/bin/env python

import pygame
from pygame.locals import *

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    #from OpenGL.arrays import *
except ImportError:
    print ('There is problem with importing the opengl modules')
    raise SystemExit


class MyGL:

    def __init__( self, w = 1024, h = 1024 ):
        pygame.init()
        pygame.display.set_mode( ( w, h ), OPENGL | DOUBLEBUF )
        glEnable( GL_DEPTH_TEST )
        glEnable( GL_LIGHTING )
        glEnable( GL_LIGHT0 )
        glEnable( GL_LIGHT1 )

        glLightfv( GL_LIGHT0, GL_AMBIENT, [ 0.3, 0.3, 0.3, 1.0 ] )
        glLightfv( GL_LIGHT0, GL_DIFFUSE, [ 0.0, 1.0, 0.0, 1.0 ] )
        glLightfv( GL_LIGHT0, GL_POSITION, [ 10.0, 10.0, 0.0, 1.0 ] )

        #glLightfv( GL_LIGHT1, GL_AMBIENT, [ 1.0, 1.0, 1.0, 1.0 ] )
        glLightfv( GL_LIGHT1, GL_DIFFUSE, [ 0.0, 0.0, 1.0, 1.0 ] )
        glLightfv( GL_LIGHT1, GL_POSITION, [ -10.0, 10.0, 0.0, 1.0 ] )

        # setup the camera
        glMatrixMode( GL_PROJECTION )
        gluPerspective( 45.0, w / h, 0.1, 100.0 )   # setup lens
        glTranslatef( 0.0, -1.0, -5.0 )              # move back
        glRotatef( 25, 1, 0, 0 )                    # orbit higher

    def handle_events( self ):
        event = pygame.event.poll()
        if ( event.type == KEYDOWN and event.key == K_ESCAPE ):
            return( 'esc' )
        elif ( event.type == KEYDOWN and event.key == K_UP ):
            return( 'up' )
        elif ( event.type == KEYDOWN and event.key == K_DOWN ):
            return( 'down' )
        elif ( event.type == KEYDOWN and event.key == K_LEFT ):
            return( 'left' )
        elif ( event.type == KEYDOWN and event.key == K_RIGHT ):
            return( 'right' )
        elif ( event.type == KEYDOWN and event.key == K_SPACE ):
            return( 'sapce' )
        elif ( event.type == KEYDOWN and event.key == K_r ):
            return( 'reset' )
        elif ( event.type == KEYDOWN and event.key == K_s ):
            return( 'save' )
        else:
            return( '' )

    def start_frame( self, delta ):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotatef( delta, 0, delta, 0 )

    def end_frame( self ):
        pygame.display.flip()
        pygame.time.wait(100)

    def draw_lines( self, verts, norms = None, cols = None ):

        ( nc, nz, nd ) = verts.shape
        glLineWidth( 3 )
        glDisable( GL_LIGHTING )
        glColor3f( 1.0, 0, 0 )
        for ic in range( nc ):
            glBegin(GL_LINE_STRIP)
            for iz in range( nz ):
                glVertex3f( verts[ ic, iz, 0 ], verts[ ic, iz, 2 ], verts[ ic, iz, 1 ] )
            glEnd()
        for iz in range( nz ):
            glBegin(GL_LINE_STRIP)
            for ic in range( nc ):
                glVertex3f( verts[ ic, iz, 0 ], verts[ ic, iz, 2 ], verts[ ic, iz, 1 ] )
            glEnd()

    def draw_polys( self, verts, norms = None, cols = None ):

        ( nc, nz, nd ) = verts.shape

        glEnable( GL_LIGHTING )
        #glColor3f( .6, .6, .6 )
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [ .6, .6, .6, 1. ])
        for iz in range( nz - 1 ):
            glBegin( GL_TRIANGLE_STRIP )
            for ic in range( nc ):
                glNormal3f( norms[ ic, iz, 0 ], norms[ ic, iz, 2 ], norms[ ic, iz, 1 ] )
                glVertex3f( verts[ ic, iz, 0 ], verts[ ic, iz, 2 ], verts[ ic, iz, 1 ] )
#                glNormal3f( norms[ ic, iz + 1, 0 ], norms[ ic, iz + 1, 2 ], norms[ ic, iz + 1, 1 ] )
                glVertex3f( verts[ ic, iz + 1, 0 ], verts[ ic, iz + 1 , 2 ], verts[ ic, iz + 1, 1 ] )
            glEnd()

