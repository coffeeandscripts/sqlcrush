# **SQLcrush v0.1.5** - console based database editor

Build using python and ncurses, SQLcrush is dedicated to allowing you to access and edit a database directly from the console. Ideal when doing bugtesting and by SSH into the server itself. Simply run SQLcrush to view, edit and manipulate the database of your choice. Works with SQLite3, PostgreSQL and MariaDB/MySQL.

You can now apply your own queries with a query mode that can be entered by pressing k.

Everyone knows that a picture says 1000 words which is demonstrated below:

![Screenshot](https://raw.githubusercontent.com/coffeeandscripts/sqlcrush/master/example.png "SQLcrush screenshot")

## Features

 - Open up SQLite3/PostgreSQL/MySQL databased right from the console
 - Save the database and open it simply and quickly without typing the specs again
 - View each table and it's structure, browsing the content
 - Edit the content easily
 - Add and delete entries
 - Track all changes

## Additions Coming Soon

 - Rollback on changes easily at any point in the project
 - Query editor with REPL

## Usage

To open a file, make sure to do the following:

~~~~
SQLite3
> cd 'path of file'						#for saved databases
> sqlcrush -t sqlite -d test.db

PostgreSQL/MySQL
> sqlcrush -t postgresql -d test -u johnsmith -h localhost
~~~~

You can then save these setting in the app itself by pressing [s] and giving it a name which can then be pulled up again without having to cd into the direcotry (for SQLite3) by entering:

~~~~
> sqlcrush -o testdb
~~~~

~~~~
-t		**type of database (sqlite, postgresql, mysql)**
-d		**database name**
-h		host (e.g. localhost)
-p		port (usually defaults to 5432 so can be left out for postgreSQL)
-u		username
-pd		password
-s      socket (relevant for some MySQL servers)
-o		open saved database (remember the name you saved it as)
~~~~
 - Bold means essential unless opening saved database

### Query Mode

SQLcrush automatically saves your queries if they produce viewable tables such as through SELECT. These can be immediately re-entered by scrolling through them and hitting enter, or deleting them simply by pressing d.

Query mode can be toggled via pressing k. A new query can be made when in query mode by pressing n and entering the appropriate query, followed by control-g when done. When a table is viewed in query mode, the individual cells cannot be updated, deleted and a new entry cannot be made.

INSERT, DELETE and CREATE are all functional within the query editor, and if effective will not present the user with an error. It will however not save these as favourite queries as it is expected that these are one off actions.

## Quickstart Guide

#### Dependencies

 - SQLalchemy
 - psycopg2
 - pymysql
 - curses (should be installed in standard library)

There are multiple installation methods:

**Make sure you are running python3**

### PyPI

~~~~
> sudo pip install sqlcrush			# may have to run pip3
> sqlcrush							# immediately run to go through setup
~~~~

### Manual

 - download file to a location of choice

~~~~
> cd 'path'
> sudo python3 setup.py install		# can use just python if error
> sqlcrush							# immediately run to go through setup
~~~~

### Uninstall

~~~
> sudo pip uninstall sqlcrush
> rm -rf ~/.sqlcrush
~~~

## Known Issues

 - Issues when terminal window reduced to pointless size
 - Crash when sqlite3 database not first openned from within its own directory
 - Cursor not visible when entering text

## Troubleshooting:

Q: I'm unable to install SQLcrush since psycopg2 is asking for pg_config.

A: Please install postgresql on your system even if you don't intend to use it.

Q: I can't use backspace when I try enter a query. PS, I'm on a Mac.

A: If you're using standard Mac terminal, you can either go into Preferences>Profiles>Advanced and select "Delete sends Control-H" or you can manually enter Control-h in order to backspace/delete text.

## Licence

SQLcrush - console based database editor

Copyright (c) 2016 coffeeandscripts

coffeeandscripts.github.io

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
