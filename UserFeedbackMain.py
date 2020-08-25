import cherrypy
import os.path
from os.path import abspath

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

        #return '''<meta http-equiv="refresh" content=";URL=https://www.youtube.com/watch?v=dQw4w9WgXcQ">'''

        return open("media/index.html")

    @cherrypy.expose
    def generate(self):
        pass


    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def handle_post(self, request):
        body = request.json

        if not all(elem in FEEDBACK_TABLE for elem in body):
            raise cherrypy.HTTPError(400, "Bad Request")

        values = [str(body[key]) for key in FEEDBACK_TABLE]
        print(values)
        self.form.write('\t'.join(values) + '\n')
        self.form.flush()

# Routes
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def average_satisfaction(self):
        if cherrypy.request.method != "GET":
            raise cherrypy.HTTPError(400, "Bad Request")

        average = 0
        nb = 0
        with open(FORM_PATH) as f:
            next(f)
            for row in f:
                content = row.split('\t')
                nb += 1
                average += float(content[FEEDBACK_TABLE.index("Rate")])

        return {"data": average / nb}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def client_comments(self):
        if cherrypy.request.method != "GET":
            raise cherrypy.HTTPError(400, "Bad Request")

        users = []
        messages = []

        with open(FORM_PATH) as f:
            next(f)
            for row in f:
                content = row.split('\t')
                users.append(content[FEEDBACK_TABLE.index("User")])
                messages.append(content[FEEDBACK_TABLE.index("Message")])

        return {"users": users, "messages": messages}

    # TO HANDLE A NEW URL CHANGE "urltest"
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def urltest(self):
        if cherrypy.request.method != "GET":
            raise cherrypy.HTTPError(400, "Bad Request")

        print("urltest")
        return {"message": "urltest"}


if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': SERVER_IP,
        'server.socket_port': SERVER_PORT,
        'cors.expose.on': True
    })
    cherrypy.quickstart(UserFeedback())
