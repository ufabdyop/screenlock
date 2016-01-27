import logging, sys
import screenlockConfig,log,screenlockController
from twisted.internet import protocol, reactor, endpoints

log.initialize_logging("NCD Server")
logger = logging.getLogger()

class OptimisticCoralResponse(protocol.Protocol):

    #def __init__(self, *args, **kwargs):
        #self.lockControl = screenlockController.SLController()
        #super(protocol.Protocol, self).__init__(*args, **kwargs)

    def dataReceived(self, data):
        global lockControl
        global logger
        logger.debug("got a command! first byte: %s, second byte: %s" % (ord(data[0]), ord(data[1])))
        response = 0

        if ord(data[1]) == 17: #SENSE COMMAND
            logger.debug("sense command")
            if lockControl.is_running():
                response = chr(0)
            else:
                response = chr(1)
        elif ord(data[1]) == 1: #TURN OFF COMMAND
            logger.debug("disable command")
            lockControl.lock_screen()
            response = chr(1)
        elif ord(data[1]) == 9: #TURN ON COMMAND
            logger.debug("enable command")
            lockControl.unlock_screen()
            response = chr(0)
        else:
            response = chr(1) #UNKNOWN COMMAND
        logger.debug("writing response: %s" % ord(response))
        self.transport.write(response)

class OptimistFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return OptimisticCoralResponse()
try:
    config = screenlockConfig.SLConfig()
    PORT=config.get('port')
    lockControl = screenlockController.SLController()
    lockControl.lock_screen()
    logger.debug("starting listening on %s" % PORT)
    endpoints.serverFromString(reactor, "tcp:" + str(PORT)).listen(OptimistFactory())
    reactor.run()
except Exception as e:
    logger.error("NCD Caught Error: %s" % e)