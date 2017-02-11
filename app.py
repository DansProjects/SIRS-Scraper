from parse import parse
import xml.etree.ElementTree as et

file = open("Output.html", "r")
data = file.read()

parse = parse()
evaluations = parse.get_html(data)

for evaluation in evaluations:
    # course info located in first row, first td
    row = evaluation.xpath('.//tr/td')[0]

    source = parse.get_data_source(evaluation)
    instructor = parse.get_instructor_name(row)
    course_name = parse.get_course_name(row)
    semester = parse.get_semester(row)
    reg_index = parse.get_reg_index(row)
    course_code = parse.get_course_code(row)
    enrollments = parse.get_num_enrollments(row)
    responses = parse.get_num_responses(row)

    print(course_name+"-"+instructor)
