from lxml import html
import xml.etree.ElementTree as et
import re
from bs4 import BeautifulSoup

class sirsParse:

    def get_html(self, data):
        """Returns list of tables, each representing one evaluation"""

        evaluations = html.fromstring(data)
        evaluations = evaluations.xpath('//table')

        return evaluations

    def get_data_source(self, table):
        """Returns format that data was collected from ex: Scannable Paper Form, Online Survey"""

        try:
            source_string = (et.tostring(table.xpath('.//caption')[0])).decode('utf-8')
            source = re.findall(r'\(([^()]+)\)', source_string)

            return source[0]

        except IndexError:
            print("Failed at get_data_source")
            return False

    def get_instructor_name(self, row):
        """Returns last name of instructor, located in first row of table in only strong tag"""

        try:
            instructor = row.xpath('.//strong/text()')[0]

            return instructor.strip()

        except IndexError:
            print("Failed at get_instructor_name")
            return False

    def get_course_name(self, row):
        """Returns name of course, located in first row of table in only q tag"""

        try:
            course_name = row.xpath('.//q/text()')[0]
            return course_name

        except IndexError:
            print("Failed at get_course_name")
            return False

    def get_full_semester(self, row):
        """Returns semester of course, located in first row of table """

        try:
            row_text = et.tostring(row).decode('utf-8')
            search = re.findall(r'(?i)(?:Spring|Fall|Summer) (?:[\s]*[\d]*)', row_text)

            return search[0]

        except IndexError:
            print("Failed at get_semester")
            return False

    def get_reg_index(self, row):
        """Returns regindex of course, located in first row of table"""

        try:
            row_text = et.tostring(row).decode('utf-8')
            search = re.findall(r'index\s#[\d]*', row_text)
            search = re.sub('[^0-9]', '', search[0])
            return search

        except IndexError:
            print("Failed at get_reg_index")
            return False

    def get_course_code(self, row):
        """Returns course code of course, located in first row of table"""

        try:
            row_text = et.tostring(row).decode('utf-8')
            search = re.findall(r'(\b([A-Za-z0-9]+:){3}[A-Za-z0-9]+\b(?=\s))', row_text)

            if len(search[0]) > 1:
                return search[0][0]
            else:
                return search[0]

        except:
            print("Failed at get_course_code")
            return False

    def get_num_enrollments(self, row):
        """Returns number of enrollments of course, located in first row of table"""

        try:
            row_text = et.tostring(row).decode('utf-8')
            search = re.findall(r'(?:Enrollment.*?)(\d+)', row_text)

            return search[0]

        except IndexError:
            print("Failed at get_num_enrollments")
            return False

    def get_num_responses(self, row):
        """Returns number of enrollments of course, located in first row of table"""

        try:
            row_text = et.tostring(row).decode('utf-8')
            search = re.findall(r'(?:Responses.*?)(\d+)', row_text)

            return search[0]

        except IndexError:
            print("Failed at get_num_responses")
            return False

    def get_year(self, semester):
        """Returns the year from the semester string ex: Spring 2017"""

        try:
            year = re.findall(r'[\d]+', semester)

            return year[0]

        except IndexError:
            print("Failed at get_year")
            return False

    def get_semester(self, semester):
        """Returns the semester (Spring) from the semester string ex: Spring 2017"""

        try:
            semester = re.findall(r'[A-z]+', semester)

            return semester[0]

        except IndexError:
            print("Failed at get_semester")
            return False

    def get_school(self,course_code):
        """Return the school id from course code"""
        course_code = course_code.split(':')
        try:
            return course_code[0]  # school id are the numbers before first :

        except IndexError:
            print("Failed at get_school")
            return False

    def get_department(self,course_code):
        """Return the department id from course code"""
        course_code = course_code.split(':')
        try:
            return course_code[1]  # school id are the numbers before second :
        except IndexError:
            print("Failed at get_department")
            return False

    def get_course(self,course_code):
        """Return the course id from course code"""
        course_code = course_code.split(':')
        try:
            return course_code[2]  # course id are the numbers before third :

        except IndexError:
            print("Failed at get_course")
            return False

    def get_section(self,course_code):
        """Return the secion id from course code"""
        course_code = course_code.split(':')
        try:
            return course_code[3]  # section id are the numbers after third :

        except IndexError:
            print("Failed at get_section")
            return False

    def get_eval_rows(self, table):
        """Retrieves questions and its response (row) given an evaluation"""

        evaluation_data = {}

        try:
            table_text = et.tostring(table).decode('utf-8')
            soup = BeautifulSoup(table_text, 'html.parser')
            tbody_text = soup.find_all('tbody') # first tbody is standard university questions
                                                # second tbody, if exists, are instructor / dept added

            question_inc = 0;

            for i, tbody in enumerate(tbody_text):

                questions = tbody.find_all(text=re.compile(r'[\d]+[.][\s]'))

                for ind, question in enumerate(questions):

                    eval_data = question.parent.parent
                    question_text = eval_data.find_all('td', {'class':"qText"})
                    question_text = question_text[0].contents[0]
                    question_text = re.sub(r'\d+[\.]', '', question_text)
                    question_text = question_text.strip()

                    question_data = {}
                    question_data["question_text"] = question_text

                    if i == 0:
                        question_data["question_type"] = "university"
                    else:
                        question_data["question_type"] = "instructor"

                    response_data = {}

                    response_text = eval_data.find_all('td', {'class':['mono']})
                    for indx, response in enumerate(response_text):
                        response_data[indx] = response.text
                        if indx == 5:
                            break #not interested in averages, which are after 6th data point

                    question_data["response"] = response_data
                    evaluation_data[question_inc] = question_data
                    question_inc += 1

            return evaluation_data

        except IndexError:
            print("Failed at get_num_responses")
            return False
