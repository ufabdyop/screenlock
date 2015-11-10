import screenlockConfig

config = screenlockConfig.SLConfig()
PORT=config.get('port')

lockControl = screenlockController.SLController()

class OptimisticCoralResponse(protocol.Protocol):

    #def __init__(self, *args, **kwargs):
        #self.lockControl = screenlockController.SLController()
        #super(protocol.Protocol, self).__init__(*args, **kwargs)

    def dataReceived(self, data):
        global lockControl
        print("got a command! first byte: %s, second byte: %s" % (ord(data[0]), ord(data[1])))
        response = 0

        if ord(data[1]) == 17: #SENSE COMMAND
            print("sense command")
            if lockControl.is_running():
                response = chr(0)
            else:
                response = chr(1)
        elif ord(data[1]) == 1: #TURN OFF COMMAND
            print("disable command")
            lockControl.lock_screen()
            response = chr(1)
        elif ord(data[1]) == 9: #TURN ON COMMAND
            print("enable command")
            lockControl.unlock_screen()
            response = chr(1)
        else:
            response = chr(1) #UNKNOWN COMMAND
        print("writing response: %s" % ord(response))
        self.transport.write(response)

class OptimistFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return OptimisticCoralResponse()

lockControl.lock_screen()
print("starting listening on %s" % PORT)
endpoints.serverFromString(reactor, "tcp:" + str(PORT)).listen(OptimistFactory())
reactor.run()

