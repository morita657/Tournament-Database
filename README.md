# Tournament-Database
This project is part of the Full Stack Web Developer nanodegree from udacity.

## The purpose of this project
Modern data-driven applications require a developers that know how to store data and interact programmatically with that data.
The project utilizes [Intro to Relational Databases](https://www.udacity.com/course/intro-to-relational-databases--ud197) to design a database based off of a provided specification and use case and then write code that makes use of that data with Python prgramme and PostgreSQL database.

## Technologies
This project requires Python 2.X (2.7.x is expected) and PostgreSQL 9.3 or latest version.
[Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads) are required to run SQL database server and web app. You need to install them on your machine.

## How to run
Download or clone repository on you machine.
Bring the project directory under the vagrant directory.
Start the virtual machine using `vagrant up` command.
After that, run `vagrant ssh` to log in to your VM.
Access the database using `psql` command and run SQL statements.
Test tournament.py running `python tournament_test.py` command.
Check that the last line of the output from this command is 'Success!  All tests pass!'
Shutdown the VM with `CTRL + D`.

## Files
This project is comprised of 3 files:
- tournament.py	 
This file contains the implementation of Swiss-system tournament
- tournament.sql
This file contains the table definition for the project
- tournament_test.py
This file is for the unit-tests for tournament.py

## Code Quality
[Here](https://google.github.io/styleguide/pyguide.html) is the Google Python Style Guide that I followed.
