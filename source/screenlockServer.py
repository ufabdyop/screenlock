import sys, os, urllib2, screenlockConfig, screenlockController, version, json, log, childController
from flask import Flask, request, Response, render_template
from urlparse import urlparse
from functools import wraps
from OpenSSL import SSL
from datetime import datetime
import pprint, logging
from rocket import Rocket

class screenlockFlaskServer(object):
    def __init__(self):
        self.config = screenlockConfig.SLConfig()
        self.port = int(self.config.get('port'))
        self.app = Flask(__name__, static_folder='static', static_path='/static', static_url_path='/static')
        self.app.debug = False
        self.logger = logging.getLogger('screenlockServer')
        self.server = None

        rocketlog = logging.getLogger('Rocket')
        rocketlog.setLevel(logging.INFO)

        self.ssl_context = None
        try:
            ssl_cert = self.config.get('cert')
            ssl_key = self.config.get('key')
            if ssl_cert and ssl_key:
                self.ssl_context = ('cert.pem', 'key.pem')
        except:
            pass


        self.setup_routes()
        self.lockController = screenlockController.SLController()
        self.childController = childController.child_controller()

    def run(self):
        #check if we should lock on start
        lock = self.config.get('lock_on_start', True)
        if (lock == 'no') or (lock == '0') or (lock == 0) or (lock == 'false'):
            lock = False

        if lock:
            self.lock_screen()
        interfaces = ("0.0.0.0", self.port)

        if self.ssl_context:
            interfaces = [('127.0.0.1', 80),
             ('0.0.0.0', self.port, self.ssl_context[1], self.ssl_context[0])]

        self.server = Rocket(interfaces, 'wsgi', {"wsgi_app": self.app})
        self.server.start(background=False)

    ########### AUTH HANDLING ############
    def check_auth(self, username, password):
        """This function is called to check if a username /
        password combination is valid.
        """
        return username == 'admin' and \
               self.config.passwordCheck(password,'web_password')

    def authenticate(self):
        """Sends a 401 response that enables basic auth"""
        return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

    def passwordError(self):
        """Sends a 401 response"""
        return Response(
        'Error, password need to be set!', 401,
        {'WWW-Authenticate': 'Basic realm="Password needs to be Set"'})

    def requires_auth(self, f):
        try:
            password = self.config.get('web_password')
            if password == '':
                raise ValueError("The password has not been set.")
        except ValueError:
            return self.passwordError

        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not self.check_auth(auth.username, auth.password):
                return self.authenticate()
            return f(*args, **kwargs)
        return decorated
    ########### END AUTH HANDLING ############

    ########### HTTP ENDPOINT METHODS ############
    def lock_or_unlock_screen(self):
        parseResult = urlparse(request.url)
        netloc = parseResult[1]
        url = request.url
        html ='<html><head><title>ScreenLock</title></head><body>'
        if self.lockController.is_running():
            html = '<p><h2>Status: locked.</h2></p>'
            html += '<br/><form action="' +parseResult[0]+'://'+netloc +'/lock" method="POST"><input type="submit" name="submit" value="Lock the Screen" disabled></form>'
            html += '<br/><form action="'+parseResult[0]+'://'+netloc+'/unlock" method="POST"><input type="submit" name="submit" value="Unlock the Screen"></form>'
        else:
            html = '<p><h2>Status: unlocked.</h2></p>'
            html += '<br/><form action="' +parseResult[0]+'://'+netloc +'/lock" method="POST"><input type="submit" name="submit" value="Lock the Screen"></form>'
            html += '<br/><form action="'+parseResult[0]+'://'+netloc+'/unlock" method="POST"><input type="submit" name="submit" value="Unlock the Screen" disabled></form>'
        html += '</body></html>'
        return html

    def get_status(self):
        result = ''
        if self.lockController.is_running():
            result = json.dumps({"status": "locked"})
        else:
            result = json.dumps({"status": "unlocked"})
        return result

    def lock_screen(self):
        try:
            self.lockController.lock_screen()
            auth = request.authorization
            self.childController.lock_childs(auth.username, auth.password)
        except Exception as e:
            self.logger.error("ScreenLockServer error locking screen: %s" % e)
        return json.dumps({"status": "locked"})

    def unlock_screen(self):
        try:
            self.lockController.unlock_screen()
            auth = request.authorization
            self.childController.unlock_childs(auth.username, auth.password)
        except Exception as e:
            self.logger.error("ScreenLockServer error unlocking screen: %s" % e)
        return json.dumps({"status": "unlocked"})
    ########### END HTTP ENDPOINT METHODS ############

    def setup_routes(self):
        @self.app.route('/admin', methods=['GET', 'POST'])
        @self.requires_auth
        def admin():
            return self.lock_or_unlock_screen()

        @self.app.route('/status', methods=['GET', 'POST'])
        @self.requires_auth
        def status():
            return self.get_status()

        @self.app.route('/lock', methods=['POST'])
        @self.requires_auth
        def lock():
            return self.lock_screen()

        @self.app.route('/unlock', methods=['POST'])
        @self.requires_auth
        def unlock():
            return self.unlock_screen()

        #Alias for unlock
        @self.app.route('/enable', methods=['POST'])
        @self.requires_auth
        def enable():
            return unlock()

        #Alias for lock
        @self.app.route('/disable', methods=['POST'])
        @self.requires_auth
        def disable():
            return lock()

        #Alias for status
        @self.app.route('/sense', methods=['POST', 'GET'])
        @self.requires_auth
        def sense():
            return status()


        @self.app.route('/static', methods=['GET'])
        @self.app.route('/static/', methods=['GET'])
        @self.app.route('/', methods=['GET'])
        def serve_static_index():
            self.logger.debug('static asset')
            return self.app.send_static_file('index.html')

        @self.app.route('/swagger.yaml', methods=['GET'])
        def swagger():
            self.logger.debug('swagger yaml')
            buffer = render_template('swagger.yaml',
                                     host=request.host)
            return buffer


        @self.app.route('/version')
        def versionPath():
            return json.dumps({"version": version.VERSION})


if __name__ == '__main__':
    PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(PATH)

    log.initialize_logging("screenlockServer")

    server = screenlockFlaskServer()
    server.run()
