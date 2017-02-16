from sirsParse import sirsParse
import xml.etree.ElementTree as et
import json

file = open("scraped/example-evaluations-year-semester-school-department.html", "r")
data = file.read()

parser = sirsParse()
evaluations = parser.get_html(data)

for evaluation in evaluations:

    evaluation_data = {}

    # course info located in first row, first td
    row = evaluation.xpath('.//tr/td')[0]

    evaluation_data["source"] = parser.get_data_source(evaluation)
    evaluation_data["instructor"] = parser.get_instructor_name(row)
    evaluation_data["course_name"] = parser.get_course_name(row)
    evaluation_data["semester"] = parser.get_semester(row)
    evaluation_data["reg_index"] = parser.get_reg_index(row)
    evaluation_data["course_code"] = parser.get_course_code(row)
    evaluation_data["enrollments"] = parser.get_num_enrollments(row)
    evaluation_data["responses"] = parser.get_num_responses(row)
    evals = parser.get_eval_rows(evaluation)

    evaluation_data["questions"] = evals
    evals_json = json.dumps(evaluation_data)
    evals_json = json.loads(evals_json)

    print(json.dumps(evals_json, indent=4, sort_keys=True))
    #break
