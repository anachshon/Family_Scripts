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
#   ACCEPT NOTIFICATION             first
#   DECLINE NOTIFICATION            first
#   HOLD NOTIFICATION               first
#   Instructions 1 Accepted         second
#   Instructions 1 Decline          second
#   Instructions 2 Accepted         third
#   Instructions 2 Decline          third
#

akeys = {
            'noteID'  :     'notificationId',
            'resTime' :     'notificationRespondTime',
            'recTime' :     'notificationReceivedTime',
            'watTime' :     'notificationWatchedTime',
            'act'     :     'userAction',
            'userId'  :     'userId'
        }
def conv_time( mili_sec ):
    time = datetime.datetime.fromtimestamp(float(mili_sec ) / 1e3)
    val = time.strftime("%a %d %b %Y %H:%M:%S")
    return( val )

inp_file = open( inp_file_name, "r" )
data = json.load( inp_file )
inp_file.close()

actions_list = []
users = data[ 'users' ]
for user_id in users.keys():
    actions = users[ user_id ]
    for action in actions.keys():
        entry = actions[ action ]
        action_string = entry[ akeys[ 'act' ] ]
        if ( 'HOLD' in action_string ):
            action_type = 0
        elif ('NOT' in action_string):
            action_type = 1
        elif ( ' 1 ' in action_string ):
            action_type = 2
        elif (' 2 ' in action_string):
            action_type = 3

        actions_list.append( ( ( user_id, action, conv_time( action ), action_type, action_string ), entry ) )

actions_list.sort()

out_file = open( out_file_name, 'w' )
out_file.write( 'phone number\taction time\taction time H\taction type\taction string\tdiff time\n' )
prev_time = -1
for entry in actions_list:
    out_list = [ str( e ) for e in entry[ 0 ] ]
    curr_time = float( entry[0][1] )
    if ( prev_time > 0 ):
        diff_time = 0.001 * ( curr_time - prev_time )
        prev_time = curr_time
        out_list.append( str( diff_time ) )
    else:
        prev_time = curr_time
    out_file.write( '\t'.join( out_list ) + '\n' )
out_file.close()

sessions_list = []
session = []
prev_phone = -1
prev_type = -1

for entry in actions_list:
    curr_phone = entry[ 0 ][ 0 ]
    curr_time = float( entry[ 0 ][ 1 ] )
    curr_type = entry[ 0 ][ 3 ]

    if ( prev_phone == -1 ):
        session = [ entry ]
        prev_phone = curr_phone
        prev_time = curr_time
        prev_type = curr_type
    if ( curr_phone <> prev_phone ):
        if ( session == [] ):
            print( "This looks like an error. A session failed to start or was closed too early ? " )
        else:
            sessions_list.append( session )
            session = [ entry ]
            prev_phone = curr_phone
            prev_time = curr_time
            prev_type = curr_type
    else:
        if ( curr_type == 0 ):
            sessions_list.append( session )
            session = [ entry ]
            prev_time = curr_time
            prev_type = curr_type
        elif ( curr_type == 1 ):
            if ( prev_type == 0 and ( curr_time - prev_time ) < 1000 * 60 * 10 ):
                session.append( entry )
                prev_time = curr_time
                prev_type = curr_type
            else:
                sessions_list.append(session)
                session = [ entry]
                prev_time = curr_time
                prev_type = curr_type
        elif ( curr_type == 2 or curr_type == 3 ):
            session.append(entry)
            prev_time = curr_time
            prev_type = curr_type

sessions_list.append( session )

def serialize_event( entry ):
    list = [ entry[ 0 ][ 0 ] ]
    list.append( entry[ 0 ][ 4 ] )
    list.append( entry[ 0 ][ 1 ] )
    list.append( entry[ 0 ][ 2 ] )

    list.append( str( entry[ 1 ][ akeys[ 'recTime' ] ] ) )
    list.append( conv_time( entry[ 1 ][ akeys[ 'recTime' ] ] ) )
    list.append( str( entry[ 1 ][ akeys[ 'resTime' ] ] ) )
    list.append( conv_time( entry[ 1 ][ akeys[ 'resTime' ] ] ) )
    list.append( str( entry[ 1 ][ akeys[ 'watTime' ] ] ) )
    list.append( conv_time( entry[ 1 ][ akeys[ 'watTime' ] ] ) )

    return( list )

header = [ 'duration' ] + 3 * [ 'phone', 'action', 'action time', 'action time H', 'recieve time', 'recieve time H', 'response time', 'response time H', 'watch time', 'watch time H']

out_file = open( out_file_name, 'w' )
out_file.write( ','.join( header ) + '\n' )
for session in sessions_list:
    list = []
    for entry in session:
        list += serialize_event( entry )
    duration = ( float( session[ -1 ][ 0 ][ 1 ] ) - float( session[ 0 ][ 0 ][ 1 ] ) ) / 1000
    list = [ str( duration ) ] + list
    out_file.write( ','.join( list ) + '\n' )

out_file.close()

"""
out_file.write( ','.join( [ 'phone', 'action' ] + akeys.keys() ) + '\n' )

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

"""