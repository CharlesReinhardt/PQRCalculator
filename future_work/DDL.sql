-- covers table
-- to represent a mentor covering another mentor's shift
-- FUTURE WORK
DROP TABLE IF EXISTS covers CASCADE;
CREATE TABLE covers(
    m_first_covered varchar,
    m_last_covered varchar,
    m_first_covering varchar,
    m_last_covering varchar,
    s_dow day_of_week,
    s_time time with time zone,
    date date,
    FOREIGN KEY (m_first_covered, m_last_covered, s_dow, s_time) REFERENCES works(m_first, m_last, s_day, s_time)
                   ON DELETE CASCADE,
    FOREIGN KEY (m_first_covering, m_last_covering) REFERENCES mentors(first_name, last_name)
                   ON DELETE CASCADE,
    PRIMARY KEY (m_first_covered, m_last_covered, m_first_covering, m_last_covering, s_dow, s_time, date)
);