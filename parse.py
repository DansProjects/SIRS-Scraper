from sirsParse import sirsParse
import xml.etree.ElementTree as et

file = open("Output.html", "r")
data = file.read()

parser = sirsParse()
evaluations = parser.get_html(data)

for evaluation in evaluations:
    # course info located in first row, first td
    row = evaluation.xpath('.//tr/td')[0]

    source = parser.get_data_source(evaluation)
    instructor = parser.get_instructor_name(row)
    course_name = parser.get_course_name(row)
    semester = parser.get_semester(row)
    reg_index = parser.get_reg_index(row)
    course_code = parser.get_course_code(row)
    enrollments = parser.get_num_enrollments(row)
    responses = parser.get_num_responses(row)
    evals = parser.get_eval_rows(evaluation)

    print(course_name+"-"+instructor)
    break
