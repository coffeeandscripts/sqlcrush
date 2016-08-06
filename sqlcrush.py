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

    scr_bottom.border(0)

    return scr_bottom

#opens a window that is 2/3 the size of the screen horizontally and vertically
def open_option_window(scr_dim):
    
    win = curses.newwin(int((int(scr_dim[0]) * 2 / 3)), int((int(scr_dim[1]) * 2 / 3)), int((int(scr_dim[0]) / 6) - 1), int((int(scr_dim[1]) / 6) - 1))

    return win

def refresh_windows(x, scr_top, scr_front_main, scr_show_left, scr_show_main, scr_bottom):

    if x == ord("1"):
        scr_top.refresh()
        scr_front_main.refresh()
    elif x == ord("2"):
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

if len(sys.argv) == 1:
    current_database = 0
elif len(sys.argv) == 2:
    current_database = sys.argv[1]
else:
    current_database = 1

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
    #scr.clear()

    scr_top = open_top_bar(scr_dim)
    scr_front_main = open_front_main(scr_dim)
    scr_show_left = open_show_left(scr_dim)
    scr_show_main = open_show_main(scr_dim)
    scr_bottom = open_bottom_bar(scr_dim)

    if x == ord("9"):
        option_window_open = True
        win = open_option_window(scr_dim)

    if option_window_open == True:
        win.border(0)

    scr.refresh()

    if option_window_open == True:
        win.refresh()

    scr_top.addstr(0, 0, "SQLcrush v0.0.1 - coffeeandscripts")
    scr_top.addstr(0, 50, str(x))

    if current_database == 0:
        scr_top.addstr(1, 0, "No open database")
    else:
        scr_top.addstr(1, 0, str(current_database))


        
        open_database = sqlite3.connect(str(current_database))

        if last_x == ord("1"):
            all_tables = open_database.execute("SELECT name FROM sqlite_master WHERE type='table'")

            n = 1

            for table in all_tables:
                scr_front_main.addstr(n, 1, str(table)[2:-3])
                n = n + 1
        elif last_x == ord("2"):
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
                                if cursor_sub[0] + cursor_sub[1] == 1:
                                    if cursor_sub[2] == n+1 or cursor_sub[2] == 0:
                                        scr_show_main.addstr(1, 2+12*n, str(column[1])[0:9] + "...", curses.A_REVERSE)
                                    else:
                                        scr_show_main.addstr(1, 2+12*n, str(column[1])[0:9] + "...")
                                else:
                                    scr_show_main.addstr(1, 2+12*n, str(column[1])[0:9] + "...")
                            else:
                                if cursor_sub[0] + cursor_sub[1] == 1:
                                    if cursor_sub[2] == n+1 or cursor_sub[2] == 0:
                                        scr_show_main.addstr(1, 2+12*n, str(column[1]), curses.A_REVERSE)
                                    else:
                                        scr_show_main.addstr(1, 2+12*n, str(column[1]))
                                else:
                                    scr_show_main.addstr(1, 2+12*n, str(column[1]))
                            n = n + 1
                    n = 0
                    entry_list = [0]
                    for entry in current_table[shown_tables[cursor_main[0] + cursor_main[1] - 1]]:
                        m = 0
                        entry_list.append(entry[m])
                        for column in columns:
                            if 2+12*m < scr_dim[1] - 16 - 12:
                                if len(str(entry[m])) >= 12:
                                    if cursor_sub[0] + cursor_sub[1] == n + 2:
                                        if cursor_sub[2] == m+1 or cursor_sub[2] == 0:
                                            scr_show_main.addstr(n+2, 2+12*m, str(entry[m])[0:9] + "...", curses.A_REVERSE)
                                        else:
                                            scr_show_main.addstr(n+2, 2+12*m, str(entry[m])[0:9] + "...")
                                    elif cursor_sub[0] + cursor_sub[1] == 1:
                                        if cursor_sub[2] == m+1:
                                            scr_show_main.addstr(n+2, 2+12*m, str(entry[m])[0:9] + "...", curses.A_REVERSE)
                                        else:
                                            scr_show_main.addstr(n+2, 2+12*m, str(entry[m])[0:9] + "...")
                                    else:
                                        scr_show_main.addstr(n+2, 2+12*m, str(entry[m])[0:9] + "...")
                                else:
                                    if cursor_sub[0] + cursor_sub[1] == n + 2:
                                        if cursor_sub[2] == m+1 or cursor_sub[2] == 0:
                                            scr_show_main.addstr(n+2, 2+12*m, str(entry[m]), curses.A_REVERSE)
                                        else:
                                            scr_show_main.addstr(n+2, 2+12*m, str(entry[m]))
                                    elif cursor_sub[0] + cursor_sub[1] == 1:
                                        if cursor_sub[2] == m+1:
                                            scr_show_main.addstr(n+2, 2+12*m, str(entry[m]), curses.A_REVERSE)
                                        else:
                                            scr_show_main.addstr(n+2, 2+12*m, str(entry[m]))
                                    else:
                                        scr_show_main.addstr(n+2, 2+12*m, str(entry[m]))
                                m = m + 1
                        n = n + 1
                elif cursor_main[2] == 2:
                    pass
            elif open_window == 0:
                scr_show_main.addstr(2, 3, "Press ENTER to view/edit")

    if open_window == 0 and last_x == ord("2"):
        open_list = shown_tables
    elif open_window == 1 and last_x == ord("2"):
        open_list = columns
    else:
        pass

    scr_top.addstr(2, 1, str(cursor_main))
    scr_top.addstr(2, 30, str(cursor_sub))

    refresh_windows(last_x, scr_top, scr_front_main, scr_show_left, scr_show_main, scr_bottom)

    x = scr.getch()

    if x != -1 and x != 261 and x != 260 and x != 258 and x != 259 and x != 10 and x != 263:
        last_x = x

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
            else:
                cursor_sub = user_input.cursor_right(cursor_sub, columns, scr_dim)
        else:
            open_window = 1
            cursor_sub == [0, 0, 0, 0]
    elif x == 260:
        if open_window == 1:
            if cursor_sub[0] + cursor_sub[1] == 0:
                cursor_main = user_input.cursor_left(cursor_main, header_list, scr_dim)
            else:
                cursor_sub = user_input.cursor_left(cursor_sub, columns, scr_dim)
        else:
            pass
    elif x == 258:
        if open_window == 0:
            cursor_main = user_input.cursor_down(cursor_main, open_list, scr_dim)
        elif open_window == 1 and cursor_main[2] == 1:
            cursor_sub = user_input.cursor_down(cursor_sub, entry_list, scr_dim)
        else:
            cursor_sub = user_input.cursor_down(cursor_sub, open_list, scr_dim)
    elif x == 259:
        if open_window == 0:
            cursor_main = user_input.cursor_up(cursor_main, open_list, scr_dim)
        elif open_window == 1 and cursor_main[2] == 1:
            cursor_sub = user_input.cursor_up(cursor_sub, entry_list, scr_dim)
        else:
            cursor_sub = user_input.cursor_up(cursor_sub, open_list, scr_dim)

#terminating the window
term_scr(scr)
