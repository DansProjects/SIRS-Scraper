from sirsParse import sirsParse
from database import Question, Course, Answer, Database, DataSource
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
import os
from collections import OrderedDict

def add_question(sess, q):
    """Adds a given question if it does not already exist, returns id of question if it does"""
    qtext = q.question_text
    instance = sess.query(Question).filter_by(question_text=qtext).first()

    if not instance:
        sess.add(q)
        sess.commit()
        return q.id
    else:
        return instance.id

def add_course(sess, c):
    """Adds a given course if it does not already exist, returns -1 if it does"""

    instance = sess.query(Course).filter(and_(Course.year==c.year, Course.semester==c.semester, Course.school==c.school, Course.department==c.department,
                                             Course.course==c.course, Course.section == c.section, Course.regindex == c.regindex)).first()
    if not instance:
        sess.add(c)
        sess.commit()
        return c.id
    else:
        return -1

def add_answer(sess, a):
    """Adds a given answer if it does not already exist, returns id if answer if it does"""

    instance = sess.query(Answer).filter(and_(Answer.question_id==a.question_id, Answer.course_id==a.course_id)).first()
    if not instance:
        sess.add(a)
        sess.commit()
        return a.id
    else:
        return instance.id

def add_file(sess, f):
    """Adds a file answer if it does not already exist, returns -1 if does"""

    instance = sess.query(DataSource).filter_by(file_name=f.file_name).first()
    if not instance:
        sess.add(f)
        sess.commit()
        return f

    return instance

def set_finished(sess, f):
    """Sets file completion status and time"""

    instance = sess.query(DataSource).filter(DataSource.id == f.id).first()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if instance:
        instance.status = "finished"
        instance.updated_at = now
        sess.commit()
        return True

    return False


def insert_data(evaluations):

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
                        section=evaluation_data['section'], regindex=evaluation_data["reg_index"],
                        source=evaluation_data['source'],enrollments=evaluation_data['enrollments'],
                        responses=evaluation_data['responses'],instructor=evaluation_data["instructor"],
                        created_at=now
            )
        course_session.close()
        course_id = add_course(course_session, course)
        if course_id == -1:
            print("Skipping course [{}] - {} - {}".format(course_id, evaluation_data["course_name"],
                                                       evaluation_data["instructor"]))
        else:
            print("Added course [{}] - {} - {}".format(course_id,evaluation_data["course_name"],
                                                       evaluation_data["instructor"]))

            evaluation_data["questions"] = evals
            #print("Instructor {} : {}".format(evaluation_data["instructor"], evals))
            evals_json = json.dumps(evaluation_data)
            evals_json = json.loads(evals_json)

            for e in evals_json['questions']:
                #print(evals_json['questions'][e])
                q_text = evals_json['questions'][e]['question_text']
                q_type = evals_json['questions'][e]['question_type']

                responses = evals_json['questions'][e]['response']

                question_session = session()
                question = Question(question_text=bytearray(q_text,'utf-8'), question_type=q_type, created_at=now)
                q_id = add_question(question_session, question)
                question_session.close()

                answer_session = session()
                rate_1,rate_2,rate_3,rate_4,rate_5,blank = 0,0,0,0,0,0
                responses = OrderedDict(sorted(responses.items()))

                for indx, inc in enumerate(responses):
                    if indx == 0:
                        rate_1 = responses[inc]
                    elif indx ==1:
                        rate_2 = responses[inc]
                    elif indx == 2:
                        rate_3 = responses[inc]
                    elif indx == 3:
                        rate_4 = responses[inc]
                    elif indx == 4:
                        rate_5 = responses[inc]
                    elif indx == 5:
                        blank = responses[inc]

                answer = Answer(course_id=course_id, question_id=q_id, rating_1=rate_1, rating_2=rate_2,
                                rating_3=rate_3, rating_4=rate_4, rating_5=rate_5, blank=blank, created_at=now)

                add_answer(answer_session, answer)
                answer_session.close()

            #print(json.dumps(evals_json, indent=4, sort_keys=True))


db_connect = Database()
connection_string = db_connect.connect()

engine = create_engine(connection_string, convert_unicode=True,
pool_size=20, max_overflow=100)

session = sessionmaker()
session.configure(bind=engine)

parser = sirsParse()
for root, dirs, files in os.walk("scraped/2003"):
    for file in files:
        if file.endswith(".html"):

            file_session = session()
            file_path = (os.path.join(root, file))

            print("Parsing file: "+file_path)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data_source = DataSource(file_name = file_path, status="started", created_at=now)
            file_instance = add_file(file_session, data_source)

            if file_instance.status == "started":
                file = open(file_path, encoding="ISO-8859-1")
                data = file.read()
                evaluations = parser.get_html(data)
                insert_data(evaluations)
                set_finished(file_session, file_instance)

            else:
                print("Skipping finished file: "+file_path)

            file_session.close()

print("Finished!")

