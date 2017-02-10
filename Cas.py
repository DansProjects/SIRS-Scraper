import requests
import lxml.html


class Cas:

    __netid = ""
    __password = ""
    __cas_login_url = ""
    __app_login_url = ""

    def __init__(self, netid, password, cas_login, app_login):
        self.__username = netid
        self.__password = password
        self.__cas_login_url = cas_login
        self.__app_login_url = app_login

    def cas_login(self):

        params = {'service': self.__app_login_url}

        # Start session and get login form.
        session = requests.session()
        login = session.get(self.__cas_login_url, params=params)

        # Get the hidden elements and put them in our form.
        login_html = lxml.html.fromstring(login.text)
        hidden_elements = login_html.xpath('//form//input[@type="hidden"]')
        form = {x.attrib['name']: x.attrib['value'] for x in hidden_elements}

        # "Fill out" the form.
        form['username'] = self.__username
        form['password'] = self.__password

        # Finally, login and return the session.
        response = session.post(self.__cas_login_url, data=form, params=params)

        return response.text
