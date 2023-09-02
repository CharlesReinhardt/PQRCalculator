-- run if database has not been created
-- CREATE DATABASE final_project_cprein19;
-- GRANT ALL PRIVILEGES ON DATABASE finalproject_cprein19 TO ehar;
-- GRANT ALL ON ALL TABLES IN SCHEMA public TO ehar;
-- CREATE TYPE day_of_week AS ENUM('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun');


-- BEGIN ENTITY SETS --

-- mentors table
DROP TABLE IF EXISTS mentors CASCADE;
CREATE TABLE mentors(
    first_name varchar,
    last_name varchar,
    class_year integer,
    PRIMARY KEY(first_name, last_name),
    CONSTRAINT valid_class_year CHECK (class_year > 1856)
);
-- insert into mentors
INSERT INTO 
    mentors 
        (first_name, last_name, class_year) 
    VALUES 
        ('Charles', 'Reinhardt', 2023);

-- courses table
DROP TABLE IF EXISTS courses CASCADE;
CREATE TABLE courses(
    id varchar PRIMARY KEY
);
-- insert into courses
INSERT INTO 
    courses
        (id)
    VALUES
        ('P101');

-- softwares table
DROP TABLE IF EXISTS softwares CASCADE;
CREATE TABLE softwares(
    name varchar PRIMARY KEY
);
-- insert into softwares
INSERT INTO
    softwares
        (name)
    VALUES
        ('PyPotions');

-- shifts table

DROP TABLE IF EXISTS shifts CASCADE;
CREATE TABLE shifts(
    day day_of_week,
    time time with time zone,
    PRIMARY KEY (day, time)
);
-- insert into shifts
INSERT INTO 
    shifts
        (day, time)
    VALUES
        ('Mon', '10:00:00 EST');

-- END ENTITY SETS --
-- BEGIN RELATIONSHIP SETS --

-- teaches table
DROP TABLE IF EXISTS teaches_courses;
CREATE TABLE teaches_courses(
    m_last varchar,
    m_first varchar,
    c_id varchar REFERENCES courses(id),
    PRIMARY KEY (m_last, m_first, c_id),
    FOREIGN KEY (m_last, m_first) REFERENCES mentors(last_name, first_name)
);
-- insert into teaches_courses
INSERT INTO
    teaches_courses
        (m_first, m_last, c_id)
    VALUES
        ('Charles', 'Reinhardt', 'P101');
-- remove from teaches_courses
DELETE FROM
    teaches_courses
WHERE
    m_first = 'Charles' AND
    m_last = 'Reinhardt' AND
    c_id = 'P101';

DROP TABLE IF EXISTS teaches_softwares;
CREATE TABLE teaches_softwares(
    m_last varchar,
    m_first varchar,
    s_name varchar REFERENCES softwares(name),
    PRIMARY KEY (m_last, m_first, s_name),
    FOREIGN KEY (m_last, m_first) REFERENCES mentors(last_name, first_name)
);
-- insert into teaches_softwares
INSERT INTO
    teaches_softwares
        (m_first, m_last, s_name)
    VALUES
        ('Charles', 'Reinhardt', 'PyPotions');
-- remove from teaches_softwares
DELETE FROM
    teaches_softwares
WHERE
    m_first = 'Charles' AND
    m_last = 'Reinhardt' AND
    s_name = 'PyPotions';

-- works table
-- relating mentors to shifts
DROP TABLE IF EXISTS works CASCADE;
CREATE TABLE works(
  m_first varchar,
  m_last varchar,
  s_day day_of_week,
  s_time time with time zone,
  FOREIGN KEY (m_first, m_last) REFERENCES mentors(first_name, last_name)
                  ON DELETE CASCADE,
  FOREIGN KEY (s_day, s_time) REFERENCES shifts(day, time)
                  ON DELETE CASCADE,
  PRIMARY KEY (m_first, m_last, s_day, s_time)
);
-- insert into works
INSERT INTO
    works
        (m_first, m_last, s_day, s_time)
    VALUES
        ('Charles','Reinhardt', 'Mon', '10:00:00 EST');
