from sirsParse import sirsParse
from database import Question, Course, Answer, Database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json


def add_question(sess, q):
    """Adds a given question if it does not already exist"""
    print(q.question_text)
    qtext = q.question_text
    qtext = qtext.encode('utf-8')
    instance = sess.query(Question).filter_by(question_text=qtext).first()

    if not instance:
        sess.add(q)
        sess.commit()
        return True
    else:
        return False

db_connect = Database()
connection_string = db_connect.connect()

engine = create_engine(connection_string)

session = sessionmaker()
session.configure(bind=engine)

file = open("scraped/example-evaluations-year-semester-school-department.html", "r")
data = file.read()

parser = sirsParse()
evaluations = parser.get_html(data)

for evaluation in evaluations:

    evaluation_data = {}
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # course info located in first row, first td
    row = evaluation.xpath('.//tr/td')[0]

    evaluation_data["source"] = parser.get_data_source(evaluation)
    evaluation_data["instructor"] = parser.get_instructor_name(row)
    evaluation_data["course_name"] = parser.get_course_name(row)
    evaluation_data["semester_full"] = parser.get_full_semester(row)
    evaluation_data["semester"] = parser.get_semester(evaluation_data["semester_full"])
    evaluation_data["year"] = parser.get_year(evaluation_data["semester_full"])
    evaluation_data["reg_index"] = parser.get_reg_index(row)
    evaluation_data["course_code"] = parser.get_course_code(row)
    evaluation_data['school'] = parser.get_school(evaluation_data["course_code"])
    evaluation_data['department'] = parser.get_department(evaluation_data["course_code"])
    evaluation_data['course'] = parser.get_course(evaluation_data["course_code"])
    evaluation_data['section'] = parser.get_section(evaluation_data["course_code"])
    evaluation_data["enrollments"] = parser.get_num_enrollments(row)
    evaluation_data["responses"] = parser.get_num_responses(row)
    evals = parser.get_eval_rows(evaluation)
    parser.get_school(evaluation_data["course_code"])

    course_session = session()
    course = Course(course_name=evaluation_data["course_name"], year=evaluation_data["year"],
                    semester=evaluation_data["semester"], school=evaluation_data['school'],
                    department=evaluation_data['department'], course=evaluation_data['course'],
                    section=evaluation_data['section'], source=evaluation_data['source'],
                    enrollments=evaluation_data['enrollments'], responses=evaluation_data['responses'],
                    created_at=now
        )

    #get_or_create_course(course_session, course)
    #course_session.add(course)
    #course_session.commit()
    #print(course.id)
    #print(evals)

    evaluation_data["questions"] = evals
    evals_json = json.dumps(evaluation_data)
    evals_json = json.loads(evals_json)
    #print(evals_json)

    for e in evals_json['questions']:
        #print(evals_json['questions'][e])
        q_text = evals_json['questions'][e]['question_text']
        q_type = evals_json['questions'][e]['question_type']

        responses = evals_json['questions'][e]['response']
        question_session = session()
        question = Question(question_text=q_text, question_type=q_type, created_at=now)
        question_session.add(question)
        question_session.commit()
        #print(q_type)
        #add_question(question_session,question)

        #for inc in q:
            #print(inc)

    #print(json.dumps(evals_json, indent=4, sort_keys=True))
    #break

