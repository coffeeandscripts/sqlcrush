#!/usr/bin/env python

## IMPORTS ##
import curses
import time
import sys
import os
import sqlite3
import user_input
import database

## GLOBALS ##
x = 1
last_x = 0
term_size_change = False
option_window_open = False

## FUNCTIONS ##
#initialize the curses window and return scr
def init_scr():
    
    scr = curses.initscr()

    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.halfdelay(5)
    scr.keypad(True)
    scr.clear()    

    return scr

#user scr to terminate the window and revert back to terminal
def term_scr(scr):

    curses.nocbreak()
    scr.keypad(False)
    curses.echo()
    curses.endwin()

#returns the number of columns or rows
def get_scr_dim(scr):
    return scr.getmaxyx()

#returns True if there has been a change in the window size, otherwise False
def check_term_size_change(scr, scr_dim):
    
    change = False

    if scr_dim != scr.getmaxyx():
        change = True

    return change

def open_top_bar(scr_dim):

    scr_top = curses.newwin(4, scr_dim[1], 0, 0)

    return scr_top

def open_front_main(scr_dim):

    scr_front_main = curses.newwin(scr_dim[0]-4, scr_dim[1], 4, 0)

    scr_front_main.addstr(2, 2, "HELP:")
    scr_front_main.addstr(3, 2, "Make sure to open the database from the command line")

    scr_front_main.border(0)

    return scr_front_main

def open_show_left(scr_dim):

    scr_show_left = curses.newwin(scr_dim[0]-4-3, 16, 4, 0)

    scr_show_left.border(0)

    return scr_show_left

def open_show_main(scr_dim):

    scr_show_main = curses.newwin(scr_dim[0]-4-3, scr_dim[1]-16, 4, 16)

    scr_show_main.border(0)

    return scr_show_main

def open_bottom_bar(scr_dim):

    scr_bottom = curses.newwin(3, scr_dim[1], scr_dim[0]-3, 0)

    return scr_bottom

def refresh_windows(current_screen, scr_top, scr_front_main, scr_show_left, scr_show_main, scr_bottom):

    if current_screen == 1:
        scr_top.refresh()
        scr_front_main.refresh()
    elif current_screen == 2:
        scr_top.refresh()
        scr_show_left.refresh()
        scr_show_main.refresh()
        scr_bottom.refresh()
    else:
        scr_top.refresh()

## WORKFLOW ##
print("SQLcrush")

time.sleep(1)
print()
print("Initializing...")
time.sleep(2)

scr = init_scr()
scr_dim = get_scr_dim(scr)

cursor_main = [0, 0, 0, 0]
cursor_sub = [0, 0, 0, 0]
open_window = 0

header_list = ["Struct", "Browse", "Execute"]

help_screen = 0

if len(sys.argv) == 1:
    current_database = 0
    current_screen = 1
elif len(sys.argv) == 2:
    current_database = sys.argv[1]
    current_screen = 2
else:
    current_database = 1
    current_screen = 1

#main loop
while x != ord("0"):

    term_size_change = check_term_size_change(scr, scr_dim)

    if term_size_change == True:
        term_scr(scr)
        scr = init_scr()
        scr_dim = get_scr_dim(scr)
        win = open_option_window(scr_dim)
        term_size_change == False

    scr_dim = get_scr_dim(scr)

    scr_top = open_top_bar(scr_dim)
    scr_front_main = open_front_main(scr_dim)
    scr_show_left = open_show_left(scr_dim)
    scr_show_main = open_show_main(scr_dim)
    scr_bottom = open_bottom_bar(scr_dim)

    scr.refresh()

    scr_top.addstr(0, 0, "SQLcrush v0.0.1 - coffeeandscripts")
    scr_top.addstr(0, 50, str(x))

    if current_database == 0:
        scr_top.addstr(1, 0, "No open database")
    else:
        scr_top.addstr(1, 0, str(current_database))
        
        open_database = sqlite3.connect(str(current_database))

        if current_database == 0 or help_screen == 1:
            all_tables = open_database.execute("SELECT name FROM sqlite_master WHERE type='table'")

            n = 1

            for table in all_tables:
                scr_front_main.addstr(n, 1, str(table)[2:-3])
                n = n + 1
        elif current_database != 0:
            if x == 9:
                if open_window == 0:
                    open_window = 1
                else:
                    open_window = 0
            scr_show_left.addstr(0, 2, str(current_database)[0:12], curses.A_REVERSE)
            n = 0
            for header in header_list:
                if open_window == 1:
                    if cursor_main[2] == n:
                        scr_show_main.addstr(0, 2+n*8, str(header), curses.A_REVERSE)
                    else:
                        scr_show_main.addstr(0, 2+n*8, str(header))
                else:
                    scr_show_main.addstr(0, 2+n*8, str(header))
                n = n + 1
            all_tables = open_database.execute("SELECT name FROM sqlite_master WHERE type='table'")
            n = 2
            shown_tables = []
            for table in all_tables:
                shown_tables.append(str(table)[2:-3])
                if len(str(table)) > 16:
                    if cursor_main[0] + cursor_main[1] == n - 1:
                        scr_show_left.addstr(n, 1, str(table)[2:13] + "...", curses.A_REVERSE)
                    else:
                        scr_show_left.addstr(n, 1, str(table)[2:13] + "...")
                else:
                    if cursor_main[0] + cursor_main[1] == n - 1:
                        scr_show_left.addstr(n, 1, str(table)[2:-3], curses.A_REVERSE)
                    else:
                        scr_show_left.addstr(n, 1, str(table)[2:-3])
                n = n + 1

            if open_window == 1:
                open_table = shown_tables[cursor_main[0] + cursor_main[1] - 1]
                
                columns = open_database.execute('PRAGMA TABLE_INFO({})'.format(shown_tables[cursor_main[0] + cursor_main[1] - 1])).fetchall()

                if cursor_main[2] == 0:
                    scr_show_main.addstr(1, 2, "ID:")
                    scr_show_main.addstr(1, 6, "Name:")
                    scr_show_main.addstr(1, 30, "Type:")
                    n = 0

                    for column in columns:
                        if cursor_sub[0] + cursor_sub[1] == n + 1: 
                            scr_show_main.addstr(2+n, 3, str(column[0]), curses.A_REVERSE)
                            scr_show_main.addstr(2+n, 6, str(column[1]), curses.A_REVERSE)
                            scr_show_main.addstr(2+n, 30, str(column[2]), curses.A_REVERSE)
                        else:
                            scr_show_main.addstr(2+n, 3, str(column[0]))
                            scr_show_main.addstr(2+n, 6, str(column[1]))
                            scr_show_main.addstr(2+n, 30, str(column[2]))
                        n = n + 1
                elif cursor_main[2] == 1:
                    
                    current_table = database.get_table(shown_tables[cursor_main[0] + cursor_main[1] - 1], open_database)
                    n = 0
                    for column in columns:
                        if 2+12*n < scr_dim[1] - 16 - 12:
                            if len(str(column[1])) >= 12:
                                short_printing = str(column[1])[0:9] + ".."
                                if cursor_sub[0] + cursor_sub[1] == 1:
                                    if cursor_sub[2] == n+1 or cursor_sub[2] == 0:
                                        scr_show_main.addstr(1, 2+12*n, short_printing, curses.A_REVERSE)
                                    else:
                                        scr_show_main.addstr(1, 2+12*n, short_printing)
                                else:
                                    scr_show_main.addstr(1, 2+12*n, short_printing)
                            else:
                                full_printing = str(column[1])
                                while len(full_printing) < 11:
                                    full_printing = " " + full_printing
                                if cursor_sub[0] + cursor_sub[1] == 1:
                                    if cursor_sub[2] == n+1 or cursor_sub[2] == 0:
                                        scr_show_main.addstr(1, 2+12*n, full_printing, curses.A_REVERSE)
                                    else:
                                        scr_show_main.addstr(1, 2+12*n, full_printing)
                                else:
                                    scr_show_main.addstr(1, 2+12*n, full_printing)
                            n = n + 1
                    n = 0
                    entry_list = [0]
                    for entry in current_table[shown_tables[cursor_main[0] + cursor_main[1] - 1]]:
                        m = 0
                        entry_list.append(entry[m])
                        for column in columns:
                            if 2+12*m < scr_dim[1] - 16 - 12:
                                if len(str(entry[m])) >= 12:
                                    short_printing = str(entry[m])[0:9].replace('\n', ' ') + ".."
                                    full_printing = str(entry[m]).replace('\n', ' ')
                                    if cursor_sub[0] + cursor_sub[1] == n + 2:
                                        if cursor_sub[2] == m+1 or cursor_sub[2] == 0:
                                            scr_show_main.addstr(n+2, 2+12*m, short_printing, curses.A_REVERSE)
                                            if cursor_sub[2] != 0:
                                                if len(full_printing) > scr_dim[1] - 10:
                                                    scr_bottom.addstr(0, 1, full_printing[0:scr_dim[1]-2] + "...")
                                                else:
                                                    scr_bottom.addstr(0, 1, full_printing)
                                        else:
                                            scr_show_main.addstr(n+2, 2+12*m, short_printing)
                                    elif cursor_sub[0] + cursor_sub[1] == 1:
                                        if cursor_sub[2] == m+1:
                                            scr_show_main.addstr(n+2, 2+12*m, short_printing, curses.A_REVERSE)
                                        else:
                                            scr_show_main.addstr(n+2, 2+12*m, short_printing)
                                    else:
                                        scr_show_main.addstr(n+2, 2+12*m, str(short_printing))
                                else:
                                    full_printing = str(entry[m]).replace('\n', ' ')
                                    while len(full_printing) < 11:
                                        full_printing = " " + full_printing
                                    if cursor_sub[0] + cursor_sub[1] == n + 2:
                                        if cursor_sub[2] == m+1 or cursor_sub[2] == 0:
                                            scr_show_main.addstr(n+2, 2+12*m, full_printing, curses.A_REVERSE)
                                            if cursor_sub[2] != 0:
                                                scr_bottom.addstr(0, 1, str(entry[m]).replace('\n', ' '))
                                        else:
                                            scr_show_main.addstr(n+2, 2+12*m, full_printing)
                                    elif cursor_sub[0] + cursor_sub[1] == 1:
                                        if cursor_sub[2] == m+1:
                                            scr_show_main.addstr(n+2, 2+12*m, full_printing, curses.A_REVERSE)
                                        else:
                                            scr_show_main.addstr(n+2, 2+12*m, full_printing)
                                    else:
                                        scr_show_main.addstr(n+2, 2+12*m, full_printing)
                                m = m + 1
                        n = n + 1
                    columns.append("Blank")
                elif cursor_main[2] == 2:
                    pass
            elif open_window == 0:
                scr_show_main.addstr(2, 3, "Press ENTER to view/edit")

    if open_window == 0 and current_screen == 2:
        open_list = shown_tables
    elif open_window == 1 and current_screen == 2:
        open_list = columns
    else:
        pass

    scr_top.addstr(2, 1, str(cursor_main))
    scr_top.addstr(2, 30, str(cursor_sub))

    scr_bottom.addstr(2, 2, "[h] Help [Arrows] Move [0] Exit", curses.A_REVERSE)

    refresh_windows(current_screen, scr_top, scr_front_main, scr_show_left, scr_show_main, scr_bottom)

    x = scr.getch()

    #if x != -1 and x != 261 and x != 260 and x != 258 and x != 259 and x != 10 and x != 263:
    #    last_x = x

    if x == 10:
        if open_window == 0:
            open_window = 1
            cursor_sub = [0, 0, 0, 0]
    if x == 263:
        if open_window == 1:
            open_window = 0
    if x == 261:
        if open_window == 1:
            if cursor_sub[0] + cursor_sub[1] == 0:
                cursor_main = user_input.cursor_right(cursor_main, header_list, scr_dim)
                cursor_sub = [0, 0, 0, 0]
            else:
                cursor_sub = user_input.cursor_right(cursor_sub, columns, scr_dim)
        else:
            open_window = 1
            cursor_sub == [0, 0, 0, 0]
    elif x == 260:
        if open_window == 1:
            if cursor_sub[0] + cursor_sub[1] == 0:
                cursor_main = user_input.cursor_left(cursor_main, header_list, scr_dim)
                cursor_sub = [0, 0, 0, 0]
            else:
                cursor_sub = user_input.cursor_left(cursor_sub, columns, scr_dim)
        else:
            pass
    elif x == 258:
        if open_window == 0:
            cursor_main = user_input.cursor_down(cursor_main, open_list, scr_dim)
            cursor_sub = [0, 0, 0, 0]
        elif open_window == 1 and cursor_main[2] == 1:
            cursor_sub = user_input.cursor_down(cursor_sub, entry_list, scr_dim)
        else:
            cursor_sub = user_input.cursor_down(cursor_sub, open_list, scr_dim)
    elif x == 259:
        if open_window == 0:
            cursor_main = user_input.cursor_up(cursor_main, open_list, scr_dim)
            cursor_sub = [0, 0, 0, 0]
        elif open_window == 1 and cursor_main[2] == 1:
            cursor_sub = user_input.cursor_up(cursor_sub, entry_list, scr_dim)
        else:
            cursor_sub = user_input.cursor_up(cursor_sub, open_list, scr_dim)
    elif x == 104:      # h
        if current_screen == 1:
            current_screen = 2
        elif current_screen == 2:
            current_screen = 1
    """
    elif x == 111:
        new_database = user_input.open_new_database(scr_top, scr_dim)
        if current_database != 0:
            open_database.close()
        current_database = new_database
        scr.clear()
    """

#terminating the window
term_scr(scr)
