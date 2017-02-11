import configparser

from cas import Cas

cp = configparser.RawConfigParser()
configFilePath = 'config.txt'
cp.read(configFilePath)

cas_login_url = cp.get("cas-config", "cas_login_url")
app_login_url = cp.get("cas-config", "app_login_url")
netid = cp.get("cas-config", "netid")
password = cp.get("cas-config", "password")

cas = Cas(netid, password, cas_login_url, app_login_url)

result = cas.cas_login()

#with open("Output.html", "w") as text_file:
#    text_file.write(result)
