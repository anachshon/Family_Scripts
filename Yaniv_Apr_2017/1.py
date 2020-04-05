#!/usr/bin/env python

import os, sys, shutil
import numpy as np
import math
import matplotlib.pyplot as plt

def solve( x1, y1, x2, y2, l1, l2 ):

    cx1 = - 2 * x1
    cy1 = - 2 * y1
    rhs1 = l1 * l1 - x1 * x1 - y1 * y1

    cx2 = - 2 * x2
    cy2 = - 2 * y2
    rhs2 = l2 * l2 - x2 * x2 - y2 * y2

    clx = 2 * ( x1 - x2 )
    cly = 2 * ( y1 - y2 )
    rhsl = rhs2 - rhs1

    #   We will assume that clx is always <> 0

    cxy = - cly / clx
    cxf = rhsl / clx

    a = 1 + cxy * cxy
    b = cy1 + 2 * cxy * cxf + cx1 * cxy
    c = -( rhs1 - cxf * cxf - cx1 * cxf )

    det = math.sqrt( b * b - 4 * a * c )
    y31 = ( -b + det ) / ( 2 * a )
    y32 = ( -b + det ) / ( 2 * a )

    y = max( y31, y32 )
    x = cxy * y + cxf

    return( [ x, y ] )

cx1 = -6.25
cy1 = 0
r1 = 2.5
cx2 = 6.25
cy2 = 0
r2 = 2.5

ll1 = 9
ll2 = 4
lr1 = 9
lr2 = 4

sl = 5
sr = 5

t1 = 0
t2 = 0

w1 = -0.001 * 599
w2 = 0.001 * 991
#w1 = 0.001 * 593
#w2 = 0.001 * 599

tick = 0.01

steps = 10000000
strike = 100

llf = float( ll1 + ll2 ) / float( ll1 )
lrf = float( lr1 + lr2 ) / float( lr1 )

plt.axis( [ -7, 7, 5, 19 ] )
plt.ion()

first_time = True
counter = 1
while ( steps > 0 ):

    x1 = cx1 + r1 * math.cos( t1 )
    y1 = cy1 + r1 * math.sin( t1 )
    x2 = cx2 + r2 * math.cos( t2 )
    y2 = cy2 + r2 * math.sin( t2 )

    x3, y3 = solve( x1, y1, x2, y2, ll1, lr1 )

    x4 = x2 + llf * ( x3 - x2 )
    y4 = y2 + llf * ( y3 - y2 )
    x5 = x1 + lrf * ( x3 - x1 )
    y5 = y1 + lrf * ( y3 - y1 )

    x6, y6 = solve( x4, y4, x5, y5, sl, sr )

    if ( first_time ):
        first_time = False
    else:
        plt.plot( [ xp, x6 ], [ yp, y6 ], color = 'blue' )
    xp = x6
    yp = y6

    if ( steps % strike == 0 ):
        #plt.scatter( x6, y6, color = 'red' )
        plt.pause( 0.00001 )


    t1 += tick * w1
    t2 += tick * w2
    steps -= 1

while ( True ):
    plt.pause( 0.00001 )

