from screenlockConfig import SLConfig
import logging, log

class child_controller(object):
    def __init__(self):
        log.initialize_logging("childController")
        self.logger = logging.getLogger("childController")
        self.config = SLConfig()

    def lock_childs(self):
        childs = self.config.getFromSubHosts('names')
        schemas = self.config.getFromSubHosts('schemas')
        ports = self.config.getFromSubHosts('ports')

        length = len(childs)
        print(length)
        print(len(schemas))
        print(len(ports))
        if (len(schemas) >= length) or (len(ports) >= length):
            self.logger.error("The length of names, schemas, and ports do not match in config.ini file.")
        if length == 1 and childs[0] == '' and schemas[0] == '' and ports[0] == '':
            self.logger.error("No child nodes listed in the config.ini file.")
        else:
            for index in range(len(childs)):
                if childs[index] == '':
                    self.logger.error("Host field is blank, skipping to next child host in config.ini.")
                    continue
                hostname = childs[index]
                schema = schemas[index]
                port = ports[index]
                print(hostname)

                if (schema == ''):
                    schema = 'https'
                print(schema)

                if (port == ''):
                    port = '9092'
                print(port)


    # def unlock_childs(self):
    #     childs = self.config.getFromSubHosts('names')
    #     schemas = self.config.getFromSubHosts('schemas')
    #     ports = self.config.getFromSubHosts('ports')
    #
    #     length = len(childs)
    #
    #     if len(schemas) != length or len(ports) != length:
    #         self.logger.error("The length of names, schemas, and ports do not match in config.ini file.")
    #     if length == 1 and childs[0] == '' and schemas[0] == '' and ports[0] == '':
    #         self.logger.error("No child nodes listed in the config.ini file.")
    #     else:
    #         for index in range(len(childs)):
    #             if childs[index] == '':
    #                 self.logger.error("Host field is blank, skipping to next child host in config.ini.")
    #                 continue
    #             print(childs[index])
    #             print(schemas[index])
    #             print(ports[index])
