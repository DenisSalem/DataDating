#! /usr/bin/python3

import os
import sys
import cgi
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
    def do_POST(self):
        print("do something", self.path)
                
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD':'POST',
                'CONTENT_TYPE':self.headers['Content-Type']
            }
        )

        print(ToJSON(form))
        
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
    def __init__(self):
        self.allow_reuse_address = True
        super(Server, self).__init__(("127.0.0.1",8282), RequestHandler)

    def handle_error(self, request, client_address):
        if sys.exc_info()[0] == Termination:
            raise Termination()
        
        else:
            super(Server, self).handle_error(request, client_address)
        
