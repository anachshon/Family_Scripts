#!/usr/bin/env python

import pyaudio
import struct

class MyAudio:

    def __init__( self ):

        self.format = pyaudio.paFloat32
        self.sample_freq = 44100
        self.frame_size = 1024
        self.nof_frames = 1

        self.buffer_size = self.frame_size * self.nof_frames

        self.p = pyaudio.PyAudio()
#        self.stream = self.p.open( format = self.format, channels = 1, rate = self.sample_freq, input = True, frames_per_buffer = self.frame_size )

    def read( self ):

        try:
            self.stream = self.p.open(format=self.format, channels=1, rate=self.sample_freq, input=True,
                                      frames_per_buffer=self.frame_size)
            data = self.stream.read( self.buffer_size )
            decoded = struct.unpack( str( self.buffer_size ) + 'f', data )
            self.stream.close()
#            print( "read success")
        except:
            decoded = []
#            print( "read failure")
        return( decoded )

    def __del__( self ):

        self.stream.close()
