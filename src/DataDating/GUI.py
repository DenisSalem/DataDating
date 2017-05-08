#! /usr/bin/python3

import os
import io
import sys
import cgi
import json
import http.server
import socketserver
import DataDating.Pattern

pathToChunks = "gui/"

pageIndex = open(pathToChunks+"index.html","r").read()
pageProfile = open(pathToChunks+"profile.html","r").read()

patternProcessor = DataDating.Pattern.processor(".:",":.","::")
patternProcessor.preProcess("Index", pageIndex)

def ToJSON(data):
    output = dict()
    for key in dict(data).keys():
        output[key] = data[key].value

    return output

class Termination(Exception):
    pass

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        if self.verbose:
            super(RequestHandler, self).log_message()
        
    def __init__(self, request, client_address, server):
        self.output = ""
        self.verbose = False
        super(RequestHandler, self).__init__(request, client_address, server)

    def reply(self):
            self.protocol_version='HTTP/1.1'
            self.send_response(200,'OK')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.output.encode("utf-8"))
    
    # replacement of the default do_GET() method, handling server response.
    def save_JSON(self, path, data):
            output = io.open(path,"w")
            output.write(json.dumps(data))
            output.close()

    def load_JSON(self, path):
        try:
            data = io.open(self.profileFolder+"/profile.json", "r").read()
            return json.loads(data)
        except:
            return {}

    def do_POST(self):
        if self.path == "/Profile":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD':'POST',
                    'CONTENT_TYPE':self.headers['Content-Type']
                }
            )

            self.save_JSON(self.profileFolder+"/profile.json", ToJSON(form))
            self.do_GET()

    def do_GET(self):
        # Send assets or ressources
        if self.path == "/":
            patternProcessor.Set("Content",pageProfile)
            self.output = patternProcessor.parse("Index")
            self.reply()

        elif self.path == "/Logout":
            raise Termination()

        elif self.path == "/Profile":
            profile = self.load_JSON(self.profileFolder+"/profile.json")
            print(profile)
            patternProcessor.Set("Content",pageProfile)
            self.output = patternProcessor.parse("Index")
            self.reply()

        elif self.path == "/Favourites":
            patternProcessor.Set("Content","")
            self.output = patternProcessor.parse("Index")
            self.reply()
        elif self.path == "/Matchs":
            patternProcessor.Set("Content","")
            self.output = patternProcessor.parse("Index")
            self.reply()

        else:
            super(RequestHandler, self).do_GET()

class Server(socketserver.TCPServer):
    def __init__(self, profileFolder):
        self.profileFolder = profileFolder
        self.allow_reuse_address = True
        super(Server, self).__init__(("127.0.0.1",8282), RequestHandler)
        self.RequestHandlerClass.profileFolder = self.profileFolder

    def handle_error(self, request, client_address):
        if sys.exc_info()[0] == Termination:
            raise Termination()
        
        else:
            super(Server, self).handle_error(request, client_address)
        
