import tornado.ioloop
import tornado.web
import tornado.websocket
import os, json, time, threading



threads = {
    "steppers": {
        "x": {
            "alive": False,
            "threadObject": None,
            "currentDirection": None
        },
        "y": {
            "alive": False,
            "threadObject": None,
            "currentDirection": None

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
                threads['steppers'][axis]['currentDirection'] = commandObject['direction']
                
                t = threading.Thread(target=stepper, args=(axis, direction))
                
                threads['steppers'][axis]['threadObject'] = t
                t.start()



            elif not commandObject['start'] and threads['steppers'][axis]['currentDirection'] == commandObject['direction']:

                threads['steppers'][axis]['alive'] = False
                threads['steppers'][axis]['threadObject'] = None
                threads['steppers'][axis]['currentDirection'] = None

        elif command == "fire":
            fire()

        elif command == "reload":
            load()


        # echo back message verbatim
        self.write_message(message)




# http handling stuff

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("CannonWebAuth")

class MainHandler(BaseHandler):
    def get(self):
        
        if not self.current_user:
            self.redirect("/login")
            return
        
        currentPassword = tornado.escape.xhtml_escape(self.current_user)
        
        if currentPassword != PASSWORD:
            self.redirect("/login")
            return

        self.render("cannon.html")

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        self.set_secure_cookie("CannonWebAuth", self.get_argument("password"))
        self.redirect("/")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("CannonWebAuth")
        self.redirect("/")


if __name__ == "__main__":
    
    PASSWORD = "password"

    handlers = [
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': "./"}),
        (r"/websocket", WebSocket)
    ]
    application = tornado.web.Application(handlers, cookie_secret=PASSWORD)
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
