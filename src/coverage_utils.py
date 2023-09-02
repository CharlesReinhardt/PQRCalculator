from commands import *

def get_course_coverage_map(conn, course):
    """
    Given a course name, return a map of days and times that course is taught
    :return: coverage_map
    """
    cur = conn.cursor()
    cur.execute(FIND_COURSE_COVERAGE, (course,))
    coverage_map = {
        'Sun': [],
        'Mon': [],
        'Tue': [],
        'Wed': [],
        'Thu': [],
        'Fri': []
    }
    
    for row in cur:
        day = row[1]
        hour = row[2].hour
        coverage_map[day].append(hour)

    return coverage_map

def get_software_coverage_map(conn, software):
    """
    Given a software name, return a map of days and times that software is taught
    :return: coverage_mape
    """
    cur = conn.cursor()
    cur.execute(FIND_SOFTWARE_COVERAGE, (software,))

    coverage_map = {
        'Sun': [],
        'Mon': [],
        'Tue': [],
        'Wed': [],
        'Thu': [],
        'Fri': []
    }
    
    for row in cur:
        day = row[1]
        hour = row[2].hour
        coverage_map[day].append(hour)

    return coverage_map


def coverage_output(coverage_map):
    """
    Given a coverage_map, print in a human readable format in stdout
    :return: None
    """

    all_output = []

    for day in coverage_map:
        row_output = [day]

        prev_hour = 0
        hours = coverage_map[day]

        for hour_idx in range(len(hours)):
            hour = hours[hour_idx]
            if prev_hour + 1 != hour:
                if prev_hour != 0:
                    row_output.append(str(prev_hour + 1))

                row_output.append(' ')
                row_output.append(str(hour))
                row_output.append('-')

            if hour_idx == len(hours) - 1:
                row_output.append(str(hour + 1))

            prev_hour = hour

        all_output.append(row_output)

    return all_output