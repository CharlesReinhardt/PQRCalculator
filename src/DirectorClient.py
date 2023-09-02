import psycopg2
from commands import *
from coverage_utils import *
from db_info import DB_NAME, DB_USER

data_dir = "../data/"

class DirectorClient:

    valid_opts = {'1', '2', '3', '4', '5', 'q', 'Q'}

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
        Display the director options
        :return: option selected by director
        '''
        while True:
            print("1) Upload mentor roster csv")
            print("2) Upload mentor schedule csv")
            print("3) Upload mentor coverage csv")
            print("4) Generate an overall course coverage sheet")
            print("5) Generate an overall software coverage sheet")
            print("Q) Quit")

            opt = input("> ")
            if opt in self.valid_opts:
                break
            else:
                print("Invalid menu option. Try again")
        
        return opt

    def input_path(self, message):
        """
        Get an input path (and check that it is valid) to a file from the user
        :return: path given by user
        """
        while True:
            path = data_dir + input(message)

            try:
                open(path)
                break
            except OSError:
                print("Invalid filename. Make sure your filename is in the 'data' folder and ends with '.csv'")

        return path

    def upload_mentor_roster(self):
        '''
        Upload a roster of current PQRC mentors
        :return: None
        '''

        #path = '../RealData/MentorRosterData.csv'
        path = self.input_path("Input mentor roster csv filename: ")

        cur = self.conn.cursor()

        # in case of re-upload, delete old data
        cur.execute(DROP_MENTORS)
        cur.execute(CREATE_MENTORS)

        f = open(path)
        # throw away header line
        f.readline()

        lines = f.readlines()
        line_no = 0
        for line in lines:
            line_no += 1
            words = line.split(',')
            inputs = (words[0].strip(), words[1].strip(), words[2].strip())

            try:
                cur.execute(INSERT_MENTOR, inputs)
            except psycopg2.Error:
                print("Unsuccessful Roster Upload on line " + str(line_no) + ". Exiting.")
                f.close()
                exit(1)

        self.conn.commit()

        print("Mentor Roster Upload Successful")
        f.close()

    def upload_mentor_schedule(self):
        '''
        Upload current PQRC mentor schedule from a csv file
        :return: None
        '''

        # ../RealData/MentorScheduleData.csv
        path = self.input_path("Input mentor schedule csv filename: ")

        cur = self.conn.cursor()

        # in case of re-upload, delete old data
        cur.execute(DROP_SCHEDULE)
        cur.execute(DROP_WORKS)
        cur.execute(CREATE_SCHEDULE)
        cur.execute(CREATE_WORKS)

        f = open(path)
        # throw away header line
        f.readline()

        lines = f.readlines()
        line_no = 0
        for line in lines:
            line_no += 1
            row = line.split(',')
            day_string = row[0][:3]
            time_string = row[1][:2] + ":00:00 EST"

            try:
                cur.execute(INSERT_SHIFT, (day_string, time_string))
            except psycopg2.Error:
                print("Unsuccessful Schedule Upload on line " + str(line_no) + ". Exiting.")
                f.close()
                exit(1)

            all_names_list = row[2:]
            names = list(
                    filter(lambda name: len(name) > 1, all_names_list)
            )

            for name in names:
                first_and_last = name.split(' ')
                first = first_and_last[0]
                last = ' '.join(first_and_last[1:]).strip()

                try:
                    cur.execute(
                        INSERT_WORKS, 
                        (first, last, day_string, time_string)
                    )
                except psycopg2.Error:
                    print("Unsuccessful Schedule Upload on line " + str(line_no) + ". Exiting.")
                    f.close()
                    exit(1)

        self.conn.commit()

        print("Mentor Schedule Upload Successful")
        f.close()

    def upload_mentor_coverage(self):
        '''
        Upload PQRC mentor course and software coverage data from a csv file
        :return: None
        '''

        # path = '../RealData/MentorCoverageData.csv'
        path = self.input_path("Input mentor coverage csv filename: ")

        f = open(path)
        # throw away header line
        first_line = f.readline().split(',')
        first_line_list = []
        for item in first_line:
            first_line_list.append(item.strip())
   
        # find the index of 'tech 1', which indicates
        # where we split our line to switch from inserting
        # courses to softwares into our database
        try:
            loc = first_line_list.index('tech1')
        except ValueError:
            print("Bad csv file. Make sure header line contains the cell 'tech1'")
            exit(1)

        lines = f.readlines()
        # insert softwares and courses
        self.upload_materials(lines, loc)

        # insert coverage
        self.upload_coverage(lines, loc)

        print("Mentor Coverage Upload Successful")
        f.close()

    def upload_materials(self, lines, loc):
        '''
        Helper function for course and software coverage upload
        :return: None
        '''
        # separate courses and softwares
        courses = set()
        softwares = set()
        for line in lines:
            line_list = []
            for item in line.split(','):
                line_list.append(item.strip())

            c_partial = list(
                filter(lambda c_id: len(c_id) > 1, line_list[1:loc])
            )
            s_partial = list(
                filter(lambda s_name: len(s_name) > 1, line_list[loc:])
            )

            courses.update(c_partial)
            softwares.update(s_partial)


        self.upload_courses(courses)
        self.upload_softwares(softwares)

    def upload_courses(self, courses):
        '''
        Helper function for uploading materials
        :return: None
        '''
        cur = self.conn.cursor()

        # in case of re-upload, delete old data
        cur.execute(DROP_COURSES)
        cur.execute(CREATE_COURSES)

        for course in courses:
            args = (course,)

            try:
                cur.execute(INSERT_COURSE, args)
            except psycopg2.Error:
                print("Internal Error: Attempted to add duplicate course")
                exit(1)

        self.conn.commit()

    def upload_softwares(self, softwares):
        '''
        Helper function for uploading materials
        :return: None
        '''
        cur = self.conn.cursor()

        # in case of re-upload, delete old data
        cur.execute(DROP_SOFTWARES)
        cur.execute(CREATE_SOFTWARES)

        for software in softwares:
            args = (software,)

            try:
                cur.execute(INSERT_SOFTWARE, args)
            except psycopg2.Error:
                print("Internal Error: Attempted to add duplicate software")
                exit(1)

        self.conn.commit()

    def upload_coverage(self, lines, loc):
        '''
        Helper function for uploading coverage
        :return: None
        '''
        cur = self.conn.cursor()

        # in case of re-upload, delete old data
        cur.execute(DROP_TEACHES_COURSES)
        cur.execute(DROP_TEACHES_SOFTWARES)
        cur.execute(CREATE_TEACHES_COURSES)
        cur.execute(CREATE_TEACHES_SOFTWARES)

        line_no = 0
        for line in lines:
            line_no += 1
            line_list = []
            for item in line.split(','):
                line_list.append(item.strip())
            
            mentor = line_list[0].split(' ')
            m_first = mentor[0].strip()
            m_last = ' '.join(mentor[1:]).strip()
            
            courses = list(
                filter(lambda c_id: len(c_id) > 1, line_list[1:loc])
            )
            softwares = list(
                filter(lambda s_name: len(s_name) > 1, line_list[loc:])
            )

            for course in courses:
                args = (m_last, m_first, course)
                try:
                    cur.execute(INSERT_TEACHES_COURSES, args)
                except psycopg2.Error:
                    print("Unsuccessful Coverage Upload on line " + str(line_no) + ". Exiting.")
                    exit(1)

            for software in softwares:
                args = (m_last, m_first, software)
                try:
                    cur.execute(INSERT_TEACHES_SOFTWARES, args)
                except psycopg2.Error:
                    print("Unsuccessful Coverage Upload on line " + str(line_no) + ". Exiting.")
                    exit(1)

            self.conn.commit()


    def generate_course_coverage(self):
        """
        Generate course coverage information for all courses 
        :return: None
        """

        print("Generating Course Coverage ... ")
        
        cur = self.conn.cursor()
        cur.execute(FIND_CLASSES)

        courses = [row[0] for row in cur]
        courses.sort()

        # output coverage for each class
        for course in courses:
            coverage_map = get_course_coverage_map(self.conn, course)
            output = coverage_output(coverage_map)

            print(course)
            for row in output:
                print(''.join(row))

            print('\n')

    def generate_software_coverage(self):
        """
        Generate software coverage information for all courses 
        :return: None
        """

        print("Generating Software Coverage ... ")
        
        cur = self.conn.cursor()
        cur.execute(FIND_SOFTWARES)

        softwares = [row[0] for row in cur]
        softwares.sort()

        # output coverage for each class
        for software in softwares:
            coverage_map = get_software_coverage_map(self.conn, software)
            output = coverage_output(coverage_map)

            print(software)
            for row in output:
                print(''.join(row))

            print('\n')

    def execute(self, opt):
        """
        Execute the menu option provided by the user
        """
        if opt not in self.valid_opts:
            raise ValueError("Invalid option passed to execute: " + opt)

        opt_map = {
            '1': self.upload_mentor_roster,
            '2': self.upload_mentor_schedule,
            '3': self.upload_mentor_coverage,
            '4': self.generate_course_coverage,
            '5': self.generate_software_coverage,
            'q': exit,
            'Q': exit
        }

        opt_map[opt]()