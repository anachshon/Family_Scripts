#!/usr/bin/env python

import math
import numpy as np
import datetime

class MyGeom:

    def __init__( self, nc = 11, nz = 11, rad = 1, h = 2 ):

        self.nc = nc
        self.nz = nz
        self.r = rad
        self.h = h

        self.cc = 0
        self.cz = 0

        self.delta_a = 2.0 * math.pi / ( nc - 1 )
        self.delta_z = float( h ) / ( nz - 1 )
        self.cos = np.array( [ math.cos( x * self.delta_a ) for x in range( self.nc + 1 ) ], dtype = np.float )
        self.sin = np.array( [ math.sin( x * self.delta_a ) for x in range( self.nc + 1 ) ], dtype = np.float )

        self.rs = np.ndarray( ( nc, nz ), dtype = np.float )
        self.rs.fill( self.r )
        self.verts = np.ndarray( ( nc, nz, 3 ), dtype = np.float )

        for iz in range( nz ):
            z = iz * self.delta_z
            factor = ( iz - 0.5 * self.nz ) / ( 0.5 * self.nz )
            circ_r = self.r * math.sqrt( 1 - factor * factor )
            for ic in range( nc ):
                self.rs[ ic, iz ] = circ_r
                self.verts[ ic, iz, 0 ] = self.rs[ ic, iz ] * self.cos[ ic ]
                self.verts[ ic, iz, 1 ] = self.rs[ ic, iz ] * self.sin[ ic ]
                self.verts[ ic, iz, 2 ] = z

        self.norms = np.ndarray((nc, nz, 3), dtype=np.float)

        for iz in range(nz):
            for ic in range(nc):
                self.norms[ic, iz, 0] = self.cos[ic]
                self.norms[ic, iz, 1] = self.sin[ic]
                self.norms[ic, iz, 2] = 0

    def reset( self ):
        for iz in range( self.nz ):
            z = iz * self.delta_z
            z = iz * self.delta_z
            factor = ( iz - 0.5 * self.nz ) / ( 0.5 * self.nz )
            circ_r = self.r * math.sqrt( 1 - factor * factor )
            for ic in range( self.nc ):
                self.rs[ ic, iz ] = circ_r
                self.verts[ ic, iz, 0 ] = self.rs[ ic, iz ] * self.cos[ ic ]
                self.verts[ ic, iz, 1 ] = self.rs[ ic, iz ] * self.sin[ ic ]
                self.verts[ ic, iz, 2 ] = z
        for iz in range( self.nz ):
            for ic in range( self.nc ):
                self.norms[ ic, iz, 0 ] = self.cos[ ic ]
                self.norms[ ic, iz, 1 ] = self.sin[ ic ]
                self.norms[ ic, iz, 2 ] = 0
        self.cz = 0

    def get_verts( self ):
        return( self.verts )

    def get_norms( self ):
        return( self.norms )

    def scale_cur( self, val ):
#        print( [ str( x ) + ' ' for x in [ self.cc, self.cz, val ] ] )
        self.rs[ self.cc, self.cz ] *= np.array( val ).mean()
        self.verts[ self.cc, self.cz, 0] = self.rs[ self.cc, self.cz ] * self.cos[ self.cc ]
        self.verts[ self.cc, self.cz, 1] = self.rs[ self.cc, self.cz ] * self.sin[ self.cc ]
        self.cc += 1
        if ( self.cc == self.nc ):
            self.cc = 0
            self.cz += 1
            if ( self.cz == self.nz ):
                self.cz = 0

    def scale_cur_z( self, vals, fact ):

        alpha = 0.45
        beta = 0.45

        arr = np.array( vals, dtype = np.float )
        min_val = arr.min()
        max_val = arr.max()

        delta = int( len( arr ) / ( self.nc -  1 ) )

        for ic in range( self.nc - 1 ):

            val = arr[ ( ic * delta ) : ( ( ic + 1 ) * delta ) ].mean()

            #print( str( ic ) + ' ' + str( val ) )
            factor = ( self.cz - 0.5 * self.nz ) / ( 0.5 * self.nz )
            circ_r = self.r * math.sqrt( 1 - factor * factor )
            new_val = circ_r + fact * ( val - min_val )
            czp = min( self.cz + 1, self.nz - 1 )
            czm = max( self.cz - 1, 0 )

            new_rad = ( 1 - alpha - beta ) * new_val + \
                  alpha * 0.5 * ( self.rs[ ic, czm] + self.rs[ ic, czp ] ) + \
                  beta * self.rs[ ic, self.cz ]
            self.rs[ ic, self.cz ] = new_rad
            #val = self.r + fact * val
            self.verts[ ic, self.cz, 0] = new_rad * self.cos[ ic ]
            self.verts[ ic, self.cz, 1] = new_rad * self.sin[ ic ]

        self.verts[ self.nc - 1, self.cz, 0] = self.verts[ 0, self.cz, 0]
        self.verts[ self.nc - 1, self.cz, 1] = self.verts[ 0, self.cz, 1]

        for iz in [ self.cz - 1, self.cz ]:
            if ( iz < 0 or iz >= ( self.nz - 1 ) ):
                continue
            for ic in range( self.nc - 1 ):
                vec1 = []
                vec2 = []
                for d in range( 3 ):
                    vec1.append( self.verts[ ic + 1, iz + 1,  d ] - self.verts[ ic, iz, d ] )
                    vec2.append( self.verts[ ic + 1, iz,  d ] - self.verts[ ic, iz + 1, d ] )
                norm_vec = np.cross( vec1, vec2 )
                norm_vec = norm_vec / np.linalg.norm( norm_vec )
                self.norms[ ic, iz, ] = -norm_vec
            self.norms[ self.nc - 1, iz, ] = self.norms[ 0, iz, ]


        self.cz += 1
        if ( self.cz == self.nz ):
            self.cz = 0
