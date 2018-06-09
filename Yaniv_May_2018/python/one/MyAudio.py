#!/usr/bin/env python

import pyaudio
import struct
import numpy as np

class MyAudio:

    def __init__( self ):

        self.format = pyaudio.paFloat32
        self.sample_freq = 44100
        self.frame_size = 1024
        self.nof_frames = 1

        self.nof_reads = 1

        self.buffer_size = self.frame_size * self.nof_frames
        self.super_buffer_size = self.nof_reads * self.buffer_size
        self.cur_pos = 0

        self.p = pyaudio.PyAudio()

        self.super_buffer = np.zeros( self.super_buffer_size, dtype = np.float )
#        self.stream = self.p.open( format = self.format, channels = 1, rate = self.sample_freq, input = True, frames_per_buffer = self.frame_size )

    def read( self ):

        try:
            self.stream = self.p.open(format=self.format, channels=1, rate=self.sample_freq, input=True,
                                      frames_per_buffer=self.frame_size)
            data = self.stream.read( self.buffer_size )
            self.stream.close()

            decoded = struct.unpack( str( self.buffer_size ) + 'f', data )
            for i in range( self.super_buffer_size - self.buffer_size - 1, -1, -1 ):
                self.super_buffer[ i + self.buffer_size ] = self.super_buffer[ i ]
            for i in range( self.buffer_size ):
                self.super_buffer[ i ] = decoded[ i ]
#                self.super_buffer[ self.cur_pos + i ] = decoded[ i ]
#            self.cur_pos += 64
#            if ( self.cur_pos + self.buffer_size >= self.super_buffer_size ):
#                self.cur_pos = 0
            """"
            vol = np.array( decoded ).mean()
            spectrum = np.fft.rfft( decoded )
            nof_freqs = len( spectrum )
            spec = zip( spectrum.real, range( nof_freqs ) )
            spec.sort()
            freqs = [ vol * float( x[ 1 ] ) / float( nof_freqs ) for x in spec ]
            #return( freqs )
            """
            #return( decoded )
            return( self.super_buffer )
        except:
            return( [] )

    def __del__( self ):

        self.stream.close()

