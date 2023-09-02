### MENTORS DDL ###
DROP_MENTORS = """
    DROP TABLE IF EXISTS mentors CASCADE;
"""

CREATE_MENTORS = """
    CREATE TABLE mentors(
        first_name varchar,
        last_name varchar,
        class_year integer,
        PRIMARY KEY(first_name, last_name),
        CONSTRAINT valid_class_year CHECK (class_year > 1856)
    );
"""

INSERT_MENTOR = """
    INSERT INTO 
        mentors 
            (first_name, last_name, class_year) 
        VALUES 
            (%s, %s, %s);
    """

### COURSES DDL ###
DROP_COURSES = """
    DROP TABLE IF EXISTS courses CASCADE;
"""

CREATE_COURSES = """
    CREATE TABLE courses(
        id varchar PRIMARY KEY
    );
"""

INSERT_COURSE = """
    INSERT INTO 
        courses(id) 
    VALUES
        (%s);
"""

DROP_TEACHES_COURSES = """
    DROP TABLE IF EXISTS teaches_courses;
"""

CREATE_TEACHES_COURSES = """
    CREATE TABLE teaches_courses(
        m_last varchar,
        m_first varchar,
        c_id varchar REFERENCES courses(id),
        PRIMARY KEY (m_last, m_first, c_id),
        FOREIGN KEY (m_last, m_first) REFERENCES mentors(last_name, first_name)
    );
"""

INSERT_TEACHES_COURSES = """
    INSERT INTO
        teaches_courses(m_last, m_first, c_id)
    VALUES
        (%s, %s, %s);
"""

DELETE_FROM_TEACHES_COURSES = """
    DELETE FROM
        teaches_courses
    WHERE
        m_first = %s AND
        m_last = %s AND
        c_id = %s;
"""

### SOFTWARES DDL ###
DROP_SOFTWARES = """
    DROP TABLE IF EXISTS softwares CASCADE;
"""

CREATE_SOFTWARES = """
    CREATE TABLE softwares(
        name varchar PRIMARY KEY
    );
"""

INSERT_SOFTWARE = """
    INSERT INTO
        softwares(name)
    VALUES
        (%s);
"""

DROP_TEACHES_SOFTWARES = """
    DROP TABLE IF EXISTS teaches_softwares;
"""

CREATE_TEACHES_SOFTWARES = """
    CREATE TABLE teaches_softwares(
        m_last varchar,
        m_first varchar,
        s_name varchar REFERENCES softwares(name),
        PRIMARY KEY (m_last, m_first, s_name),
        FOREIGN KEY (m_last, m_first) REFERENCES mentors(last_name, first_name)
    );
"""

INSERT_TEACHES_SOFTWARES = """
    INSERT INTO
        teaches_softwares(m_last, m_first, s_name)
    VALUES
        (%s, %s, %s);
"""

DELETE_FROM_TEACHES_SOFTWARES = """
    DELETE FROM
        teaches_softwares
    WHERE
        m_first = %s AND
        m_last = %s AND
        s_name = %s;
"""

### SHIFTS DDL ###
DROP_SCHEDULE = """
    DROP TABLE IF EXISTS shifts CASCADE;
"""

CREATE_SCHEDULE = """
    CREATE TABLE shifts(
        day day_of_week,
        time time with time zone,
        PRIMARY KEY (day, time)
    );
"""

INSERT_SHIFT = """
    INSERT INTO 
        shifts 
    VALUES 
        (%s, %s);
"""

DROP_WORKS = """
    DROP TABLE IF EXISTS works CASCADE;
"""

CREATE_WORKS = """
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
"""

INSERT_WORKS = """
    INSERT INTO 
        works 
    VALUES
        (%s, %s, %s, %s);
"""

### EXISTENCE CHECKS ###
CHECK_MENTOR_IS_VALID = """
    SELECT
        count(*)
    FROM
        mentors
    WHERE
        first_name = %s AND
        last_name = %s;
"""

CHECK_COURSE_IS_VALID = """
    SELECT
        count(*)
    FROM
        courses
    WHERE
        id = %s;
"""

CHECK_SOFTWARE_IS_VALID = """
    SELECT
        count(*)
    FROM
        softwares
    WHERE
        name = %s;
"""

CHECK_TEACHES_COURSES_ENTRY_EXISTS = """
    SELECT
        count(*)
    FROM
        teaches_courses
    WHERE 
        m_last = %s AND
        m_first = %s AND
        c_id = %s;
"""

CHECK_TEACHES_SOFTWARES_ENTRY_EXISTS = """
    SELECT
        count(*)
    FROM
        teaches_softwares
    WHERE 
        m_last = %s AND
        m_first = %s AND
        s_name = %s;
"""

### QUERIES ###
FIND_COURSE_COVERAGE = """
    SELECT DISTINCT
        c_id, s_day, s_time
    FROM
        teaches_courses JOIN works USING (m_last, m_first)
    WHERE
        c_id = %s;
"""

FIND_SOFTWARE_COVERAGE = """
    SELECT DISTINCT
        s_name, s_day, s_time
    FROM
        teaches_softwares JOIN works USING (m_last, m_first)
    WHERE
        s_name = %s;
"""

FIND_WORKER = """
    SELECT
        m_first, m_last
    FROM
        works
    WHERE
        s_day = %s AND
        s_time = %s;
"""

FIND_CLASSES = """
    SELECT
        id
    FROM
        courses;
"""

FIND_SOFTWARES = """
    SELECT
        name
    FROM
        softwares;
"""