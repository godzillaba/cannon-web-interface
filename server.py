
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import json, time, threading



threads = {
    "steppers": {
        "x": {
            "alive": False,
            "threadObject": None
        },
        "y": {
            "alive": False,
            "threadObject": None
        }
    }
}




def stepper(axis, direction):
    print "stepper: %s %s STARTING" % (axis, str(direction))
    
    while threads["steppers"][axis]['alive'] == True:
        
        # stepper code here
        time.sleep(.2)

    print "stepper: %s %s STOPPING" % (axis, str(direction))

def fire():
    print "Firing cannon!!!"

def load():
    print "Reloading cannon!!!"


class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

    def onMessage(self, payload, isBinary):

        commandObject = json.loads(payload)

        
        command = commandObject['command']

        # if stepper command was received, evaluate axis, direction, start/stop, etc and start/stop thread
        if command == "stepper":
            axis = commandObject['axis']

            if commandObject['start'] and not threads['steppers'][axis]['alive']:
                
                direction = commandObject['direction']
                
                threads['steppers'][axis]['alive'] = True
                
                t = threading.Thread(target=stepper, args=(axis, direction))
                
                threads['steppers'][axis]['threadObject'] = t
                t.start()

            elif not commandObject['start']:

                threads['steppers'][axis]['alive'] = False
                threads['steppers'][axis]['threadObject'] = None

        elif command == "fire":
            fire()

        elif command == "reload":
            load()



        # echo back message verbatim
        self.sendMessage(payload)



if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000", debug=False)
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    reactor.listenTCP(9000, factory)
    reactor.run()
