#!/usr/bin/env python

import dics

#   The cube faces are 1 to 4 the vertical faces, and 5 and 6 are top and bottom
#   1 is right, 2 is back, 3 is left, 4 is front, 5 is up, 6 is down

class cube:

    def __init__( self, index, colors, magnets ):

#        self.cols = np.array( [ dics.colors[ x ] for x in colors ], dtype = np.int8 )
#        self.mags = np.array( [ dics.magnets[ x ] for x in magnets ], dtype = np.int8 )
        self.cols = [ dics.colors[ x ] for x in colors ]
        self.mags = [ dics.magnets[ x ] for x in magnets ]

        # the values of x and y will be 1 to 6
        # x and y cannot be the same value
        # also x and y cannot be of opposite faces (1,3), (2,4), (5,6)

        self.index = index
        self.x = 1
        self.y = 5

    def get_index( self ):
        return( self.index )

    def get_x( self ):
        return( self.x )

    def get_y( self ):
        return( self.y )

    def set_x( self, x ):
        self.x = x
    def set_y( self, y ):
        self.y = y

    def get_up( self ):
        y = self.y - 1
        return( ( self.cols[ y ], self.mags[ y ] ) )

    def get_right( self ):
        x = self.x - 1
        return( ( self.cols[ x ], self.mags[ x ] ) )

    def get_down( self ):
        y = dics.pairs[ self.y ] - 1
        return( ( self.cols[ y ], self.mags[ y ] ) )

    def get_left( self ):
        x = dics.pairs[ self.x ] - 1
        return( ( self.cols[ x ], self.mags[ x ] ) )

    def get_back( self ):
        vert_vals = dics.valid_vals[ self.y ]
        right_index = vert_vals.index( self.x )
        front_index = ( right_index + 1 ) if ( right_index != 3 ) else 0
        x = vert_vals[ front_index ] - 1
        return( ( self.cols[ x ], self.mags[ x ] ) )

    def get_front( self ):
        vert_vals = dics.valid_vals[ self.y ]
        right_index = vert_vals.index( self.x )
        back_index = ( right_index - 1 ) if ( right_index != 0 ) else 3
        x = vert_vals[ back_index ] - 1
        return( ( self.cols[ x ], self.mags[ x ] ) )

    def match_right( self, other ):
        mag_me = self.get_right()[ 1 ]
        mag_other = other.get_left()[ 1 ]
        return( mag_me != mag_other )

    def match_front( self, other ):
        mag_me = self.get_front()[ 1 ]
        mag_other = other.get_back()[ 1 ]
        return( mag_me != mag_other )

    def match_down( self, other ):
        mag_me = self.get_down()[ 1 ]
        mag_other = other.get_up()[ 1 ]
        return( mag_me != mag_other )

    def has_color( self, color ):
        if ( color in self.cols ):
            return( self.cols.index( color ) + 1 )
        else:
            return( 0 )
