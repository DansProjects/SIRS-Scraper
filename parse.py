from sirsParse import sirsParse
import xml.etree.ElementTree as et
import json

file = open("scraped/example-evaluations-year-semester-school-department.html", "r")
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

    evals_json = json.dumps(evals)
    evals_json = json.loads(evals_json)

    print(course_name+"-"+instructor)
    print(json.dumps(evals_json, indent=4, sort_keys=True))
    break
