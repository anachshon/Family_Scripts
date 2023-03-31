#!/usr/bin/env python

class f:
    right   = 0
    back    = 1
    left    = 2
    front   = 3
    up      = 4
    down    = 5

    nof     = 6

f_inv = {
            "Right"   : 0,
            "Back"    : 1,
            "left"    : 2,
            "Front"   : 3,
            "Top"     : 4,
            "Down"    : 5
        }

#
#   color   Freq
#   Black   21
#   Blue    27
#   Green   27
#   Orange  20
#   Purple  27
#   Red     27
#   White   28
#   Yellow  27
#

colors = {
    "White"     : 0,
    "Black"     : 1,
    "Red"       : 2,
    "Green"     : 3,
    "Blue"      : 4,
    "Yellow"    : 5,
    "Purple"    : 6,
    "Orange"    : 7,
    "N"         : -1
}

colors_inv = { v : k for k, v in colors.items() }

magnets = {
    "+"  : +1,
    "-" : -1
}

magnets_rev = { v : k for k, v in magnets.items() }

valid_vals = {
    1 : [ 2, 5, 4, 6 ],
    2 : [ 1, 6, 3, 5 ],
    3 : [ 2, 6, 4, 5 ],
    4 : [ 1, 5, 3, 6 ],
    5 : [ 1, 2, 3, 4 ],
    6 : [ 1, 4, 3, 2 ]
}

pairs = {
    1 : 3,
    2 : 4,
    3 : 1,
    4 : 2,
    5 : 6,
    6 : 5
}