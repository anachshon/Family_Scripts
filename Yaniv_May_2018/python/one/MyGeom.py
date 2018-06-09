#!/usr/bin/env python

import math
import numpy as np
import datetime
from stl import mesh
import os

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

        self.cap_size = 5   # number of points

        for iz in range( nz ):
            z = iz * self.delta_z
            #factor = ( iz - 0.5 * ( self.nz - 1 ) ) / ( 0.5 * ( self.nz - 1 ) )
            #circ_r = self.r * math.sqrt( 1 - factor * factor )
            circ_r = self.calc_radius( iz )
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

        self.max_untrunc = -9999

    def reset( self ):
        for iz in range( self.nz ):
            z = iz * self.delta_z
            z = iz * self.delta_z
            #factor = ( iz - 0.5 * self.nz ) / ( 0.5 * self.nz )
            #circ_r = self.r * math.sqrt( 1 - factor * factor )
            circ_r = self.calc_radius( iz )
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

    def scale_cur_z( self, vals, fact, mode ):

        if ( mode == "normal" ):
            alpha = 0.4
            beta = 0.1
            gamma = 0.1
        elif ( mode == "slow" ):
            alpha = 0.8
            beta = 0.1
            gamma = 0.1

        arr = np.array( vals, dtype = np.float )
        arr = abs( arr )
        min_val = arr.min()
        max_val = arr.max()

        delta = int( len( arr ) / ( self.nc -  1 ) )

        for ic in range( self.nc - 1 ):

            val = arr[ ( ic * delta ) : ( ( ic + 1 ) * delta ) ].max()

            #print( str( ic ) + ' ' + str( val ) )
            #factor = ( self.cz - 0.5 * ( self.nz - 1 ) ) / ( 0.5 * ( self.nz - 1 ) )
            #circ_r = self.r * math.sqrt( 1 - factor * factor )
            circ_r = self.calc_radius( self.cz )
            #new_val = circ_r + fact * ( val - min_val )
            new_val = circ_r + fact * val

            czp = min( self.cz + 1, self.nz - 1 )
            czm = max( self.cz - 1, 0 )
            icp = min( ic + 1, self.nc - 1 )
            icm = max( ic - 1 , 0 )

            self.max_untrunc = max( self.max_untrunc, new_val )
            new_val = min( new_val, 1.5 )

            new_rad = ( 1 - alpha - beta - gamma ) * new_val + \
                  alpha * self.rs[ ic, self.cz ] + \
                  beta * 0.5 * ( self.rs[ ic, czm] + self.rs[ ic, czp ] ) + \
                  gamma * 0.5 * ( self.rs[ icp, self.cz ] + self.rs[ icm, self.cz ] )
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
            self.max_untrunc = -9999
            self.cz = 0

    def get_max_radius ( self ):
        return( self.max_untrunc )

    def calc_radius( self , iz ):
        if ( iz == 0 or iz == self.nz - 1 ):
            return( 0.2 * self.calc_radius( 1 ) )
        elif ( iz <= self.cap_size ):
            factor = 1 - float( iz ) / ( self.cap_size )
            return( self.r * math.sqrt( 1 - factor * factor ) )
        elif ( self.nz - iz <= self.cap_size ):
            factor = 1 - float( self.nz - 1 - iz ) / ( self.cap_size + 1 )
            return( self.r * math.sqrt( 1 - factor * factor ) )
        else:
            return( self.r )



    # Create the mesh
    def save( self ):

        triangles = np.ndarray( ( 2 * ( self.nc - 1 ) * ( self.nz - 1 ), 3 ), dtype = np.int )
        n = 0
        for iz in range( self.nz - 1 ):
            for ic in range( self.nc - 1 ):
                triangles[ n , 0 ] = iz * self.nc + ic
                triangles[ n , 1 ] = iz * self.nc + ic + 1
                triangles[ n , 2 ] = ( iz + 1 ) * self.nc + ic
                triangles[ n + 1, 0 ] = iz * self.nc + ic + 1
                triangles[ n + 1, 1 ] = ( iz + 1 ) * self.nc + ic + 1
                triangles[ n + 1, 2 ] = ( iz + 1 ) * self.nc + ic
                n += 2

        my_mesh = mesh.Mesh(np.zeros( triangles.shape[0], dtype=mesh.Mesh.dtype ) )
        n = 0
        for iz in range( self.nz - 1 ):
            for ic in range( self.nc - 1 ):
                my_mesh.vectors[ n ][ 0 ] = self.verts[ ic, iz, : ]
                my_mesh.vectors[ n ][ 1 ] = self.verts[ ic + 1, iz, : ]
                my_mesh.vectors[ n ][ 2 ] = self.verts[ ic, iz + 1, : ]
                my_mesh.vectors[ n + 1 ][ 0 ] = self.verts[ ic + 1, iz, : ]
                my_mesh.vectors[ n + 1 ][ 1 ] = self.verts[ ic + 1, iz + 1, : ]
                my_mesh.vectors[ n + 1 ][ 2 ] = self.verts[ ic, iz + 1, : ]
                n += 2

        files = os.listdir( "./" )
        max_files = 0
        for file in files:
            if ( file.endswith( ".stl" ) and file.startswith( "mesh_" ) ):
                try:
                    num = int( file.split( "_" )[ 1 ].split( "." )[ 0 ] )
                    if ( num > max_files ):
                        max_files = num
                except:
                    pass

        my_mesh.save( "mesh_" + str( max_files + 1 ) + ".stl" )
