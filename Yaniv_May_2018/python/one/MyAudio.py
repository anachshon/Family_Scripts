#!/usr/bin/env python

import pyaudio
import struct
import numpy as np
import math

class MyAudio:

    def __init__( self ):

        self.format = pyaudio.paFloat32
        self.sample_freq = 44100
        self.frame_size = 1024
        self.nof_frames = 8

        self.nof_reads = 1

        self.buffer_size = self.frame_size * self.nof_frames
        self.super_buffer_size = self.nof_reads * self.buffer_size
        self.cur_pos = 0

        self.p = pyaudio.PyAudio()

        self.super_buffer = np.zeros( self.super_buffer_size, dtype = np.float )
        self.stream = self.p.open( format = self.format, channels = 1, rate = self.sample_freq, input = True, frames_per_buffer = self.frame_size )

    def read( self ):

        try:
            #self.stream = self.p.open(format=self.format, channels=1, rate=self.sample_freq, input=True,
            #                          frames_per_buffer=self.frame_size)
            data = self.stream.read( self.buffer_size )
            #self.stream.close()

            decoded = struct.unpack( str( self.buffer_size ) + 'f', data )
            #print( 'decoded ' + str( len( decoded ) ) )
            #print( min( decoded ) )
            #print( max( decoded ) )
            #print( len( decoded ) )
            """"
            if ( self.nof_reads == 1 ):
                return( decoded )
            else:
                for i in range( self.super_buffer_size - self.buffer_size - 1, -1, -1 ):
                    self.super_buffer[ i + self.buffer_size ] = self.super_buffer[ i ]
                for i in range( self.buffer_size ):
                    self.super_buffer[ i ] = decoded[ i ]
                return( self.super_buffer )
            """
            vol = max( np.array( decoded ) )
            #print( vol )
            spectrum = np.fft.rfft( decoded, norm = "ortho" )
            nof_freqs = len( spectrum )
            #print( nof_freqs )
            spec = zip( spectrum.real, range( nof_freqs ) )
            spec.sort()
            #print( spec[ : 10 ] )
            freqs = [ vol * float( x[ 1 ] ) / float( nof_freqs ) for x in spec ]
            #print( spectrum[ :16 ] )
            vals = np.array( spectrum, dtype = np.float )
            for n in range( len( vals ) ):
               log_fac = math.log10( n + 1 )
               vals[ n ] *= log_fac
            return( [ vals[ n ] for n in range( 16, 64 ) ] )

        except:
            return( [] )

    def __del__( self ):

        self.stream.close()

