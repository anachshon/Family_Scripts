#!/usr/bin/env python

colors = {
    "A" : 0,
    "B" : 1,
    "C" : 2,
    "D" : 3,
    "E" : 4,
    "F" : 5,
    "G" : 6,
    "H" : 7
}

colors_inv = { v : k for k, v in colors.items() }

magnets = {
    "p"  : +1,
    "n" : -1
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