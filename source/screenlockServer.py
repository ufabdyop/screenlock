import sys, os, urllib2, screenlockConfig, screenlockController, version, json, log
from flask import Flask, request, Response
from urlparse import urlparse
from functools import wraps
from OpenSSL import SSL
from datetime import datetime

PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(PATH)

app = Flask(__name__)
config = screenlockConfig.SLConfig()
lockController = screenlockController.SLController()
context = ('cert.pem', 'key.pem')
global logFile
logFile = open(log.create_log_file('screenlockServer'), "a")
errorLogFile = open(log.create_log_file('ErrorscreenlockServer'), "a")
sys.stdout = logFile
sys.stderr = errorLogFile

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and config.passwordCheck(password,'web_password')

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})
    
def passwordError():
    """Sends a 401 response"""
    return Response(
    'Error, password need to be set!', 401,
    {'WWW-Authenticate': 'Basic realm="Password needs to be Set"'})

def requires_auth(f):
    try:
        password = config.get('web_password')
        if password == '':
            raise ValueError("The password has not been set.")
    except ValueError:
        return passwordError
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
    
@app.route('/admin', methods=['GET', 'POST'])
@requires_auth
def lock_or_unlock_Screen():
    parseResult = urlparse(request.url)
    netloc = parseResult[1]
    url = request.url
    html ='<html><head><title>ScreenLock</title></head><body>'
    if lockController.is_running():
        html = '<p><h2>Status: locked.</h2></p>'
        html += '<br/><form action="' +parseResult[0]+'://'+netloc +'/lock" method="POST"><input type="submit" name="submit" value="Lock the Screen" disabled></form>'
        html += '<br/><form action="'+parseResult[0]+'://'+netloc+'/unlock" method="POST"><input type="submit" name="submit" value="Unlock the Screen"></form>'
    else:
        html = '<p><h2>Status: unlocked.</h2></p>'
        html += '<br/><form action="' +parseResult[0]+'://'+netloc +'/lock" method="POST"><input type="submit" name="submit" value="Lock the Screen"></form>'
        html += '<br/><form action="'+parseResult[0]+'://'+netloc+'/unlock" method="POST"><input type="submit" name="submit" value="Unlock the Screen" disabled></form>'
    html += '</body></html>'
    return html

@app.route('/status', methods=['GET', 'POST'])
@requires_auth   
def get_status():
    result = ''
    if lockController.is_running():
        result = json.dumps({"status": "locked"})
    else:
        result = json.dumps({"status": "unlocked"})
    return result
 
@app.route('/lock', methods=['POST'])
@requires_auth   
def lock_Screen():
    global lockController
    try:
        lockController.lock_screen()
    except Exception,e:
        print (str(datetime.now()) + "  ScreenLockServer: " + str(e))
    return json.dumps({"status": "locked"})

@app.route('/unlock', methods=['POST'])
@requires_auth   
def unlock_Screen():
    global lockController
    try:
        lockController.unlock_screen()
    except Exception,e:
        print (str(datetime.now()) + "  ScreenLockServer: " + str(e))
    return json.dumps({"status": "unlocked"})

@app.route('/enable', methods=['POST'])
@requires_auth
def enable_Screen():
    return unlock_Screen()

@app.route('/disable', methods=['POST'])
@requires_auth
def disable_Screen():
    return lock_Screen()

@app.route('/sense', methods=['POST', 'GET'])
@requires_auth
def sense_status():
    return get_status()

@app.route('/version')
def get_Version():
    return json.dumps({"version": version.VERSION})

if __name__ == '__main__':
    portNumber = config.get('port')
    lockController.lock_screen()
    app.run(host='0.0.0.0', port = int(portNumber), ssl_context=context)
    global logFile
    logFile.close()
    global errorLogFile
    errorLogFile.close()
