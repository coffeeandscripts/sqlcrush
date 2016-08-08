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
database.print_intro()

scr = init_scr()
scr_dim = get_scr_dim(scr)

cursor_main = [0, 0, 0, 0]
cursor_sub = [0, 0, 0, 0]
open_window = 0

header_list = ["Struct", "Browse", "Execute"]

help_screen = 0
find_list = []

table_executions = {}

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
        term_size_change == False

    scr_dim = get_scr_dim(scr)

    scr_top = open_top_bar(scr_dim)
    scr_front_main = open_front_main(scr_dim)
    scr_show_left = open_show_left(scr_dim)
    scr_show_main = open_show_main(scr_dim)
    scr_bottom = open_bottom_bar(scr_dim)

    scr.refresh()

    scr_top.addstr(0, 0, "SQLcrush v0.0.1 - by coffeeandscripts")
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
            p = 0
            shown_tables = []
            for table in all_tables:
                shown_tables.append(str(table)[2:-3])
                if str(table)[2:-3] not in table_executions:
                    table_executions[str(table)[2:-3]] = []
                if n - 2 >= scr_dim[0] - 10:
                    continue
                if cursor_main[1] >= p + 1:
                    p = p + 1
                    continue
                if len(str(table)) > 16:
                    if cursor_main[0] + cursor_main[1] == p + 1:
                        scr_show_left.addstr(n, 1, str(table)[2:13] + "...", curses.A_REVERSE)
                    else:
                        scr_show_left.addstr(n, 1, str(table)[2:13] + "...")
                else:
                    if cursor_main[0] + cursor_main[1] == p + 1:
                        scr_show_left.addstr(n, 1, str(table)[2:-3], curses.A_REVERSE)
                    else:
                        scr_show_left.addstr(n, 1, str(table)[2:-3])
                n = n + 1
                p = p + 1

            if open_window == 1:
                open_table = shown_tables[cursor_main[0] + cursor_main[1] - 1]
                
                columns = open_database.execute('PRAGMA TABLE_INFO({})'.format(shown_tables[cursor_main[0] + cursor_main[1] - 1])).fetchall()

                if cursor_main[2] == 0:
                    scr_show_main.addstr(1, 2, "ID:")
                    scr_show_main.addstr(1, 6, "Name:")
                    scr_show_main.addstr(1, 30, "Type:")
                    n = 0
                    p = 0
                    for column in columns:
                        if n >= scr_dim[0] - 10:
                            continue
                        if cursor_sub[1] >= p + 1:
                            p = p + 1
                            continue
                        id_print = str(column[0]) + " "
                        name_print = " " + str(column[1])
                        type_print = " " + str(column[2])
                        while len(id_print) < 4:
                            id_print = " " + id_print
                        while len(name_print) < 24:
                            name_print = name_print + " "
                        while len(type_print) < 12:
                            type_print = type_print + " "
                        if cursor_sub[0] + cursor_sub[1] == p + 1: 
                            scr_show_main.addstr(2+n, 3, id_print, curses.A_REVERSE)
                            scr_show_main.addstr(2+n, 6, name_print, curses.A_REVERSE)
                            scr_show_main.addstr(2+n, 30, type_print, curses.A_REVERSE)
                        else:
                            scr_show_main.addstr(2+n, 3, id_print)
                            scr_show_main.addstr(2+n, 6, name_print)
                            scr_show_main.addstr(2+n, 30, type_print)
                        n = n + 1
                        p = p + 1
                elif cursor_main[2] == 1:
                    
                    current_table = database.get_table(shown_tables[cursor_main[0] + cursor_main[1] - 1], open_database)
                    n = 0
                    m = 0
                    for column in columns:
                        if cursor_sub[3] >= m + 1:
                            m = m + 1
                            continue
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
                    p = 0
                    find_counter = 0
                    entry_list = [0]
                    for entry in current_table[shown_tables[cursor_main[0] + cursor_main[1] - 1]]:
                        m = 0
                        q = 0
                        entry_list.append(entry[m])
                        if find_list != []:
                            if int(p) not in find_list:
                                p = p + 1
                                continue
                            else:
                                find_counter = find_counter + 1
                        if n >= scr_dim[0] - 10:
                            continue
                        if cursor_sub[1] >= p + 1:
                            p = p + 1
                            continue
                        for column in columns:
                            if cursor_sub[3] >= q + 1:
                                q = q + 1
                                continue
                            if 2+12*m < scr_dim[1] - 16 - 12:
                                if len(str(entry[q])) >= 12:
                                    short_printing = str(entry[q])[0:9].replace('\n', ' ') + ".."
                                    full_printing = str(entry[q]).replace('\n', ' ')
                                    if (cursor_sub[0] + cursor_sub[1] == p + 2 and find_counter == 0) or cursor_sub[0] + cursor_sub[1] == find_counter + 1:
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
                                    full_printing = str(entry[q]).replace('\n', ' ')
                                    while len(full_printing) < 11:
                                        full_printing = " " + full_printing
                                    if (cursor_sub[0] + cursor_sub[1] == p + 2 and find_counter == 0) or cursor_sub[0] + cursor_sub[1] == find_counter + 1:
                                        if cursor_sub[2] == m+1 or cursor_sub[2] == 0:
                                            scr_show_main.addstr(n+2, 2+12*m, full_printing, curses.A_REVERSE)
                                            if cursor_sub[2] != 0:
                                                scr_bottom.addstr(0, 1, str(entry[q]).replace('\n', ' '))
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
                                q = q + 1
                        n = n + 1
                        p = p + 1
                    columns.append("Blank")
                elif cursor_main[2] == 2:
                    executions_list = table_executions[str(shown_tables[cursor_main[0] + cursor_main[1] - 1])]
                    n = 0
                    p = 0
                    for execution in reversed(executions_list):
                        if n >= scr_dim[0] - 10:
                            continue
                        if cursor_sub[1] >= p + 1:
                            p = p + 1
                            continue
                        if cursor_sub[0] + cursor_sub[1] == p + 1:
                            scr_show_main.addstr(n+2, 1, str(execution), curses.A_REVERSE)
                        else:
                            scr_show_main.addstr(n+2, 1, str(execution))
                        n = n + 1
                        p = p + 1
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
    if scr_dim[1] > 90:
        scr_bottom.addstr(2, 2, "[h] Help [Arrows] Move [delete] Back [f] Find [n] New [u] Update [d] Delete [Esc/0] Exit", curses.A_REVERSE)
    elif scr_dim[1] > 40:
        scr_bottom.addstr(2, 2, "[h] Help [Arrows] Move [Esc/0] Exit", curses.A_REVERSE)
    else:
        scr_bottom.addstr(2, 2, "[h] Help [Esc/0] Exit", curses.A_REVERSE)

    scr_bottom.addstr(1, 1, str(find_list))

    refresh_windows(current_screen, scr_top, scr_front_main, scr_show_left, scr_show_main, scr_bottom)

    x = scr.getch()

    if x == 10:
        if open_window == 0:
            open_window = 1
            cursor_sub = [0, 0, 0, 0]
    if x == 263 or x == 127:
        if open_window == 1:
            open_window = 0
    if x == 102:        # f
        if open_window == 1 and cursor_main[2] == 1:
            if len(find_list) == 0:
                find_list = database.find_database_entry(cursor_main, cursor_sub, columns, shown_tables, current_table, scr_bottom, scr_dim)
                cursor_sub = [0, 0, 0, 0]
            else:
                find_list = []
                cursor_sub = [0, 0, 0, 0]
    if x == 100:        # d
        if open_window == 1 and cursor_main[2] == 1 and cursor_sub[1] + cursor_sub[0] > 1 and cursor_sub[2] == 0:
            current_table = database.get_table(shown_tables[cursor_main[0] + cursor_main[1] - 1], open_database)
            table_executions = database.delete_database_entry(cursor_main, cursor_sub, columns, shown_tables, current_table, open_database, scr_bottom, table_executions)
            if cursor_sub[1] == 0 or cursor_sub[1] == 1:
                cursor_sub[0] = cursor_sub[0] - 1
            else:
                cursor_sub[0] = cursor_sub[0] - 1
                cursor_sub[1] = cursor_sub[1] - 1
        if open_window == 1 and cursor_main[2] == 1 and cursor_sub[1] + cursor_sub[0] > 1 and cursor_sub[2] + cursor_sub[3] > 0:
            table_executions = database.delete_database_cell(cursor_main, cursor_sub, columns, shown_tables, current_table, open_database, scr_bottom, table_executions)
        if open_window == 1 and cursor_main[2] == 2 and cursor_sub[1] + cursor_sub[0] > 0:
            table_executions = database.delete_execution(cursor_main, cursor_sub, shown_tables, current_table, table_executions)
            if cursor_sub[0] > 1:
                cursor_sub[0] = cursor_sub[0] - 1
            elif cursor_sub[1] > 0:
                cursor_sub[1] = cursor_sub[1] - 1
            else:
                cursor_sub[0] = cursor_sub[0] - 1


    if x == 117:        # u
        if open_window == 1 and cursor_main[2] == 1 and cursor_sub[1] + cursor_sub[0] > 1 and cursor_sub[2] + cursor_sub[3] > 0:
            table_executions = database.update_database_cell(cursor_main, cursor_sub, columns, shown_tables, current_table, open_database, scr_bottom, scr_dim, table_executions)

    if x == 110:        # n
        if open_window == 1 and cursor_main[2] == 2:
            table_executions = database.new_execution(cursor_main, cursor_sub, table_executions)

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
            cursor_main = user_input.cursor_down(cursor_main, open_list, scr_dim, cursor_sub)
            cursor_sub = [0, 0, 0, 0]
        elif open_window == 1 and cursor_main[2] == 1:
            if find_list == []:
                cursor_sub = user_input.cursor_down(cursor_sub, entry_list, scr_dim, cursor_main)
            else:
                find_list.append(-1)
                cursor_sub = user_input.cursor_down(cursor_sub, find_list, scr_dim, cursor_main)
                find_list.remove(-1)
        elif open_window == 1 and cursor_main[2] == 2:
            cursor_sub = user_input.cursor_down(cursor_sub, executions_list, scr_dim, cursor_main)
        else:
            cursor_sub = user_input.cursor_down(cursor_sub, open_list, scr_dim, cursor_main)
    elif x == 259:
        if open_window == 0:
            cursor_main = user_input.cursor_up(cursor_main, open_list, scr_dim, cursor_sub)
            cursor_sub = [0, 0, 0, 0]
        elif open_window == 1 and cursor_main[2] == 1:
            cursor_sub = user_input.cursor_up(cursor_sub, entry_list, scr_dim, cursor_main)
        elif open_window == 1 and cursor_main[2] == 2:
            cursor_sub = user_input.cursor_up(cursor_sub, entry_list, scr_dim, cursor_main)
        else:
            cursor_sub = user_input.cursor_up(cursor_sub, open_list, scr_dim, cursor_main)
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
