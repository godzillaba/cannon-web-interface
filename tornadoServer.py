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

def get_client_ip(self):
    return repr(self.request).split("remote_ip='")[1].split("'")[0]

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return {
            "username": self.get_secure_cookie("CannonWebAuth_user"), 
            "password": self.get_secure_cookie("CannonWebAuth_password")
        }

class MainHandler(BaseHandler):
    def get(self):
        
        if not self.current_user['username'] or not self.current_user['password']:
            print "%s -- GET / -- (cookies not found, redirecting to /login)" % get_client_ip(self)
            self.redirect("/login")
            return
        
        currentUsername = tornado.escape.xhtml_escape(self.current_user['username'])
        currentPassword = tornado.escape.xhtml_escape(self.current_user['password'])
        
        if currentUsername in users and users[currentUsername] == currentPassword:
            print "%s -- GET / --" % get_client_ip(self)
            self.render("cannon.html", user=currentUsername)

        else:
            print "%s -- GET / -- (incorrect password, redirecting to /login)" % get_client_ip(self)
            self.redirect("/login")
            return


class LoginHandler(BaseHandler):
    def get(self):
        print "%s -- GET /login" % get_client_ip(self)
        
        if self.current_user and self.current_user['username']:
            user = self.current_user['username']
        else:
            user = ""

        self.render("login.html", user=user)

    def post(self):
        print "%s -- POST /login" % get_client_ip(self)
        self.set_secure_cookie("CannonWebAuth_user", self.get_argument("username"))
        self.set_secure_cookie("CannonWebAuth_password", self.get_argument("password"))

        print "%s logged in" % self.current_user['username']
        self.redirect("/")

class LogoutHandler(BaseHandler):
    def get(self):
        print "%s -- GET /logout -- (clearing cookie)" % get_client_ip(self)
        
        print "%s logged out" % self.current_user['username']
        self.clear_cookie("CannonWebAuth_password")
        self.redirect("/")


if __name__ == "__main__":
    
    PASSWORD = "password"
    PORT = 8888

    users = {
        "admin": "pwd",
        "henry": "ppp"
    }

    handlers = [
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': "./"}),
        (r"/websocket", WebSocket)
    ]
    application = tornado.web.Application(handlers, cookie_secret=PASSWORD)
    application.listen(PORT)
    tornado.ioloop.IOLoop.current().start()
