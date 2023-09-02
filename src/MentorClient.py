import psycopg2
from commands import *
from db_info import DB_NAME, DB_USER

class MentorClient:

    valid_opts = {'1', '2', 'q', 'Q'}

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
        Display the mentor options
        :return: option selected by mentor
        '''
        while True:
            print("1) Change course coverage information")
            print("2) Change software coverage information")
            print("Q) Quit")

            opt = input("> ")
            if opt in self.valid_opts:
                break
            else:
                print("Invalid menu option. Try again")
        
        return opt

    def modify_course_coverage(self):
        """
        Allow a mentor to add/remove a course from their coverage information
        :return: None
        """

        mentor = self.get_user()
        m_first = mentor[0]
        m_last = mentor[1]

        course = self.get_course()

        action = self.get_coverage_action('course')
        
        if action == 'add':
            msg = self.add_course_coverage(m_first, m_last, course)
        elif action == 'remove':
            msg = self.remove_course_coverage(m_first, m_last, course)
        else:
            print("Internal error. Invalid action recieved: " + action)
            exit(1)

        self.conn.commit()    
        print(msg)
                    
    def modify_software_coverage(self):
        """
        Allow a mentor to add/remove a software from their coverage information
        :return: None
        """

        mentor = self.get_user()
        m_first = mentor[0]
        m_last = mentor[1]

        software = self.get_software()

        action = self.get_coverage_action("software")

        if action == 'add':
            msg = self.add_software_coverage(m_first, m_last, software)
        elif action == 'remove':
            msg = self.remove_software_coverage(m_first, m_last, software)
        else:
            print("Internal error. Invalid action recieved: " + action)
            exit(1)

        self.conn.commit()
        print(msg)

    def get_user(self):
        """
        Get a mentor name (and check that it is valid) as input from the user
        :return: a tuple of (first_name, last_name)
        """
        cur = self.conn.cursor()

        print("Enter your name (first last)")
        while True:
            m_full = input("> ").split(' ')
            m_first = m_full[0].title()
            m_last = m_full[1].title()
            args = (m_first, m_last)

            cur.execute(CHECK_MENTOR_IS_VALID, args)
            count = cur.fetchone()[0]

            if count > 0:
                return (m_first, m_last)
            else:
                print("Invalid Mentor Name. Try again")

    def get_course(self):
        """
        Get a course ID (and check that it is valid) as input from the user
        :return: course ID
        """
        cur = self.conn.cursor()

        while True:
            print("What course would you like to add/remove?")

            course = input("> ")
            cur.execute(CHECK_COURSE_IS_VALID, (course,))
            count = cur.fetchone()[0]

            if count > 0:
                return course
            else:
                print("Invalid Course ID. Try again")

    def get_software(self):
        """
        Get a software name (and check that it is valid) as input from the user
        :return: software name
        """
        cur = self.conn.cursor()

        while True:
            print("What software would you like to add/remove?")

            course = input("> ")
            cur.execute(CHECK_SOFTWARE_IS_VALID, (course,))
            count = cur.fetchone()[0]

            if count > 0:
                return course
            else:
                print("Invalid software name. Try again")

    def get_coverage_action(self, type):
        """
        Get whether a user would like to add/remove from their coverage information
        :return: add or remove
        """
        print("Would you like to add or remove coverage for this {}?".format(type))
        
        while True:
            action = input("> ").lower()
            if action in {'add', 'remove'}:
                return action
            else:
                print("Invalid action. Valid options include \"Add\" or \"Remove\". Try again.")

    def add_course_coverage(self, m_first, m_last, course):
        """
        Add a course to a mentor's course coverage information
        :return: message regarding DB insert success or failure
        """
        cur = self.conn.cursor()
        args = (m_last, m_first, course)

        cur.execute(CHECK_TEACHES_COURSES_ENTRY_EXISTS, args)
        count = cur.fetchone()[0]

        if count > 0:
            return "Course {} is already covered by {} {}".format(course, m_first, m_last)
        else:
            cur.execute(INSERT_TEACHES_COURSES, args)
            return "Course {} added to coverage for {} {}".format(course, m_first, m_last)

    def remove_course_coverage(self, m_first, m_last, course):
        """
        Remove a course from a mentor's course coverage information
        :return: message regarding DB remove success or failure
        """
        cur = self.conn.cursor()
        args = (m_last, m_first, course)

        cur.execute(CHECK_TEACHES_COURSES_ENTRY_EXISTS, args)
        count = cur.fetchone()[0]

        if count > 0:
            cur.execute(DELETE_FROM_TEACHES_COURSES, args)
            return "Course {} removed from coverage for {} {}".format(course, m_first, m_last)
        else:
            return "Course {} not covered by {} {}".format(course, m_first, m_last)


    def add_software_coverage(self, m_first, m_last, software):
        """
        Add a software to a mentor's software coverage information
        :return: message regarding DB insert success or failure
        """
        cur = self.conn.cursor()
        args = (m_last, m_first, software)

        cur.execute(CHECK_TEACHES_SOFTWARES_ENTRY_EXISTS, args)
        count = cur.fetchone()[0]

        if count > 0:
            return "Software {} is already covered by {} {}".format(software, m_first, m_last)
        else:
            cur.execute(INSERT_TEACHES_SOFTWARES, args)
            return "Software {} added to coverage for {} {}".format(software, m_first, m_last)

    def remove_software_coverage(self, m_first, m_last, software):
        """
        Remove a software to a mentor's software coverage information
        :return: message regarding DB remove success or failure
        """
        cur = self.conn.cursor()
        args = (m_last, m_first, software)

        cur.execute(CHECK_TEACHES_SOFTWARES_ENTRY_EXISTS, args)
        count = cur.fetchone()[0]

        if count > 0:
            cur.execute(DELETE_FROM_TEACHES_SOFTWARES, args)
            return "Software {} removed from coverage for {} {}".format(software, m_first, m_last)
        else:
            return "Software {} not covered by {} {}".format(software, m_first, m_last)

    def execute(self, opt):
        """
        Execute the option given by the user
        :return:
        """
        if opt not in self.valid_opts:
            raise ValueError("Invalid option passed to execute: " + opt)

        opt_map = {
            '1': self.modify_course_coverage,
            '2': self.modify_software_coverage,
            'q': exit,
            'Q': exit
        }

        opt_map[opt]()