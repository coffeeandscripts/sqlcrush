#!/usr/bin/env python

"""
Set of functions to correspond to user input
"""

## IMPORTS ##
import curses
import curses.textpad as textpad

## FUNCTIONS ##

def cursor_right(cursor, hoz_list, scr_dim):

    max_list_length = len(hoz_list)

    if cursor[2] < max_list_length - 1:
        cursor[2] = cursor[2] + 1

    return cursor

def cursor_left(cursor, hoz_list, scr_dim):
    
    if cursor[2] > 0:
        cursor[2] = cursor[2] - 1

    return cursor

def cursor_down(cursor, vert_list, scr_dim):

    max_list_length = len(vert_list)

    if cursor[0] < scr_dim[0] - 7 and cursor[0] + cursor[1] < max_list_length:
        cursor[0] = cursor[0] + 1
    elif cursor[0] == scr_dim[0] - 7 and cursor[0] + cursor[1] < max_list_length:
        cursor[1] = cursor[1] + 1

    return cursor

def cursor_up(cursor, vert_list, scr_dim):

    if cursor[0] > 0:
        cursor[0] = cursor[0] - 1
    elif cursor[0] == 0 and cursor[1] > 0:
        cursor[1] = cursor[1] - 1

    return cursor

def input_n():

    return 0
