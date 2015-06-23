
from twisted.internet import protocol, reactor, endpoints
import pprint

import screenlockConfig, screenlockController
config = screenlockConfig.SLConfig()
PORT=config.get('port')

class OptimisticCoralResponse(protocol.Protocol):
    state = 0 #off

    def dataReceived(self, data):
        print("got a command! first byte: %s, second byte: %s" % (ord(data[0], ord(data[1]))))
        response = 0

        if ord(data[1]) == 17: #SENSE COMMAND
                response = chr(self.state)
        elif ord(data[1]) == 1: #TURN OFF COMMAND
                self.state = 0
                response = chr(1)
        elif ord(data[1]) == 9: #TURN ON COMMAND
                self.state = 1
                response = chr(1)
        else:
                response = chr(1) #UNKNOWN COMMAND
        print("writing response: %s" % ord(response))
        self.transport.write(response)

class OptimistFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return OptimisticCoralResponse()

endpoints.serverFromString(reactor, "tcp:" + str(PORT)).listen(OptimistFactory())
reactor.run()

