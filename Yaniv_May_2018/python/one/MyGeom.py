#!/usr/bin/env python

import math
import numpy as np

class MyGeom:

    def __init__( self, nc = 11, nz = 11, rad = 1, h = 2 ):

        self.nc = nc
        self.nz = nz
        self.r = rad
        self.h = h

        self.cc = 0
        self.cz = 0

        delta_a = 2.0 * math.pi / ( nc - 1 )
        delta_z = float( h ) / ( nz - 1 )
        self.cos = np.array( [ math.cos( x * delta_a ) for x in range( self.nc + 1 ) ], dtype = np.float )
        self.sin = np.array( [ math.sin( x * delta_a ) for x in range( self.nc + 1 ) ], dtype = np.float )

        self.rs = np.ndarray( ( nc, nz ), dtype = np.float )
        self.rs.fill( self.r )
        self.verts = np.ndarray( ( nc, nz, 3 ), dtype = np.float )

        for iz in range( nz ):
            z = iz * delta_z
            for ic in range( nc ):
                self.verts[ ic, iz, 0 ] = self.rs[ ic, iz ] * self.cos[ ic ]
                self.verts[ ic, iz, 1 ] = self.rs[ ic, iz ] * self.sin[ ic ]
                self.verts[ ic, iz, 2 ] = z

        self.norms = np.ndarray((nc, nz, 3), dtype=np.float)

        for iz in range(nz):
            for ic in range(nc):
                self.norms[ic, iz, 0] = self.cos[ic]
                self.norms[ic, iz, 1] = self.sin[ic]
                self.norms[ic, iz, 2] = 0

    def get_verts( self ):
        return( self.verts )

    def get_norms( self ):
        return( self.norms )

    def scale_cur( self, val ):
#        print( [ str( x ) + ' ' for x in [ self.cc, self.cz, val ] ] )
        self.rs[ self.cc, self.cz ] *= val
        self.verts[ self.cc, self.cz, 0] = self.rs[ self.cc, self.cz ] * self.cos[ self.cc ]
        self.verts[ self.cc, self.cz, 1] = self.rs[ self.cc, self.cz ] * self.sin[ self.cc ]
        self.cc += 1
        if ( self.cc == self.nc ):
            self.cc = 0
            self.cz += 1
            if ( self.cz == self.nz ):
                self.cz = 0
