import os, psutil, wx, win32gui, win32con, time, thread, win32process, subprocess, ConfigParser, signal, pythoncom, pyHook, threading
import screenlockConfig
from flask import Flask, request, Response
from functools import wraps

app = Flask(__name__)
config = screenlockConfig.SLConfig()

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
    
def IsRunning(appname):    
    for p in psutil.process_iter():
        try:
            if p.name == appname:
                return True
        except psutil.Error:
            pass
    return False
      
                 
@app.route('/status', methods=['GET', 'POST'])
@requires_auth
def lock_or_unlock_Screen():
    url = request.url
    str =''
    if request.method == 'POST':
        if request.form['submit'] == 'Unlock the Screen':
            path = config.get('unlock')
            os.startfile(path)
            return 'Screen is unlocked.'
        elif request.form['submit'] == 'Lock the Screen':
            path = config.get('lock')
            os.startfile(path)
            return 'Screen is locked.'
    else:
        if IsRunning('screenlockApp.exe'):
            str = 'Screen is locked. <form action="'+url+'" method="POST"><input type="submit" name="submit" value="Unlock the Screen"></form>'
        else:
            str = 'Screen is unlocked. <form action="' +url +'" method="POST"><input type="submit" name="submit" value="Lock the Screen"></form>'
        return str

if __name__ == '__main__':
    portNumber = config.get('port')
    app.run(host='0.0.0.0', port = int(portNumber))
