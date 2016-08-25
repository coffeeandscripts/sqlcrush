#!/usr/bin/env python

## IMPORTS ##
import curses
import time
import sys
import os
import datetime
from sqlalchemy import *
from sqlalchemy.orm import *

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

def connect_database(n, current_real_database, dbname, user, host, password, port, socket, database_type, saved_database):

    database_dir = 0

    if saved_database == 0:
        if database_type == "mysql":
            sql_connect = str(database_type) + "+pymysql://"
        else:
            sql_connect = str(database_type) + "://"
        if user != 0:
            sql_connect = sql_connect + user
        if password != 0:
            sql_connect = sql_connect + ":" + password
        if host != 0:
            sql_connect = sql_connect + "@" + host
        if port != 0 and database_type != "mysql":
            sql_connect = sql_connect + ":" + port
        if dbname != 0:
            sql_connect = sql_connect + "/" + dbname
        if socket != 0 and database_type == "mysql":
            sql_connect = sql_connect + "?unix_socket='" + socket + "'"
    else:
        root_path = os.path.expanduser("~")
        f = open(root_path + "/.sqlcrush/saved_databases", "r")
        
        saved_dbs = f.readlines()
        f.close()
        length_save_name = len(saved_database)

        for line in saved_dbs:
            if saved_database == line.split(" ")[0]:
                if len(line.split(" ")) == 2:
                    sql_connect = line.split(" ")[1]
                elif len(line.split(" ")) == 3:
                    sql_connect = line.split(" ")[1]
                    database_dir = line.split(" ")[2]
    try:
        if database_dir != 0:
            os.chdir(database_dir)
        open_database = create_engine(sql_connect)
    except:
        open_database = 0

    return open_database

def save_database_to_file(dbname, user, host, password, port, database_type, scr_dim, scr_bottom):

    root_path = os.path.expanduser("~")

    save_input = user_input.save_database_name(scr_dim, scr_bottom)

    database_save = "\n" + save_input[0:-1] + " " + str(database_type) + "://"
    if user != 0:
        database_save = database_save + user
    if password != 0:
        database_save = database_save + ":" + password
    if host != 0:
        database_save = database_save + "@" + host
    if dbname != 0:
        database_save = database_save + "/" + dbname

    if database_type == "sqlite":
        current_dir = os.getcwd()
        database_save = database_save + " " + current_dir

    with open(root_path + "/.sqlcrush/saved_databases", "a") as f:
        f.write(database_save)

def get_table(table_name, open_database, database_dir):

    if database_dir != 0:
        os.chidir(database_dir)

    current_table = {table_name:{}}
    with open_database.connect() as conn:
        current_table[table_name] = conn.execute('SELECT * FROM %s' % table_name).fetchall()

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
    
    try:
        Session = sessionmaker(bind=open_database)
        conn = Session()
        conn.execute(sql_command)
        conn.commit()
        table_executions[str(shown_tables[cursor_main[0] + cursor_main[1] - 1])].append(sql_command)

    except:
        scr_bottom.clear()
        scr_bottom.addstr(1, 1, "Delete failed")
        scr_bottom.refresh()
        time.sleep(1)

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
        Session = sessionmaker(bind=open_database)
        conn = Session()
        conn.execute(sql_command)
        conn.commit()
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
        Session = sessionmaker(bind=open_database)
        conn = Session()
        conn.execute(sql_command)
        conn.commit()

        table_executions[str(shown_tables[cursor_main[0] + cursor_main[1] - 1])].append(str(sql_command))

    except:
        scr_bottom.clear()
        scr_bottom.addstr(1, 1, "Update failed")
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

def new_execution(cursor_main, cursor_sub, table_executions, scr_dim, open_database, scr_show_main, shown_tables, scr_bottom):

    new_execution = user_input.new_execution_input(scr_dim)

    try:
        Session = sessionmaker(bind=open_database)
        conn = Session()
        conn.execute(new_execution)
        conn.commit()

        table_executions[str(shown_tables[cursor_main[0] + cursor_main[1] - 1])].append(str(new_execution))

    except:
        scr_bottom.clear()
        scr_bottom.addstr(1, 1, "Execution failed")
        scr_bottom.refresh()
        time.sleep(1)

    return table_executions

def new_entry(cursor_main, cursor_sub, table_executions, scr_dim, open_database, scr_bottom, shown_tables, columns):

    empty_values = "("

    n = 0
    n_max = len(columns)

    for column in columns:
        if n < n_max - 1:
            n = n + 1
            if column[5] == 1 or str(column[5]) == "True":
                new_input = "DEFAULT"
            else:
                new_input = user_input.add_new_row(column, scr_dim, scr_bottom)
            if new_input == "DEFAULT":
                empty_values = empty_values + new_input + ", "
            elif str(new_input)[:-1] == "now":
                    empty_values = empty_values + "'" + str(datetime.datetime.now()) + "', "
            else:
                empty_values = empty_values + "'" + str(new_input)[:-1] + "', "

    empty_values = empty_values[:-2] + ")"

    sql_command = "INSERT INTO " + str(shown_tables[cursor_main[0] + cursor_main[1] - 1]) + " VALUES " + empty_values

    scr_bottom.addstr(1, 1, str(sql_command))

    scr_bottom.refresh()

    time.sleep(1)

    try:
        Session = sessionmaker(bind=open_database)
        conn = Session()
        conn.execute(sql_command)
        conn.commit()

        table_executions[str(shown_tables[cursor_main[0] + cursor_main[1] - 1])].append(str(sql_command))

    except:
        scr_bottom.clear()
        scr_bottom.addstr(1, 1, "New entry failed")
        scr_bottom.refresh()
        time.sleep(1)
   
    return table_executions


def close_databases(current_real_database, current_database, open_database, table_executions, database_type):

    open_database.close()

    if database_type == "SQLite3":

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

def new_user_query(scr_dim, scr_query_main, open_database):

    scr_query_main.addstr(1, 1, "Enter new query:    Ctrl-g to enter")

    for line in range(scr_dim[0]-10):
        if line < 8:
            line_print = " " + str(line)
        else:
            line_print = str(line)
        scr_query_main.addstr(line+2, 0, str(line+1))

    scr_query_main.refresh()

    new_user_query = user_input.new_query_input(scr_dim, scr_query_main)

    try:
        new_user_query = new_user_query.rstrip("\n")
        with open_database.connect() as conn:
            new_query_results = conn.execute(new_user_query).fetchall()
    except:
        try:
            with open_database.connect() as conn:
                conn.execute(new_user_query)
                conn.commit()
        except:
            scr_query_main.addstr(1, 1, "User query failed..", curses.A_REVERSE)
            scr_query_main.refresh()
            time.sleep(2)
            new_user_query = "000"

    return new_user_query

def favourite_queries():
    
    root_path = os.path.expanduser("~")

    try:
        f = open(root_path + "/.sqlcrush/favourite_queries", "r")
        
        fav_qs = f.readlines()
    except:
        fav_qs = []

    return fav_qs

def delete_fav_query(cursor):

    root_path = os.path.expanduser("~")

    f = open(root_path + "/.sqlcrush/favourite_queries", "r")
    fav_queries = f.readlines()
    f.close()
    new_fav_queries = []
    counter = 1
    for line in fav_queries:
        if counter != cursor[0] + cursor[1]:
            new_fav_queries.append(line)
        counter = counter + 1
    os.system("rm " + str(root_path) + "/.sqlcrush/favourite_queries")

    f = open(root_path + "/.sqlcrush/favourite_queries", "a+")
    for line in new_fav_queries:
        f.write(line.rstrip("\n"))
        f.write("\n")

def save_query(user_query):

    user_query = user_query + "\n"

    root_path = os.path.expanduser("~")

    with open(root_path + "/.sqlcrush/favourite_queries", "a+") as f:
        f.write(user_query)

def run_user_query(cursor_main, open_database):

    root_path = os.path.expanduser("~")

    f = open(root_path + "/.sqlcrush/favourite_queries", "r")
    fav_queries = f.readlines()
    f.close()

    new_user_query = fav_queries[cursor_main[0] + cursor_main[1] - 1]

    try:
        new_user_query = new_user_query.rstrip("\n")
        with open_database.connect() as conn:
            new_query_results = conn.execute(new_user_query).fetchall()
    except:
        try:
            with open_database.connect() as conn:
                conn.execute(new_user_query)
                conn.commit()
        except:
            scr_query_main.addstr(1, 1, "User query failed..", curses.A_REVERSE)
            scr_query_main.refresh()
            time.sleep(2)
            new_user_query = "000"

    return new_user_query

