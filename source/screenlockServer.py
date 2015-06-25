import os, psutil, wx, win32gui, win32con, time, thread, win32process, subprocess, ConfigParser, signal, pythoncom, pyHook, threading, win32api, zope.interface
from twisted.internet import protocol, reactor, endpoints
import screenlockConfig, screenlockController
from flask import Flask, request, Response
from functools import wraps

app = Flask(__name__)
config = screenlockConfig.SLConfig()
lockController = screenlockController.SLController()

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and config.passwordCheck(password)

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
        password = config.get('admin_override')
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
    
@app.route('/status', methods=['GET', 'POST'])
@requires_auth
def lock_or_unlock_Screen():
    global lockController
    url = request.url
    html =''
    if request.method == 'POST':
        if request.form['submit'] == 'Unlock the Screen':
            lockController.unlock_screen()
        elif request.form['submit'] == 'Lock the Screen':
            lockController.lock_screen()
    if lockController.is_running():
        html = '<p><h2>Screen is locked.</h2></p>'
        html += '<br/><form action="' +url +'" method="POST"><input type="submit" name="submit" value="Lock the Screen" disabled></form>'
        html += '<br/><form action="'+url+'" method="POST"><input type="submit" name="submit" value="Unlock the Screen"></form>'
    else:
        html = '<p><h2>Screen is unlocked.</h2></p>' 
        html += '<br/><form action="' +url +'" method="POST"><input type="submit" name="submit" value="Lock the Screen"></form>'
        html += '<br/><form action="'+url+'" method="POST"><input type="submit" name="submit" value="Unlock the Screen" disabled></form>'
    return html

if __name__ == '__main__':
    portNumber = config.get('port')
    lockController.lock_screen()
    app.run(host='0.0.0.0', port = int(portNumber))
