import cherrypy
import os.path

from UserFeedbackHelper import *


class UserFeedback(object):
    def __init__(self):
        if not os.path.isfile(FORM_PATH):
            with open(FORM_PATH, 'w') as f:
                f.write('\t'.join(FEEDBACK_TABLE))

        self.form = open(FORM_PATH, 'a')

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def index(self):
        if cherrypy.request.method == "POST":
            return self.handle_post(cherrypy.request)

        return '''<meta http-equiv="refresh" content="durée;URL=https://www.youtube.com/watch?v=dQw4w9WgXcQ">'''

    @cherrypy.expose
    def generate(self):
        pass

    # TO HANDLE A NEW URL CHANGE "urltest"
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def urltest(self):
        print("urltest")
        return {"message": "urltest"}

    def handle_post(self, request):
        body = request.json
        print("post", body)
        return {"type": "post"}


if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': SERVER_IP,
        'server.socket_port': SERVER_PORT
    })
    cherrypy.quickstart(UserFeedback())
    print("alo")
