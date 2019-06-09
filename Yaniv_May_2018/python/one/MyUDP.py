import socket
import sys

class MyUDP:

    def __init__( self ):

        self.sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        udp_host = "127.0.0.1"
        udp_port = 10000
        self.sock.bind( ( udp_host, udp_port ) )
        self.sock.settimeout( 0.001 )

    def handle_messages( self ):

        data = ''
        try:
		    data, addr = self.sock.recvfrom( 64 )
        finally:
		    return( data )

