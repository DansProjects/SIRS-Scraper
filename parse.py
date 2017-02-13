from lxml import html
import xml.etree.ElementTree as et
import re
from bs4 import BeautifulSoup

class parse:

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

            return source

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

    def get_semester(self, row):
        """Returns semester of course, located in first row of table """

        try:
            row_text = et.tostring(row).decode('utf-8')
            search = re.findall(r'(?:Spring|Fall|Summer) (?:[\s]*[\d]*)', row_text)

            return search[0]

        except IndexError:
            print("Failed at get_semester")
            return False

    def get_reg_index(self, row):
        """Returns regindex of course, located in first row of table"""

        try:
            row_text = et.tostring(row).decode('utf-8')
            search = re.findall(r'index\s#[\d]*', row_text)

            return search[0]

        except IndexError:
            print("Failed at get_reg_index")
            return False

    def get_course_code(self, row):
        """Returns course code of course, located in first row of table"""

        try:
            row_text = et.tostring(row).decode('utf-8')
            #TODO currently taking first course code - need to deal with cross lists
            search = re.findall(r'([\d]+:[\d]+:[\d]+:*.[^\s])', row_text)

            return search[0]

        except IndexError:
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

    def get_eval_rows(self, table):
        """Retrieves questions and its response (row) given an evaluation"""

        try:
            table_text = et.tostring(table).decode('utf-8')
            soup = BeautifulSoup(table_text, 'html.parser')

            questions = soup.find_all(text=re.compile(r'[\d+][.][\s]'))
            print(questions)
            eval_data = questions[0].parent.parent
            print(eval_data)

        except IndexError:
            print("Failed at get_num_responses")
        return False
