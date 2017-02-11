import requests
import lxml.html


class sirsScrape:

    __netid = ""
    __password = ""
    __cas_login_url = ""
    __app_login_url = ""
    __session = ""
    __sirs_base_url = "https://sirs.ctaar.rutgers.edu"

    def __init__(self, netid, password, cas_login, app_login):
        self.__username = netid
        self.__password = password
        self.__cas_login_url = cas_login
        self.__app_login_url = app_login

    def cas_login(self):

        """Logs into SIRS via CAS and sets session for later requests"""

        params = {'service': self.__app_login_url}

        # Start session and get login form.
        session = requests.session()
        login = session.get(self.__cas_login_url, params=params)

        # Simulate browser, Chrome 56.0
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        # Get the hidden elements and put them in our form.
        login_html = lxml.html.fromstring(login.text)
        hidden_elements = login_html.xpath('//form//input[@type="hidden"]')
        form = {x.attrib['name']: x.attrib['value'] for x in hidden_elements}

        # "Fill out" the form.
        form['username'] = self.__username
        form['password'] = self.__password

        # Finally, login and return the session.
        response = session.post(self.__cas_login_url, data=form, params=params, headers=headers)
        if response:
            self.__session = session
            return True
        else:
            return False

    def get_schools(self, year, semester):

        """Grab list of schools for given year
            URL format: https://sirs.ctaar.rutgers.edu/courseFilter.php?survey[semester]=Spring&survey[year]=2015&mode=course
            Returns json
        """

        url = "{sirs_base_url}/courseFilter.php?survey[semester]={semester}&survey[year]={year}&mode=course"\
            .format(sirs_base_url = self.__sirs_base_url, semester = semester, year = year)

        schools = self.__session.get(url)

        return schools.text

    def get_departments(self, year, semester, school):

        """Grabs list of departments given school id
            URL format: https://sirs.ctaar.rutgers.edu/courseFilter.php?survey[semester]=Spring&survey[year]=2016
            &survey[school]=15&survey[dept]=&survey[course]=&mode=course
            Returns json
        """
        url = "{sirs_base_url}/courseFilter.php?survey[semester]={semester}&survey[year]={year}&survey[school]={school}&mode=course"\
            .format(sirs_base_url = self.__sirs_base_url, semester = semester, year = year, school = school)

        subjects = self.__session.get(url)

        return subjects.text