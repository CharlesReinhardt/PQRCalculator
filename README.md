# Introduction

Welcome to the PQRCalculator! This repository holds the source code for automated course and software coverage calculation for the STLAWU PQRC. This project was developed as a project for CS-345 Database Systems. Turns out that it worked pretty decent, so we're keeping it around!

## Instructions

This is where I'd put a step by step instruction manual on how to use the PQRCalculator...

![](docs/images/IfIHadOne.jpeg)

1. Table creation.

The commands to create tables can be found in `DDL.sql`. These include the commands to grant ehar access to this database (that I am not positive work). Many of the create table commands are also run within our python program when we interact with our database.

2. Views and SQL Queries

The queries are where this project is lacking. There are no highly complicated queries, but all queries that drive our program can be found in `DML.sql`. They can also be found in `src/commands.py`.

3. Final Project Presentation

A copy of my slides can be found (in pdf form) in `presentation/presentation.pdf`

4. My Python Program

Goodness. Can be accessed by running `cd src && python3 main.py`. Note that in order to connect to the database (through main.py), you will need to configure a database name and database user (in db_info.py). You'll also need to create a `src/.pwd` file in order to access the psql database.

The rest of things in this repo have helped me in some way stay organized while developing this project. Feel free to poke around as you so please.
