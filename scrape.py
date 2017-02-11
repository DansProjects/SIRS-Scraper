import configparser
import json

from sirsScrape import sirsScrape

cp = configparser.RawConfigParser()
configFilePath = 'config.txt'
cp.read(configFilePath)

cas_login_url = cp.get("cas-config", "cas_login_url")
app_login_url = cp.get("cas-config", "app_login_url")
netid = cp.get("cas-config", "netid")
password = cp.get("cas-config", "password")

years = ( 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009,
          2010, 2011, 2012, 2013, 2014, 2016)

cas_session = sirsScrape(netid, password, cas_login_url, app_login_url)

cas_session.cas_login()

year = years[10]
semester = "Spring"
schools_json = cas_session.get_schools(year,semester)
schools_json = json.loads(schools_json)

for school in schools_json["schools"]:
    print(school[0]+' - '+school[1])
    departments_json = cas_session.get_departments(year, semester, school[0])
    departments_json = json.loads(departments_json)

    for department in departments_json["depts"]:
        print("\t Department: "+department)

    break;

#with open("Output.html", "w") as text_file:
#    text_file.write(result)
