#!/usr/bin/env python

import os, sys, shutil
import json
import datetime

inp_file_name = sys.argv[ 1 ]
out_file_name = sys.argv[ 2 ]

#
#   "users": {
#     "0504207377": {
#       "1518180354044": {
#         "notificationId": "1",
#         "notificationReceivedTime": 1518180350558,
#         "notificationRespondTime": 1518180354044,
#         "notificationWatchedTime": 1518180350577,
#         "userAction": "ACCEPT NOTIFICATION"
#       }
#     },
#     "0505999113": {
#       "1519286952836": {
#         "notificationId": "2",
#         "notificationReceivedTime": 1519286868898,
#         "notificationRespondTime": 1519286952836,
#         "notificationWatchedTime": 1519286942838,
#         "userAction": "ACCEPT NOTIFICATION",
#         "userId": "0505999113"
#       },
#

akeys = {
            'noteID'  :     ( 'notificationId', 'asis' ),
            'resTimeH' :     ( 'notificationRespondTime', 'conv' ),
            'recTimeH' :     ( 'notificationReceivedTime', 'conv' ),
            'watTimeH' :     ( 'notificationWatchedTime', 'conv' ),
            'resTime' :     ( 'notificationRespondTime', 'asis' ),
            'recTime' :     ( 'notificationReceivedTime', 'asis' ),
            'watTime' :     ( 'notificationWatchedTime', 'asis' ),
            'act'     :     ( 'userAction', 'asis' ),
            'userId'  :     ( 'userId', 'asis' )
        }

inp_file = open( inp_file_name, "r" )
data = json.load( inp_file )
inp_file.close()

out_file = open( out_file_name, 'w' )
out_file.write( ','.join( [ 'phone', 'action' ] + akeys.keys() ) + '\n' )
users = data[ 'users' ]
for user_id in users.keys():
    actions = users[ user_id ]
    for action in actions.keys():
        out_line = user_id + ',' + action
        entry = actions[ action ]
        for key in akeys.keys():
            key_str = akeys[ key ][ 0 ]
            val = ''
            if ( key_str in entry.keys() ):
                if ( akeys[ key ][ 1 ] == "asis" ):
                    val = str( entry[ key_str ] )
                elif ( akeys[ key ][ 1 ] == "conv" ):
                    time = datetime.datetime.fromtimestamp( float( entry[ key_str ] ) / 1e3 )
                    val = time.strftime( "%a %d %b %Y %H:%M:%S")
            out_line += ',' + val
        out_file.write( out_line + '\n' )

out_file.close()