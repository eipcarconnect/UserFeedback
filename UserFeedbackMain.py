import cherrypy
import os.path

from UserFeedbackHelper import *


class UserFeedback(object):
    def __init__(self):
        if not os.path.isfile(FORM_PATH):
            with open(FORM_PATH, 'w') as f:
                f.write('\t'.join(FEEDBACK_TABLE) + '\n')
                f.flush()

        self.form = open(FORM_PATH, 'a')

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def index(self):
        if cherrypy.request.method == "POST":
            return self.handle_post(cherrypy.request)

        return '''<meta http-equiv="refresh" content=";URL=https://www.youtube.com/watch?v=dQw4w9WgXcQ">'''

    @cherrypy.expose
    def generate(self):
        pass

    @cherrypy.tools.json_out()
    def handle_post(self, request):
        body = request.json

        if not all(elem in FEEDBACK_TABLE for elem in body):
            raise cherrypy.HTTPError(400, "Bad Request")

        values = [str(body[key]) for key in FEEDBACK_TABLE]
        print(values)
        self.form.write('\t'.join(values) + '\n')
        self.form.flush()

    # TO HANDLE A NEW URL CHANGE "urltest"
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def urltest(self):
        print("urltest")
        return {"message": "urltest"}


if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': SERVER_IP,
        'server.socket_port': SERVER_PORT
    })
    cherrypy.quickstart(UserFeedback())
    print("alo")
