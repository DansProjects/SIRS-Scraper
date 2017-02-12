import configparser
import json
import os
import errno
import time
from random import randint
from time import sleep

from sirsScrape import sirsScrape

def archive(html, year, semester, school, department):
    """Saves evaluation data onto disk"""

    directory_path = "scraped/"+format(year)+"/"+format(semester)+"/"+format(school)

    try:
        os.makedirs(directory_path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    file_name = "evaluations-"+format(year)+"-"+format(semester)+"-"+format(school)+"-"+format(department)+".html"
    file_path = directory_path+"/"+file_name

    try:
        with open(file_path, "w") as html_file:
            html_file.write(html)
    except IOError:
        print("Could not write to file: ", format(file_name))


cp = configparser.RawConfigParser()
configFilePath = 'config.txt'
cp.read(configFilePath)

cas_login_url = cp.get("cas-config", "cas_login_url")
app_login_url = cp.get("cas-config", "app_login_url")
netid = cp.get("cas-config", "netid")
password = cp.get("cas-config", "password")

years = ( 2014, 2015, 2016)

semesters = ("Spring", "Fall")

cas_session = sirsScrape(netid, password, cas_login_url, app_login_url)

cas_session.cas_login()

start_time = time.time()

for year in years:
    print(year,end=" ")
    for semester in semesters:
        print(semester)
        if (time.time() - start_time) > 3600:
            cas_session.cas_login() #refresh session every hour
            start_time = time.time()

        schools_json = cas_session.get_schools(year,semester)
        schools_json = json.loads(schools_json)

        for school in schools_json["schools"]:
            print(school[0]+' - '+school[1])
            #if int(school[0]) > 25:
            departments_json = cas_session.get_departments(year, semester, school[0])
            departments_json = json.loads(departments_json)

            for department in departments_json["depts"]:
                #if int(department) > 553:
                print("\t Department: "+department)
                evaluations_html = cas_session.get_evaluations(year, semester, school[0], department)
                if not evaluations_html:
                    continue
                else:
                    archive(evaluations_html, year, semester, school[0], department)
                    sleep(randint(2, 7))
                #break
            #break

            # end department
        # end school
    # end semester
#end year




