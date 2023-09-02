--------------------

-- EXISTENCE CHECKS --
-- check mentor existss
SELECT
    count(*)
FROM
    mentors
WHERE
    first_name = 'Charles' AND
    last_name = 'Reinhardt';

-- check course exists
SELECT
    count(*)
FROM
    courses
WHERE
    id = 'P101';

-- check software exists
SELECT
    count(*)
FROM
    softwares
WHERE
    name = 'PyPotions';

-- check that a mentor teaches a particular course
SELECT
    count(*)
FROM
    teaches_courses
WHERE 
    m_first = 'Charles' AND
    m_last = 'Reinhardt' AND
    c_id = 'P101';

-- check that a mentor teaches a particular software
SELECT
    count(*)
FROM
    teaches_softwares
WHERE 
    m_first = 'Charles' AND
    m_last = 'Reinhardt' AND
    s_name = 'PyPotions';

-- QUERIES --

-- find the times a particular course is taught
SELECT DISTINCT
    c_id, s_day, s_time
FROM
    teaches_courses JOIN works USING (m_last, m_first)
WHERE
    c_id = 'P101';

-- find the times a particular software is taught
SELECT DISTINCT
    s_name, s_day, s_time
FROM
    teaches_softwares JOIN works USING (m_last, m_first)
WHERE
    s_name = 'PyPotions';

-- find the times a particular mentor is working
SELECT
    m_first, m_last
FROM
    works
WHERE
    s_day = 'Mon' AND
    s_time = '10:00:00 EST';

-- get a list of all classes
SELECT
    id
FROM
    courses;

-- get a list of all softwares
SELECT
    name
FROM
    softwares;