import tornado.ioloop
import tornado.web
import tornado.websocket
import os, json, time, threading



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



class WebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_close(self):
        print("WebSocket closed")
    

    def on_message(self, message):

        commandObject = json.loads(message)

        
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
        self.write_message(message)




if __name__ == "__main__":
    
    handlers = [
        (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': "./"}),
        (r"/websocket", WebSocket)
    ]
    application = tornado.web.Application(handlers)
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()