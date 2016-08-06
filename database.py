#!/usr/bin/env python

## IMPORTS ##
import curses
import sys
import os
import datetime
import sqlite3

## FUNCTIONS ##

def get_table(table_name, open_database):
    
    current_table = {table_name:{}}

    current_table[table_name] = open_database.execute('SELECT * FROM %s' % table_name).fetchall()

    return current_table
