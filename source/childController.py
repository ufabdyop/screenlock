import logging, log, requests
from screenlockConfig import SLConfig
from requests.auth import HTTPBasicAuth

class child_controller(object):
    def __init__(self):
        log.initialize_logging("childController")
        self.logger = logging.getLogger("childController")
        self.config = SLConfig()



    def lock_childs(self, username, password):
        """Locks all of the child nodes with the provided hostnames/ips in the
            'config.ini' file. If there is not a hostname specified, skip to next one.
            If the schema or the port filed is left empty for the hostname, it will
            choose the defaults. (Defaults are 'https' for schema and '9092' for the
            port.

        Args:
            username: The username of the screenlock.
            password: The password of the screenlock.
        """

        # Gets the list of childs.
        childs = self.config.getFromSubHosts('names')
        # Gets the list of schemas.
        schemas = self.config.getFromSubHosts('schemas')
        # Gets the list of the ports.
        ports = self.config.getFromSubHosts('ports')

        length = len(childs)

        # Makes sure that there are same entries for each field.
        if (len(schemas) != length) or (len(ports) != length):
            self.logger.error("The length of names, schemas, and ports do not match in config.ini file.")
        # Don't do anything if there is only one entry and it's empty.
        elif length == 1 and childs[0] == '' and schemas[0] == '' and ports[0] == '':
            self.logger.error("No child nodes listed in the config.ini file.")
        else:
            # Go through the list of childs and send signal to each of them.
            for index in range(len(childs)):

                if childs[index] == '':
                    self.logger.error("Host field is blank, skipping to next child host in config.ini.")
                    continue

                hostname = childs[index]
                schema = schemas[index]
                port = ports[index]

                # If it's not defined, use the default
                if (schema == ''):
                    schema = 'https'
                if (port == ''):
                    port = '9092'

                # Send the signal to individual child.
                send_signal_to_child(hostname, schema, port, 'lock', username, password)


    def unlock_childs(self, username, password):
        """Unlocks all of the child nodes with the provided hostnames/ips in the
            'config.ini' file. If there is not a hostname specified, skip to next one.
            If the schema or the port filed is left empty for the hostname, it will
            choose the defaults. (Defaults are 'https' for schema and '9092' for the
            port.

        Args:
            username: The username of the screenlock.
            password: The password of the screenlock.
        """

        # Gets the list of childs.
        childs = self.config.getFromSubHosts('names')
        # Gets the list of schemas.
        schemas = self.config.getFromSubHosts('schemas')
        # Gets the list of the ports.
        ports = self.config.getFromSubHosts('ports')

        length = len(childs)

        # Makes sure that there are same entries for each field.
        if (len(schemas) != length) or (len(ports) != length):
            self.logger.error("The length of names, schemas, and ports do not match in config.ini file.")

        # Don't do anything if there is only one entry and it's empty.
        elif length == 1 and childs[0] == '' and schemas[0] == '' and ports[0] == '':
            self.logger.error("No child nodes listed in the config.ini file.")
        else:
            # Go through the list of childs and send signal to each of them.
            for index in range(len(childs)):

                if childs[index] == '':
                    self.logger.error("Host field is blank, skipping to next child host in config.ini.")
                    continue

                hostname = childs[index]
                schema = schemas[index]
                port = ports[index]

                # If it's not defined, use the default
                if schema == '':
                    schema = 'https'
                if port == '':
                    port = '9092'

                # Send the signal to individual child.
                send_signal_to_child(hostname, schema, port, 'unlock', username, password)


def send_signal_to_child(hostname, schema, port, command, username, password):
    """Sends the child nodes a signal to lock or unlock the screenlock app.

    Args:
        hostname: The hostname/ip of the child node that you would like to lock/unlock.
        schemma: Type of schema.
        port: The port number of the screenlock app server.
        command: 'lock' or 'unlock'.
    """

    logging.info("Sending " + command + " single to " + hostname + ".")
    url = '%s://%s:%s/%s' % (schema, hostname, port, command)
    auth = HTTPBasicAuth(username, password)
    logging.debug("Proxying request: %s, %s" % (url, command))
    response = requests.post(url, data=None, headers=None, auth=auth)
    logging.info("Got response code %s " % response.status_code)




