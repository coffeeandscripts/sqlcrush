# **SQLcrush v0.1.1** - console based database editor

Build using python and ncurses, SQLcrush is dedicated to allowing you to access and edit a database directly from the console. Ideal when doing bugtesting and by SSH into the server itself. Simply run SQLcrush to view, edit and manipulate the database of your choice. Currently runs for SQLite3 but more features will be coming shortly.

Everyone knows that a picture says 1000 words which is demonstrated below:

![Screenshot](https://raw.githubusercontent.com/coffeeandscripts/sqlcrush/master/example.png "SQLcrush screenshot")

## Features

 - Open up SQLite3 databased right from the console
 - View each table and it's structure, browsing the content
 - Edit the content easily
 - Go back on any changes by controlling the executions that have been made
 - The database is always safe until a saved exit where changes will be applied
 - Add and delete entries
 - Track all changes

## Quickstart Guide

#### Dependencies

 - sqlite3 (should be installed in standard library)
 - curses (should be installed in standard library)

There are multiple installation methods:

** Make sure you are running python3 **

### PyPI

~~~~
> sudo pip install sqlcrush			# may have to run pip3
> sqlcrush
~~~~

### Manual

 - download file to a location of choice

~~~~
> cd 'path'
> sudo python3 setup.py install		# can use just python if error
> sqlcrush
~~~~

### Uninstall

~~~
> sudo pip uninstall sqlcrush
~~~

## Usage

To open a file, make sure to do the following:

~~~~
> cd 'path of file'
> sqlcrush filename.db			# this may also be filename.sqlite3
~~~~

Make sure to quit using [q] since that will save the changes made. A hard close of the terminal window will cause all changes to be neglected and the database will remain as normal.

## Known Issues

 - Issues when terminal window reduced to pointless size

## Licence

SQLcrush - console based database editor

Copyright (c) 2016 coffeeandscripts

coffeeandscripts.github.io

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
