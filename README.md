Hey Ed! Hope grading is going well. Here is a little guide to my final project, in the hopes it helps you navigate my repo.

0. Functional Requirements Document

My functional requirements document can be found in `FunctionalRequirements.pdf`, created with google docs and exported as pdf. Interestingly, this document is organzied similarly to how I organized functional requirements documents with AWS this summer. I thought this practice was fun, my classmates thought it was overkill. I think we were both right.

1. ER Diagram.

This can be found in `ERD.pdf`. Created with LucidChart with comments.

2. Schema Document

This can be found in `SCHEMA.pdf`. Created with google docs and exported as pdf.

3. Table creation.

The commands to create tables can be found in `DDL.sql`. These include the commands to grant ehar access to this database (that I am not positive work). Many of the create table commands are also run within our python program when we interact with our database.

4. Data population.

This database project uses real data from Fall 2022 data from our PQRC. This data can be found in csv files in the `data/` directory. These csv files conform to specifications found in `FunctionalRequirements.pdf`

5. Views and SQL Queries

The queries are where this project is lacking. There are no highly complicated queries, but all queries that drive our program can be found in `DML.sql`. They can also be found in `src/commands.py`.

6. NoSQL Angle

My NoSQL angle is the extensive python program I have created. I had hoped to include a NoSQL (json-style) database in my repo to hold mentor biography information. I did not get around to this, so I am counting my extensive (and so enjoyable) csv -> SQL manipulation as my "Not Only SQL"

7. Final Project Presentation

A copy of my slides can be found (in pdf form) in `presentation/presentation.pdf`

8. B+ Tree Drawing

A rough B+ Tree index drawing on my mentors table can be found in `RosterIndexBTree.jpeg`. It doesn't include arrows from the bottom level of the B+ Tree to the table. I got a cool educational experience out of creating the B+ Tree and perfecting it further was not something I was interested in.

9. My Python Program

Goodness. Can be accessed by running `cd src && python3 main.py`. Note that in order to connect to the database (through main.py), you will need to configure a database name and database user (in db_info.py). You'll also need to create a `src/.pwd` file in order to access the psql database.

The rest of things in this repo have helped me in some way stay organized while developing this project. Feel free to poke around as you so please. Thanks for a great semester. Happy Holidays!
