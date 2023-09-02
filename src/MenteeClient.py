import psycopg2
from commands import *
from coverage_utils import *
from db_info import DB_NAME, DB_USER


VALID_DAYS = {'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'}

class MenteeClient:

    valid_opts = {'1', '2', '3', 'q', 'Q'}

    def __init__(self):
        try: 
            pwd_file = open('.pwd')
        except OSError:
            print("Error: No authorization")
            exit()
        
        try: 
            self.conn = psycopg2.connect(
                dbname = DB_NAME,
                user = DB_USER,
                password = pwd_file.readline(),
                host = "ada.hpc.stlawu.edu"
            )
        except psycopg2.Error:
            print("Error: cannot connect to database")
            exit()
        finally:
            pwd_file.close()

    def menu(self):
        '''
        Display the mentee options
        :return: option selected by the mentee
        '''
        while True:
            print("1) Find when a course is taught")
            print("2) Find when a software is taught")
            print("3) Find who is working at a given time")
            print("Q) Quit")

            opt = input("> ")
            if opt in self.valid_opts:
                break
            else:
                print("Invalid menu option. Try again")
        
        return opt   

    def find_course_coverage(self):
        """
        Get course input from the user and print out a list of days and times that the course is covered
        :return: None
        """
        course = input("Enter the course ID that you are looking for: ")

        coverage_map = get_course_coverage_map(self.conn, course)

        output = coverage_output(coverage_map)

        for row in output:
            print(''.join(row))
    
    def find_software_coverage(self):
        """
        Get software input from the user and print out a list of days and times that the software is covered
        :return: None
        """
        software = input("Enter the software name that you are looking for: ")

        coverage_map = get_software_coverage_map(self.conn, software)

        output = coverage_output(coverage_map)

        for row in output:
            print(''.join(row))

    def find_workers(self):
        """
        Get a time and day from the user and print out a list of mentors working at that time
        :return: None
        """
        cur = self.conn.cursor()

        input_day = self.get_day_input()
        input_hour = self.get_hour_input()
        args = (input_day, input_hour)

        cur.execute(FIND_WORKER, args)
        output = []
        for row in cur:
            output.append(row[0] + " " + row[1])

        if len(output) == 0:
            print("No PQRC workers at this time")
            return None

        for row in output:
            print(row)
        

    def get_day_input(self):
        """
        Get a day value (and check that it is valid) from user input
        :return: day given as input
        """

        while True:
            input_day = input("Enter a day (Mon, Tue, Wed, Thu, Fri, or Sun): ")
            if input_day not in VALID_DAYS:
                print("Not a valid day value. Try again")
            else:
                return input_day

    def get_hour_input(self):
        """
        Get an hour value (and check that it is valid) from user input
        :return: an ISO formatted time string the hour given (in EST)
        """

        while True:
            input_hour = input("Enter a whole hour value (i.e. 10, 11): ")
            if not input_hour.isnumeric():
                print("Not a valid time value. Try again")
            else:
                return "{}:00:00 EST".format(input_hour)

    def execute(self, opt):
        """
        Execute option given by the user
        :return: None
        """
        if opt not in self.valid_opts:
            raise ValueError("Invalid option passed to execute: " + opt)

        opt_map = {
            '1': self.find_course_coverage,
            '2': self.find_software_coverage,
            '3': self.find_workers,
            'q': exit,
            'Q': exit,
        }

        opt_map[opt]()