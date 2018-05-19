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

    def draw_cube( self ):

        CUBE_POINTS = (
            (0.5, -0.5, -0.5), (0.5, 0.5, -0.5),
            (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5),
            (0.5, -0.5, 0.5), (0.5, 0.5, 0.5),
            (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5)
        )

        CUBE_COLORS = (
            (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0),
            (1, 0, 1), (1, 1, 1), (0, 0, 1), (0, 1, 1)
        )

        CUBE_QUAD_VERTS = (
            (0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
            (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6)
        )

        CUBE_EDGES = (
            (0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7),
            (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7),
        )

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glRotatef(1, 0, 1, 0)

        allpoints = list(zip(CUBE_POINTS, CUBE_COLORS))

        glBegin(GL_QUADS)
        for face in CUBE_QUAD_VERTS:
            for vert in face:
                pos, color = allpoints[vert]
                glColor3fv(color)
                glVertex3fv(pos)
        glEnd()

        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINES)
        for line in CUBE_EDGES:
            for vert in line:
                pos, color = allpoints[vert]
                glVertex3fv(pos)

        glEnd()

        pygame.display.flip()
        pygame.time.wait(10)

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
        else:
            return( '' )

    def start_frame( self, delta ):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotatef( delta, 0, delta, 0 )

    def end_frame( self ):
        pygame.display.flip()
        pygame.time.wait(1)

    def draw_mesh( self, verts, norms = None, cols = None ):

        ( nc, nz, nd ) = verts.shape

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

