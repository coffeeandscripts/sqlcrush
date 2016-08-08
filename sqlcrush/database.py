#!/usr/bin/env python

## IMPORTS ##
import curses
import time
import sys
import os
import datetime
import sqlite3

from sqlcrush import user_input

## FUNCTIONS ##

def print_intro():

    print(" ______   ______    __       ______   ______    __  __   ______   ___   ___     ")
    print("/_____/\ /_____/\  /_/\     /_____/\ /_____/\  /_/\/_/\ /_____/\ /__/\ /__/\    ")
    print("\::::_\/_\:::_ \ \ \:\ \    \:::__\/ \:::_ \ \ \:\ \:\ \\\\::::_\/_\::\ \\\\  \ \   ")
    print(" \:\/___/\\\\:\ \ \ \_\:\ \    \:\ \  __\:(_) ) )_\:\ \:\ \\\\:\/___/\\\\::\/_\ .\ \  ")
    print("  \_::._\:\\\\:\ \ /_ \\\\:\ \____\:\ \/_/\\\\: __ `\ \\\\:\ \:\ \\\\_::._\:\\\\:: ___::\ \ ")
    print("    /____\:\\\\:\_-  \ \\\\:\/___/\\\\:\_\ \ \\\\ \ `\ \ \\\\:\_\:\ \ /____\:\\\\: \ \\\\::\ \\")
    print("    \_____\/ \___|\_\_/\_____\/ \_____\/ \_\/ \_\/ \_____\/ \_____\/ \__\/ \::\/")
    print()
    print("                                                             by coffeeandscripts")

    time.sleep(1)
    print()
    print("Initializing...")
    time.sleep(2)

def get_table(table_name, open_database):

    current_table = {table_name:{}}

    current_table[table_name] = open_database.execute('SELECT * FROM %s' % table_name).fetchall()

    return current_table

def delete_database_entry(cursor_main, cursor_sub, columns, shown_tables, current_table, open_database, scr_bottom, table_executions, current_real_database, current_database, find_list):

    n = 0

    for column in columns:
        if column[5] == 1:
            current_entry_primary_key = n
            current_entry_primary_key_name = column[1]
            break
        else:
            n = n + 1

    if find_list != []:
        current_entry_primary_key_id = current_table[shown_tables[cursor_main[0] + cursor_main[1] - 1]][find_list[cursor_sub[0] + cursor_sub[1] - 2]][current_entry_primary_key]
    else:
        current_entry_primary_key_id = current_table[shown_tables[cursor_main[0] + cursor_main[1] - 1]][cursor_sub[0] + cursor_sub[1] - 2][current_entry_primary_key]

    sql_command = "DELETE from " + str(shown_tables[cursor_main[0] + cursor_main[1] - 1]) + " WHERE " + str(current_entry_primary_key_name) + "=" + str(current_entry_primary_key_id)

    scr_bottom.addstr(1, 1, str(sql_command))

    scr_bottom.refresh()

    time.sleep(1)

    open_database.execute(sql_command)

    open_database.commit()

    table_executions[str(shown_tables[cursor_main[0] + cursor_main[1] - 1])].append(sql_command)

    return table_executions

def delete_database_cell(cursor_main, cursor_sub, columns, shown_tables, current_table, open_database, scr_bottom, table_executions, find_list):

    n = 0

    for column in columns:
        if column[5] == 1:
            current_entry_primary_key = n
            current_entry_primary_key_name = column[1]
            break
        else:
            n = n + 1

    if find_list != []:
        current_entry_primary_key_id = current_table[shown_tables[cursor_main[0] + cursor_main[1] - 1]][find_list[cursor_sub[0] + cursor_sub[1] - 2]][current_entry_primary_key]
    else:
        current_entry_primary_key_id = current_table[shown_tables[cursor_main[0] + cursor_main[1] - 1]][cursor_sub[0] + cursor_sub[1] - 2][current_entry_primary_key]

    sql_command = "UPDATE " + str(shown_tables[cursor_main[0] + cursor_main[1] - 1]) + " SET " + str(columns[cursor_sub[2] + cursor_sub[3] - 1][1]) + " = " + "NULL" + " WHERE " + str(current_entry_primary_key_name) + "=" + str(current_entry_primary_key_id)

    scr_bottom.addstr(1, 1, str(sql_command))
    table_executions[str(shown_tables[cursor_main[0] + cursor_main[1] - 1])].append(str(sql_command))

    scr_bottom.refresh()

    time.sleep(1)

    try:
        open_database.execute(sql_command)
        open_database.commit()
        table_executions[str(shown_tables[cursor_main[0] + cursor_main[1] - 1])].append(str(sql_command))
    except:
        scr_bottom.clear()
        scr_bottom.addstr(1, 1, "Delete failed")
        scr_bottom.refresh()
        time.sleep(1)

    return table_executions

def update_database_cell(cursor_main, cursor_sub, columns, shown_tables, current_table, open_database, scr_bottom, scr_dim, table_executions, find_list):

    n = 0

    for column in columns:
        if column[5] == 1:
            current_entry_primary_key = n
            current_entry_primary_key_name = column[1]
            break
        else:
            n = n + 1
    if find_list != []:
        original = current_table[shown_tables[cursor_main[0] + cursor_main[1] - 1]][find_list[cursor_sub[0] - cursor_sub[1] - 2]][cursor_sub[2] + cursor_sub[3] - 1]
    else:
        original = current_table[shown_tables[cursor_main[0] + cursor_main[1] - 1]][cursor_sub[0] - cursor_sub[1] - 2][cursor_sub[2] + cursor_sub[3] - 1]

    new_entry = user_input.update_cell(scr_dim, original)

    if find_list != []:
        current_entry_primary_key_id = current_table[shown_tables[cursor_main[0] + cursor_main[1] - 1]][find_list[cursor_sub[0] + cursor_sub[1] - 2]][current_entry_primary_key]
    else:
        current_entry_primary_key_id = current_table[shown_tables[cursor_main[0] + cursor_main[1] - 1]][cursor_sub[0] + cursor_sub[1] - 2][current_entry_primary_key]
    if str(user_input) != " " and str(user_input) != "\n" and str(user_input) != "":
        sql_command = "UPDATE " + str(shown_tables[cursor_main[0] + cursor_main[1] - 1]) + " SET " + str(columns[cursor_sub[2] + cursor_sub[3] - 1][1]) + " = '" + str(new_entry)[:-1] + "' WHERE " + str(current_entry_primary_key_name) + "=" + str(current_entry_primary_key_id)

        scr_bottom.addstr(1, 1, str(sql_command))

    try:
        open_database.execute(sql_command)
        open_database.commit()
        table_executions[str(shown_tables[cursor_main[0] + cursor_main[1] - 1])].append(str(sql_command))
    except:
        scr_bottom.clear()
        scr_bottom.addstr(1, 1, "Delete failed")
        scr_bottom.refresh()
        time.sleep(1)


    return table_executions

def delete_execution(cursor_main, cursor_sub, shown_tables, current_table, table_executions, current_real_database, current_database, open_database):

    execution_entry_position = len(table_executions[str(shown_tables[cursor_main[0] + cursor_main[1] - 1])]) - cursor_sub[0] - cursor_sub[1]

    execution_to_remove = table_executions[str(shown_tables[cursor_main[0] + cursor_main[1] - 1])][execution_entry_position]

    table_executions[str(shown_tables[cursor_main[0] + cursor_main[1] - 1])].remove(str(execution_to_remove))

    open_database.close()

    os.system("rm " + current_database)

    os.system("cp " + current_real_database + " " + current_database)

    temp_database = sqlite3.connect(str(current_database))

    for table in table_executions:
        for execution in table_executions[table]:
            try:
                temp_database.execute(execution)
                temp_database.commit()
            except:
                pass

    temp_database.close()

    return table_executions

def find_database_entry(cursor_main, cursor_sub, columns, shown_tables, current_table, scr_bottom, scr_dim):

    scr_bottom.clear()
    scr_bottom.refresh()

    find_column = user_input.find_column_input(scr_bottom, scr_dim)
    find_value = user_input.find_value_input(scr_bottom, scr_dim)

    scr_bottom.clear()
    scr_bottom.refresh()

    column_found = 0
    n = 0

    for column in columns:
        if str(find_column)[:-1] == str(column[1]):
            column_found = 1
            column_id = n
        n = n + 1
    if column_found == 0:
        scr_bottom.addstr(1, 1, "Column not found...", curses.A_REVERSE)
        scr_bottom.refresh()
        time.sleep(2)
        return []

    p = 0

    find_list = []

    for entry in current_table[shown_tables[cursor_main[0] + cursor_main[1] - 1]]:
        if str(entry[column_id]) == str(find_value)[:-1]:
            find_list.append(p)
        p = p + 1

    return find_list

def new_execution(cursor_main, cursor_sub, table_executions, scr_dim, open_database, scr_show_main, shown_tables):

    new_execution = user_input.new_execution_input(scr_dim)

    try:
        open_database.execute(new_execution)
        open_database.commit()
        table_executions[str(shown_tables[cursor_main[0] + cursor_main[1] - 1])].append(new_execution)
    except:
        scr_show_main.addstr(1, 1, "Execution failed...")
        scr_show_main.refresh()
        time.sleep(1)

    return table_executions

def new_entry(cursor_main, cursor_sub, table_executions, scr_dim, open_database, scr_bottom, shown_tables, columns):

    empty_values = "("

    n = 0
    n_max = len(columns)

    for column in columns:
        if n < n_max - 1:
            n = n + 1
            if column[3] == 0 or column[5] == 1:
                empty_values = empty_values + "NULL, "
            else:
                empty_values = empty_values + "'-----', "

    empty_values = empty_values[:-2] + ")"

    sql_command = "INSERT INTO " + str(shown_tables[cursor_main[0] + cursor_main[1] - 1]) + " VALUES " + empty_values

    scr_bottom.addstr(1, 1, str(sql_command))

    scr_bottom.refresh()

    time.sleep(1)
    #try:
    open_database.execute(sql_command)

    open_database.commit()

    table_executions[str(shown_tables[cursor_main[0] + cursor_main[1] - 1])].append(sql_command)
    """
    except:
        scr_bottom.clear()
        scr_bottom.addstr(1, 1, "New entry failed")
        scr_bottom.refresh()
        time.sleep(1)
    """
    return table_executions


def close_databases(current_real_database, current_database, open_database, table_executions):

    open_database.close()

    real_database = sqlite3.connect(str(current_real_database))

    for table in table_executions:
        for execution in table_executions[table]:
            try:
                real_database.execute(execution)
                real_database.commit()
            except:
                pass

    real_database.close()

    os.system("rm " + current_database)
