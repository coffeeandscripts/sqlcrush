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

    if cursor[2] + cursor[3] < max_list_length - 1:
        cursor[2] = cursor[2] + 1

    if cursor[2]*12+2 > scr_dim[1] - 16:
        cursor[2] = cursor[2] - 1
        cursor[3] = cursor[3] + 1

    return cursor

def cursor_left(cursor, hoz_list, scr_dim):
    
    if cursor[2] > 0:
        cursor[2] = cursor[2] - 1

    if cursor[2] == 0 and cursor[3] != 0:
        cursor[2] = 1
        cursor[3] = cursor[3] - 1

    return cursor

def cursor_down(cursor, vert_list, scr_dim, cursor_other):

    max_list_length = len(vert_list)

    if cursor[0] + cursor[1] < max_list_length:
        cursor[0] = cursor[0] + 1
    
    if cursor_other[2] == 1:
        if cursor[0] > scr_dim[0] - 9:
            cursor[0] = cursor[0] - 1
            cursor[1] = cursor[1] + 1
    else:
        if cursor[0] > scr_dim[0] - 10:
            cursor[0] = cursor[0] - 1
            cursor[1] = cursor[1] + 1

    return cursor

def cursor_up(cursor, vert_list, scr_dim, cursor_other):

    if cursor[0] > 0:
        cursor[0] = cursor[0] - 1
    if cursor_other[2] == 1:
        if cursor[0] == 1 and cursor[1] != 1 and cursor[1] != 0:
            cursor[0] = 2
            cursor[1] = cursor[1] - 1
        if cursor[0] == 1 and cursor[1] == 1:
            cursor[1] = 0
    else:
        if cursor[0] == 0 and cursor[1] != 0:
            cursor[0] = 1
            cursor[1] = cursor[1] - 1

    return cursor

def update_cell(scr_dim, original):

    #curses.start_color()
    #curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    new_entry_window = curses.newwin(1, scr_dim[1]-2, scr_dim[0] - 3, 1)
    #new_entry_window.bkgd(curses.color_pair(1))
    new_entry_box = textpad.Textbox(new_entry_window)
    new_entry_window.addstr(0, 0, str(original), curses.A_REVERSE)
    new_entry_window.refresh()
    new_entry = new_entry_box.edit()

    return new_entry

def open_new_database(scr_top, scr_dim):

    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    new_database_window = curses.newwin(1, scr_dim[1], 1, 0)
    new_database_window.bkgd(curses.color_pair(1))
    new_database_box = textpad.Textbox(new_database_window)
    new_database_window.refresh()
    scr_top.addstr(2, 1, "Open new database. Leave blank and hit enter to close")
    new_database = new_database_box.edit()

    return new_database
