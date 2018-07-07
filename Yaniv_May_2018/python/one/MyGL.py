#!/usr/bin/env python

import pygame
from pygame.locals import *
import math

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    #from OpenGL.arrays import *
except ImportError:
    print ('There is problem with importing the opengl modules')
    raise SystemExit


class MyGL:

    def __init__( self, anim_length, w = 1280, h = 800 ):
        pygame.init()
        pygame.display.set_mode( ( w, h ), OPENGL | DOUBLEBUF | RESIZABLE )
        glEnable( GL_DEPTH_TEST )
        glEnable( GL_LIGHTING )
        glEnable( GL_LIGHT0 )
        glEnable( GL_LIGHT1 )

        glLightfv( GL_LIGHT0, GL_AMBIENT, [ 0.3, 0.3, 0.3, 1.0 ] )
        glLightfv( GL_LIGHT0, GL_DIFFUSE, [ 0.0, 0.7, 0.0, 1.0 ] )
        glLightfv( GL_LIGHT0, GL_POSITION, [ 10.0, 10.0, 0.0, 1.0 ] )

        #glLightfv( GL_LIGHT1, GL_AMBIENT, [ 1.0, 1.0, 1.0, 1.0 ] )
        glLightfv( GL_LIGHT1, GL_DIFFUSE, [ 0.0, 0.0, 0.7, 1.0 ] )
        glLightfv( GL_LIGHT1, GL_POSITION, [ -10.0, 10.0, 0.0, 1.0 ] )

        # setup the camera
        glMatrixMode( GL_PROJECTION )
        #gluPerspective( 45.0, w / h, 0.1, 100.0 )   # setup lens
        #glTranslatef( 0.0, -10.0, -50.0 )              # move back
        #glRotatef( 15, 1, 0, 0 )                    # orbit higher
        #gluLookAt( 0, -1, -8, 0, 1, 0, 0, 1, 0 )

        self.rot_angle = 0
        self.cam_x = 0
        self.cam_y = 1
        self.cam_z = -5

        self.cam_start_factor_y = 1.0
        self.cam_end_factor_y = 1.0
        self.cam_start_factor_z = 12.0
        self.cam_end_factor_z = 1.0

        self.cam_anim_length = anim_length
        self.fac_exp = 10 ** ( math.log10( self.cam_start_factor_z ) / self.cam_anim_length )

        self.cam_anim_frame = 0

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
        elif ( event.type == KEYDOWN and event.key == K_t ):
            return( 'toggle' )
        else:
            return( '' )

    def start_frame( self, delta, counter ):
        self.cam_anim_frame = counter
        glLoadIdentity( )
        gluPerspective( 45.0, 1, 0.1, 100.0 )
        if ( self.cam_anim_frame <= self.cam_anim_length ):
            ratio = float( self.cam_anim_frame ) / float( self.cam_anim_length )
            factor_y = ratio * self.cam_end_factor_y + ( 1.0 - ratio ) * self.cam_start_factor_y
            #factor_z = ratio * self.cam_end_factor_z + ( 1.0 - ratio ) * self.cam_start_factor_z

            factor_z = self.fac_exp ** ( float( self.cam_anim_length ) - float( self.cam_anim_frame ) )
        else:
            factor_y = self.cam_end_factor_y
            factor_z = self.cam_end_factor_z
        #print( factor )
        gluLookAt( self.cam_x, factor_y * self.cam_y, factor_z * self.cam_z, 0, 1.0, 0, 0, 1, 0 )
        #glDepthRange( 0.1, 100 )
        #glTranslatef( 0.0, 0.5, 0.5 )
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
        glRotatef( self.rot_angle, 0, self.rot_angle, 0 )
        self.rot_angle += delta

    def end_frame( self ):
        pygame.display.flip()
        pygame.time.wait(0)

    def draw_lines( self, verts, norms = None, cols = None ):

        ca = math.cos( ( -self.rot_angle + 90 ) * math.pi / 180.0 )
        sa = math.sin( ( -self.rot_angle + 90 ) * math.pi / 180.0 )
        ( nc, nz, nd ) = verts.shape
        glLineWidth( 1 )
        #glDepthFunc( GL_ALWAYS )
        glDisable( GL_LIGHTING )
        #glColor3f( 1.0, 0, 0 )
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [ .6, .6, .6, 1. ])
        for ic in range( nc ):
            glBegin(GL_LINE_STRIP)
            for iz in range( nz ):
                x = verts[ ic, iz, 0 ]
                y = verts[ ic, iz, 1 ]
                perp = - x * ca + y * sa
                glColor3f( perp + 1, 0, 0  )
                glVertex3f( 1.001 * verts[ ic, iz, 0 ], 1.001 * verts[ ic, iz, 2 ], verts[ ic, iz, 1 ] )
            glEnd()
        for iz in range( nz ):
            glBegin(GL_LINE_STRIP)
            for ic in range( nc ):
                x = verts[ ic, iz, 0 ]
                y = verts[ ic, iz, 1 ]
                perp = -x * ca + y * sa
                glColor3f( perp + 1, 0, 0  )
                glVertex3f( 1.001 * verts[ ic, iz, 0 ], 1.001 * verts[ ic, iz, 2 ], verts[ ic, iz, 1 ] )
            glEnd()

    def draw_polys( self, verts, norms = None, cols = None ):

        ( nc, nz, nd ) = verts.shape

        #glDepthFunc( GL_GEQUAL )
        glEnable( GL_LIGHTING )
        #glDisable( GL_LIGHTING )
        #glColor3f( .6, .6, .6 )
        if ( self.cam_anim_frame <= self.cam_anim_length ):
            col = 0.6 * float( self.cam_anim_frame ) / float( self.cam_anim_length )
        else:
            col = 0.6
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [ col, col, col, 1. ])
        for iz in range( nz - 1 ):
            glBegin( GL_TRIANGLE_STRIP )
            for ic in range( nc ):
                glNormal3f( norms[ ic, iz, 0 ], norms[ ic, iz, 2 ], norms[ ic, iz, 1 ] )
                glVertex3f( verts[ ic, iz, 0 ], verts[ ic, iz, 2 ], verts[ ic, iz, 1 ] )
#                glNormal3f( norms[ ic, iz + 1, 0 ], norms[ ic, iz + 1, 2 ], norms[ ic, iz + 1, 1 ] )
                glVertex3f( verts[ ic, iz + 1, 0 ], verts[ ic, iz + 1 , 2 ], verts[ ic, iz + 1, 1 ] )
            glEnd()

    def draw_points(self, verts ):
        ca = math.cos( ( -self.rot_angle + 90 ) * math.pi / 180.0 )
        sa = math.sin( ( -self.rot_angle + 90 ) * math.pi / 180.0 )
        ( nc, nz, nd ) = verts.shape

        prev_depth_func = glGetIntegerv( GL_DEPTH_FUNC )
        glDepthFunc( GL_ALWAYS )
        glDisable( GL_LIGHTING )
        glPointSize( 3 )
        glBegin( GL_POINTS )
        for iz in range( nz ):
            for ic in range( nc ):
                x = verts[ ic, iz, 0 ]
                y = verts[ ic, iz, 1 ]
                perp = - x * ca + y * sa
                glColor3f( perp + 1, perp + 1, perp + 1  )
                glVertex3f( 1.001 * verts[ ic, iz, 0 ], 1.001 * verts[ ic, iz , 2 ], verts[ ic, iz, 1 ] )
        glEnd()
        glDepthFunc( prev_depth_func )
