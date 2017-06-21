#! /usr/bin/python3

import http.server

from DataDating.Controler.MainControler import MainControler
from DataDating.Controler.MainControler import Termination
from DataDating.Controler.MainControler import NonHtml

mainControler = MainControler()

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.output = ""
        super(RequestHandler, self).__init__(request, client_address, server)

    def log_message(self, format, *args):
        global mainControler
        if mainControler.verbose:
            super(RequestHandler, self).log_message(format, *args)
        
    def ReplyHTML(self):
            self.protocol_version='HTTP/1.1'
            self.send_response(200,'OK')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.output.encode("utf-8"))
    
    def do_POST(self):
        global mainControler
        self.do_GET()

    def do_GET(self):
        global mainControler
        self.output = str()
        
        try:
            self.output = mainControler.GetResponse(self.path)
            self.ReplyHTML()

        except NonHtml:
            super(RequestHandler, self).do_GET()
