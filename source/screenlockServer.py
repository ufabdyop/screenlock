import os, sys, psutil, wx, win32gui, win32con, time, thread, win32process, subprocess, ConfigParser, signal, pythoncom, pyHook, threading, win32api, zope.interface, urllib2
from twisted.internet import protocol, reactor, endpoints
import screenlockConfig, screenlockController, version
from flask import Flask, request, Response
from functools import wraps
from urlparse import urlparse
from OpenSSL import SSL
import json

app = Flask(__name__)
config = screenlockConfig.SLConfig()
lockController = screenlockController.SLController()
context = ('cert.pem', 'key.pem')

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
    
    
    html += '<br/><br/><form action="' + url +'" method = "POST"><table><tr><td>Enter Current Admin Password:</td><td><input type="password" name="current_pw" ></td></tr>' + \
    '<tr><td>Set New Admin Password:</td><td><input type="password" name="new_pw" ></td></tr><tr><td>Confirm New Admin Password:</td><td><input type="password" name="confirm_pw"></td></tr>'+ \
    '<tr><td colspan = "2" align =right><input type="submit" name="pw_submit" value="Submit"></td></tr></tabel></form>'
    if request.method == 'POST':
        oldPassword = request.form['current_pw']
        newPassword = request.form['new_pw']
        confirmPassword = request.form['confirm_pw']
        if config.passwordCheck(oldPassword, 'web_password') == False:
            html += '<br/><h2>Wrong Password!</h2>'         
        elif newPassword == "":
            html += '<br/><h2>Empty Password!</h2>'
        elif newPassword != confirmPassword:
            html += '<br/><h2>Password Mismatch!</h2>'
        else:
            config.writePassword(newPassword, 'web_password')
            html += '<br/><h2>Saved New Password</h2>'
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
def lock_Screen():
    global lockController
    try:
        lockController.lock_screen()
    except Exception,e:
        print str(e)
    return json.dumps('locked')

@app.route('/unlock', methods=['POST'])
def unlock_Screen():
    global lockController
    try:
        lockController.unlock_screen()
    except Exception,e:
            print str(e)
    return json.dumps("unlocked")
   
@app.route('/version')
def get_Version():
    return json.dumps({"version": version.VERSION})

if __name__ == '__main__':
    portNumber = config.get('port')
    lockController.lock_screen()
    app.run(host='0.0.0.0', port = int(portNumber), ssl_context=context)
